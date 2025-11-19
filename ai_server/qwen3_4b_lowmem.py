#!/usr/bin/env python3
"""
Reality Lab Qwen3-4B Server (Low Memory Version with 8-bit quantization)
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TextIteratorStreamer
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import logging
import time
import requests
import json
import re
import threading
from threading import Thread
from datetime import datetime
import pytz
from hierarchical_retriever import HierarchicalRetriever

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables
model = None
tokenizer = None
rag_retriever = None
last_activity_time = None
shutdown_timeout = 120  # 2 minutes in seconds
shutdown_timer_thread = None
model_choice_global = 'qwen3-4b'  # Store model choice for reloading
is_loading_model = False  # Track if model is currently being loaded
request_lock = threading.Lock()  # Lock for sequential request processing
is_processing_request = False  # Track if a request is currently being processed

def is_rest_time():
    """
    Check if current time is during rest hours (4 AM - 8 AM KST)
    Returns: (bool, str) - (is_rest_time, message)
    """
    # TEMPORARY: Rest time disabled for testing
    return False, ("", "")

    # Original code (commented out for testing):
    # kst = pytz.timezone('Asia/Seoul')
    # now_kst = datetime.now(kst)
    # current_hour = now_kst.hour
    #
    # # Rest time: 4 AM - 8 AM KST
    # if 4 <= current_hour < 8:
    #     resume_time = now_kst.replace(hour=8, minute=0, second=0, microsecond=0)
    #     message_ko = f"현재 AI 챗봇 휴식시간입니다 (한국 시간 오전 4시~8시).\n오전 8시부터 다시 이용 가능합니다."
    #     message_en = f"AI Chatbot is currently resting (4 AM - 8 AM KST).\nService will resume at 8 AM KST."
    #     return True, (message_ko, message_en)
    #
    # return False, ("", "")

def load_model(model_choice='qwen3-4b'):
    """Load Qwen model with 4-bit quantization

    Args:
        model_choice: 'qwen3-4b' or 'qwen25-3b'
    """
    global model, tokenizer

    try:
        # Select model path based on choice
        model_paths = {
            'qwen3-4b': "/home/i0179/.cache/huggingface/hub/qwen3-4b-git",
            'qwen25-3b': "/home/i0179/.cache/huggingface/hub/qwen25-3b-git"
        }

        model_names = {
            'qwen3-4b': "Qwen3-4B",
            'qwen25-3b': "Qwen2.5-3B"
        }

        if model_choice not in model_paths:
            raise ValueError(f"Invalid model choice: {model_choice}. Choose from {list(model_paths.keys())}")

        model_path = model_paths[model_choice]
        model_name = model_names[model_choice]

        logger.info(f"Loading {model_name} tokenizer from local path")
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Set padding token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        logger.info(f"Loading {model_name} model with 4-bit quantization")

        # Configure 4-bit quantization for maximum memory reduction
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=quantization_config,
            device_map="auto",
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )

        logger.info(f"✅ {model_name} model loaded successfully with 4-bit quantization")
        logger.info(f"Model vocab size: {model.config.vocab_size}, Tokenizer vocab size: {len(tokenizer)}")
        logger.info(f"PAD token ID: {tokenizer.pad_token_id}, EOS token ID: {tokenizer.eos_token_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

def update_activity():
    """Update last activity time"""
    global last_activity_time
    last_activity_time = time.time()

def unload_model():
    """Unload model from GPU to free memory"""
    global model, tokenizer

    if model is None and tokenizer is None:
        return  # Already unloaded

    logger.info("🔌 Unloading model from GPU...")

    # Clear model and tokenizer
    if model is not None:
        del model
        model = None
    if tokenizer is not None:
        del tokenizer
        tokenizer = None

    # Force garbage collection and clear CUDA cache
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    logger.info("✅ GPU memory freed. Server remains active for auto-reload.")

def ensure_model_loaded():
    """Ensure model is loaded, reload if necessary"""
    global model, tokenizer, is_loading_model, model_choice_global

    if model is not None and tokenizer is not None:
        return True  # Already loaded

    if is_loading_model:
        return False  # Currently loading, caller should wait

    # Reload model
    is_loading_model = True
    try:
        logger.info("🔄 Model not loaded. Reloading...")
        success = load_model(model_choice_global)
        is_loading_model = False
        return success
    except Exception as e:
        logger.error(f"Failed to reload model: {e}")
        is_loading_model = False
        return False

def check_idle_timeout():
    """Check if server has been idle and unload model if necessary"""
    global last_activity_time

    while True:
        time.sleep(10)  # Check every 10 seconds

        if last_activity_time is None:
            continue

        idle_time = time.time() - last_activity_time

        if idle_time >= shutdown_timeout and (model is not None or tokenizer is not None):
            # Double-check activity time before unloading (prevent race condition with heartbeat)
            final_idle_time = time.time() - last_activity_time
            if final_idle_time >= shutdown_timeout:
                logger.info(f"⏱️  Server idle for {final_idle_time:.1f}s (threshold: {shutdown_timeout}s)")
                unload_model()
                last_activity_time = None  # Reset to prevent repeated unload attempts
            else:
                logger.info(f"⏱️  Unload cancelled - recent activity detected ({final_idle_time:.1f}s < {shutdown_timeout}s)")

def contains_chinese(text):
    """Check if text contains Chinese characters"""
    # Chinese Unicode ranges: \u4e00-\u9fff (CJK Unified Ideographs)
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    matches = chinese_pattern.findall(text)
    # Consider it Chinese if there are more than 5 Chinese characters
    return len(matches) > 5

def ensure_sentence_completion(text, language='ko'):
    """Ensure the response ends with complete sentences"""

    # Korean sentence endings
    korean_endings = ['다', '요', '니다', '습니다', '어요', '아요', '게요', '죠', '네요', '세요']
    # English sentence endings
    english_endings = ['.', '!', '?']

    if language == 'ko':
        # Check if text ends with Korean sentence ending
        for ending in korean_endings:
            if text.endswith(ending):
                return text

        # Find the last complete Korean sentence
        sentences = re.split(r'[.!?]|(?<=[다요니습어아게죠네세])\s', text)
        if len(sentences) > 1 and sentences[-2].strip():
            # Return text up to the last complete sentence
            last_complete = sentences[-2].strip()
            # Find position of last complete sentence
            pos = text.rfind(last_complete)
            if pos != -1:
                end_pos = pos + len(last_complete)
                return text[:end_pos].strip()
    else:
        # English text
        for ending in english_endings:
            if text.endswith(ending):
                return text

        # Find last complete English sentence
        sentences = re.split(r'[.!?]\s+', text)
        if len(sentences) > 1 and sentences[-2].strip():
            # Return up to last complete sentence
            return '.'.join(sentences[:-1]) + '.'

    return text

def clean_korean_query(query):
    """Remove Korean particles from query for better keyword matching"""
    # Sort by length (longest first) to match compound particles like "이라는" before "이"
    particles = ['이라는', '까지', '에서', '으로', '에게', '한테', '부터', '라는', '이', '가', '을', '를', '은', '는', '에', '의', '와', '과', '도', '만', '로']

    cleaned_words = []
    for word in query.split():
        if len(word) > 1:
            clean_word = word
            for particle in particles:
                if clean_word.endswith(particle) and len(clean_word) > len(particle):
                    clean_word = clean_word[:-len(particle)]
                    break  # Stop after first match
            cleaned_words.append(clean_word if len(clean_word) > 1 else word)
        else:
            cleaned_words.append(word)

    return ' '.join(cleaned_words)

def extract_relevant_sections(question, knowledge_base_path, max_sections=5, max_chars=2000):
    """Extract relevant sections from knowledge base based on keywords in question"""
    try:
        with open(knowledge_base_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into smaller chunks by individual entries (using "이름:" as delimiter for member entries)
        chunks = []
        current_chunk = []
        lines = content.split('\n')
        current_header = ""

        for line in lines:
            # Track section headers
            if line.startswith('===') or line.startswith('##'):
                current_header = line
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
            # Split by individual member entries (이름:)
            elif line.strip().startswith('이름:'):
                if current_chunk and len(current_chunk) > 1:  # Don't split if just header
                    chunks.append('\n'.join(current_chunk))
                current_chunk = [current_header, line] if current_header else [line]
            else:
                current_chunk.append(line)

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        # Extract keywords from question (including original casing for name matching)
        # Remove common Korean particles to get clean keywords
        # Sort by length (longest first) to match compound particles like "이라는" before "이"
        particles = ['이라는', '까지', '에서', '으로', '에게', '한테', '부터', '라는', '이', '가', '을', '를', '은', '는', '에', '의', '와', '과', '도', '만', '로']

        keywords = set()
        keywords_original = set()
        for word in question.split():
            if len(word) > 1:
                # Remove particles from word (try longest first)
                clean_word = word
                for particle in particles:
                    if clean_word.endswith(particle) and len(clean_word) > len(particle):
                        clean_word = clean_word[:-len(particle)]
                        break  # Stop after first match

                if len(clean_word) > 1:
                    keywords.add(clean_word.lower())
                    keywords_original.add(clean_word)
                # Also add original word
                keywords.add(word.lower())
                keywords_original.add(word)

        # Score each chunk
        chunk_scores = []
        for i, chunk in enumerate(chunks):
            chunk_lower = chunk.lower()
            score = 0

            # Check keywords (case-insensitive)
            for keyword in keywords:
                if keyword in chunk_lower:
                    # Higher score for exact matches
                    score += chunk_lower.count(keyword) * 3

            # Check keywords with original casing (for names)
            for keyword in keywords_original:
                if keyword in chunk:
                    score += chunk.count(keyword) * 5

            # Boost score for section headers that match
            first_line = chunk.split('\n')[0] if chunk else ''
            for keyword in keywords:
                if keyword in first_line.lower():
                    score += 15

            chunk_scores.append((score, i, chunk))

        # Sort by score and select top chunks
        chunk_scores.sort(reverse=True, key=lambda x: x[0])

        # Get top chunks but limit total characters
        selected_chunks = []
        total_chars = 0

        for score, idx, chunk in chunk_scores[:max_sections * 2]:  # Check more chunks
            if score > 0:  # Only include chunks with matches
                if total_chars + len(chunk) <= max_chars:
                    selected_chunks.append(chunk)
                    total_chars += len(chunk)
                    if len(selected_chunks) >= max_sections:
                        break
                elif total_chars < max_chars // 2:  # If we haven't used much space yet
                    # Add truncated chunk
                    remaining = max_chars - total_chars
                    if remaining > 300:
                        selected_chunks.append(chunk[:remaining] + "...")
                        break

        return '\n\n'.join(selected_chunks) if selected_chunks else ""

    except Exception as e:
        logger.error(f"Error extracting relevant sections: {e}")
        return ""

def generate_response(prompt, language='ko', max_length=700):
    """Generate AI response"""
    global model, tokenizer, rag_retriever

    if model is None or tokenizer is None:
        return "AI model not loaded"

    try:
        # Use RAG (Retrieval-Augmented Generation) with cleaned query
        rag_context = ""
        if rag_retriever is not None:
            try:
                # Clean query by removing Korean particles
                cleaned_prompt = clean_korean_query(prompt)
                logger.info(f"Original query: {prompt}")
                logger.info(f"Cleaned query: {cleaned_prompt}")

                # Search with lower threshold for more results
                search_results = rag_retriever.search(cleaned_prompt, k=5, min_score=0.25)
                if search_results:
                    rag_context = rag_retriever.format_context(search_results, language=language)
                    rag_context += "\n\n"
                    logger.info(f"RAG found {len(search_results)} documents")
                else:
                    logger.warning("RAG found no matching documents")
            except Exception as e:
                logger.warning(f"RAG search failed: {e}")

        # Create language-specific system prompt (concise yet friendly with key info)
        if language == 'en':
            system_content = f"""{rag_context}You are a helpful assistant for Reality Lab at Soongsil University. Be concise yet friendly, and include all essential information.

Use the reference materials above to answer the question. If the references don't contain the answer, use your general knowledge about Reality Lab.

Reality Lab (Soongsil University):
- Established 2023, Led by Prof. Heewon Kim
- Research: Robotics, Computer Vision, Machine Learning, Multimodal AI, Healthcare AI
- Location: 105 Sadan-ro, Dongjak-gu, Seoul
- Contact: +82-2-820-0679

Guidelines:
- Be concise yet polite and friendly
- Include all key information needed
- Use natural, complete sentences
- No <think> tags or internal reasoning"""
        else:
            # Ultra-simple prompt for weak model
            system_content = f"""Reality Lab Q&A 봇입니다. 주어진 정보에서 답을 찾아 한국어로 간단히 답변하세요.

기본 정보:
- 설립: 2023년, 김희원 교수님
- 연구: 로보틱스, 컴퓨터비전, 기계학습, 멀티모달 AI, 헬스케어 AI
- 위치: 서울특별시 동작구 사당로 105, 숭실대학교
- 전화: +82-2-820-0679

{rag_context}

답변 형식:
- 한국어로만 답변
- 1-2문장으로 답변
- 정보가 없으면 "죄송합니다. 해당 정보를 찾을 수 없습니다. 김희원 교수님(heewon@ssu.ac.kr)께 문의해주세요."

예시:
Q: 박성용 학생 연구 분야는?
A: 박성용 학생은 Image Restoration과 AI for Astronomy를 연구하고 있습니다."""

        # Create chat template
        messages = [
            {
                "role": "system",
                "content": system_content
            },
            {"role": "user", "content": prompt}
        ]

        # Apply chat template
        formatted_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        # Tokenize input
        inputs = tokenizer(
            formatted_prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(model.device)

        # Generate response with optimized parameters for speed
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=max_length,
                min_new_tokens=50,  # Ensure substantial response
                do_sample=False,  # Greedy decoding (fastest)
                num_beams=1,  # No beam search (fastest)
                pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id,
                eos_token_id=[tokenizer.eos_token_id] if tokenizer.eos_token_id is not None else None,
                attention_mask=inputs.attention_mask,
                use_cache=True,  # Use KV cache for speed
                repetition_penalty=1.1  # Prevent repetition, faster termination
            )

        # Decode response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Calculate generated token count
        input_length = inputs.input_ids.shape[1]
        output_length = outputs.shape[1]
        generated_tokens = output_length - input_length

        # Extract generated text
        if "assistant\n" in response:
            parts = response.split("assistant\n")
            if len(parts) > 1:
                generated_text = parts[-1].replace("<|im_end|>", "").strip()
            else:
                generated_text = response[len(formatted_prompt):].strip()
        else:
            generated_text = response[len(formatted_prompt):].strip()

        # Remove thinking tags and content
        generated_text = re.sub(r'<think>.*?</think>', '', generated_text, flags=re.DOTALL).strip()
        # Also remove any remaining <think> or </think> tags
        generated_text = generated_text.replace('<think>', '').replace('</think>', '').strip()

        # Remove any database info header that leaked through
        generated_text = re.sub(r'===\s*데이터베이스 정보\s*===', '', generated_text).strip()
        generated_text = re.sub(r'===\s*Database Information\s*===', '', generated_text).strip()

        # Remove reference markers (legacy)
        generated_text = re.sub(r'\[참고자료\s*\d+[^\]]*\]', '', generated_text).strip()
        generated_text = re.sub(r'\[참조자료\s*\d+[^\]]*\]', '', generated_text).strip()

        # Remove internal reasoning markers
        generated_text = re.sub(r'\*\*정답\*\*:?', '', generated_text).strip()
        generated_text = re.sub(r'정답\s*:', '', generated_text).strip()
        generated_text = re.sub(r'질문\s*:', '', generated_text).strip()
        generated_text = re.sub(r'Q:', '', generated_text).strip()
        generated_text = re.sub(r'A:', '', generated_text).strip()

        # Remove separator lines
        lines = generated_text.split('\n')
        cleaned_lines = [line for line in lines if line.strip() != '---']
        generated_text = '\n'.join(cleaned_lines).strip()

        # Check for Chinese characters (for Korean language mode)
        if language == 'ko' and contains_chinese(generated_text):
            logger.warning("Chinese detected in Korean response, using fallback")
            # Provide Korean fallback message
            if '연구' in prompt or '분야' in prompt:
                generated_text = "Reality Lab의 주요 연구 분야는 로보틱스, 컴퓨터 비전, 기계학습, 멀티모달 AI, 헬스케어 AI입니다. 자세한 내용은 김희원 교수님(heewon@ssu.ac.kr)께 문의하시면 됩니다."
            elif '구성원' in prompt or '팀' in prompt or '멤버' in prompt:
                generated_text = "Reality Lab의 주요 구성원은 김희원 교수님(설립자), 이예빈 인턴(컴퓨터 비전, AI for Sports 연구) 등입니다. 자세한 구성원 정보는 연구실에 문의해주세요."
            elif '연락' in prompt or '이메일' in prompt or '전화' in prompt:
                generated_text = "Reality Lab 연락처: 전화 +82-2-820-0679, 이메일 heewon@ssu.ac.kr, 위치: 서울특별시 동작구 사당로 105 숭실대학교"
            else:
                generated_text = "죄송합니다. 질문에 대한 정확한 답변을 준비하지 못했습니다. 자세한 내용은 김희원 교수님(heewon@ssu.ac.kr, +82-2-820-0679)께 문의하시면 됩니다."

        # Ensure natural sentence completion
        if generated_text:
            generated_text = ensure_sentence_completion(generated_text, language)
            return generated_text, generated_tokens
        else:
            return "죄송합니다. 응답을 생성할 수 없습니다.", generated_tokens

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return "응답 생성 중 오류가 발생했습니다.", 0

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_name': 'Qwen3-4B-4bit'
    })

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    """Heartbeat endpoint to keep server alive and ensure model is loaded"""
    update_activity()

    # Check if model is loaded, if not, trigger auto-reload
    global model, is_loading_model

    model_status = 'loaded' if model is not None else 'unloaded'

    # If model is not loaded and not currently loading, trigger reload in background
    if model is None and not is_loading_model:
        logger.info("📥 Heartbeat received with unloaded model - triggering auto-reload")
        # Start loading in background (non-blocking)
        from threading import Thread
        def load_in_background():
            ensure_model_loaded()
        Thread(target=load_in_background, daemon=True).start()
        model_status = 'loading'
    elif is_loading_model:
        model_status = 'loading'

    return jsonify({
        'status': 'alive',
        'message': 'Server is active',
        'model_status': model_status
    })

@app.route('/status', methods=['GET'])
def server_status():
    """Get server status including idle time"""
    global last_activity_time

    if last_activity_time is None:
        idle_time = 0
    else:
        idle_time = time.time() - last_activity_time

    return jsonify({
        'status': 'running',
        'model_loaded': model is not None,
        'idle_time': idle_time,
        'shutdown_timeout': shutdown_timeout,
        'will_shutdown_in': max(0, shutdown_timeout - idle_time) if last_activity_time else None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    global is_processing_request

    try:
        # Check if it's rest time
        rest_time, messages = is_rest_time()
        if rest_time:
            message_ko, message_en = messages
            # Detect language from request if available
            data = request.get_json(force=True) if request.data else {}
            question = data.get('question', '') if data else ''
            # Simple language detection
            is_korean = any(ord(c) >= 0xAC00 and ord(c) <= 0xD7A3 for c in question)
            response_message = message_ko if is_korean else message_en

            return jsonify({
                'response': response_message,
                'tokens': len(response_message.split()),
                'response_time': 0.1,
                'rest_time': True
            })

        update_activity()  # Update activity on each chat request

        data = request.get_json(force=True)

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        if 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400

        user_question = data['question']
        language = data.get('language', 'ko')
        max_length = data.get('max_length', 700)  # Balanced default

        # Check if another request is currently being processed
        if is_processing_request:
            return jsonify({
                'response': '다른 사용자와 대화 중입니다. 잠시만 기다려주세요. 조금 더 오래 걸릴 수 있습니다.' if language == 'ko' else 'Currently talking with another user. Please wait, this may take a bit longer.',
                'tokens': 0,
                'response_time': 0,
                'status': 'waiting'
            })

        # Check if model is loaded, reload if necessary
        if is_loading_model:
            return jsonify({
                'response': 'AI 모델을 로딩 중입니다. 잠시만 기다려주세요... (5~10초 정도 소요됩니다)' if language == 'ko' else 'Loading AI model. Please wait... (Takes about 5~10 seconds)',
                'tokens': 0,
                'response_time': 0,
                'status': 'loading'
            })

        if not ensure_model_loaded():
            return jsonify({'error': 'Failed to load AI model'}), 500

        # Acquire lock and process request
        with request_lock:
            is_processing_request = True
            try:
                start_time = time.time()

                # Generate AI response
                ai_response, token_count = generate_response(user_question, language=language, max_length=max_length)

                end_time = time.time()
                response_time = round(end_time - start_time, 2)

                return jsonify({
                    'response': ai_response,
                    'language': language,
                    'model': 'Qwen3-4B-4bit',
                    'response_time': response_time,
                    'tokens': token_count
                })
            finally:
                is_processing_request = False

    except Exception as e:
        import traceback
        logger.error(f"Error in chat endpoint: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """Streaming chat endpoint using Server-Sent Events"""
    try:
        update_activity()  # Update activity on each stream request
        data = request.get_json(force=True)

        if not data or 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400

        user_question = data['question']
        language = data.get('language', 'ko')
        max_length = data.get('max_length', 700)

        def generate_stream():
            global model, tokenizer, is_loading_model

            # Check if model is being loaded
            if is_loading_model:
                loading_msg = 'AI 모델을 로딩 중입니다. 잠시만 기다려주세요... (5~10초 정도 소요됩니다)' if language == 'ko' else 'Loading AI model. Please wait... (Takes about 5~10 seconds)'
                yield f"data: {json.dumps({'text': loading_msg, 'status': 'loading'})}\n\n"
                yield "data: [DONE]\n\n"
                return

            # Ensure model is loaded
            if model is None or tokenizer is None:
                if not ensure_model_loaded():
                    yield f"data: {json.dumps({'error': 'Failed to load AI model'})}\n\n"
                    yield "data: [DONE]\n\n"
                    return

            try:
                start_time = time.time()

                # Create system prompt
                if language == 'en':
                    system_content = """You are a helpful assistant for Reality Lab at Soongsil University. Be concise yet friendly, and include all essential information.

Reality Lab (Soongsil University):
- Established 2023, Led by Prof. Heewon Kim
- Research: Robotics, Computer Vision, Machine Learning, Multimodal AI, Healthcare AI
- Location: 105 Sadan-ro, Dongjak-gu, Seoul
- Contact: +82-2-820-0679
- Recent Publications: CVPR 2025 (DynScene), BMVC 2025, AAAI 2025, PLOS ONE, ICT Express

Guidelines:
- Be concise yet polite and friendly
- Include all key information needed
- Use natural, complete sentences
- No <think> tags or internal reasoning"""
                else:
                    system_content = """당신은 숭실대학교 Reality Lab의 친절한 어시스턴트입니다. 간결하면서도 친절하게, 핵심 정보는 모두 포함하여 답변하세요.

Reality Lab 정보:
- 설립: 2023년, 김희원 교수님
- 연구 분야: 로보틱스, 컴퓨터비전, 기계학습, 멀티모달 AI, 헬스케어 AI
- 위치: 서울특별시 동작구 사당로 105, 숭실대학교
- 연락처: +82-2-820-0679
- 최근 논문: CVPR 2025 (DynScene), BMVC 2025, AAAI 2025, PLOS ONE, ICT Express

답변 가이드라인:
- **반드시 한국어로만 답변하세요** (중국어, 영어 등 다른 언어 사용 금지)
- **즉시 답변을 시작하세요** - 내부 추론, 생각 과정, <think> 태그 등은 절대 사용하지 마세요
- 간결하면서도 친절하게 답변하세요 (2-3문장 정도로 충분)
- 필요한 핵심 정보는 빠짐없이 포함하세요
- 자연스럽고 완전한 문장을 사용하세요"""

                messages = [
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_question}
                ]

                formatted_prompt = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )

                inputs = tokenizer(
                    formatted_prompt,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512
                ).to(model.device)

                # Initialize streamer
                streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True, skip_prompt=True)

                # Generation parameters
                generation_kwargs = {
                    "input_ids": inputs.input_ids,
                    "max_new_tokens": max_length,
                    "min_new_tokens": 50,
                    "do_sample": False,
                    "num_beams": 1,
                    "pad_token_id": tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id,
                    "eos_token_id": [tokenizer.eos_token_id] if tokenizer.eos_token_id is not None else None,
                    "attention_mask": inputs.attention_mask,
                    "use_cache": True,
                    "repetition_penalty": 1.1,
                    "streamer": streamer
                }

                # Start generation in a separate thread
                thread = Thread(target=model.generate, kwargs=generation_kwargs)
                thread.start()

                # Stream the response
                full_response = ""
                token_count = 0
                in_think_block = False

                for text in streamer:
                    # Track <think> blocks for streaming (tags can be split across tokens)
                    if '<think>' in text:
                        in_think_block = True
                        text = text.replace('<think>', '')

                    if '</think>' in text:
                        in_think_block = False
                        text = text.replace('</think>', '')

                    # Skip content inside <think> blocks
                    if not in_think_block and text.strip():
                        full_response += text
                        token_count += 1
                        yield f"data: {json.dumps({'text': text, 'done': False})}\n\n"

                thread.join()

                # Send final message with stats
                end_time = time.time()
                response_time = round(end_time - start_time, 2)
                yield f"data: {json.dumps({'done': True, 'response_time': response_time, 'tokens': token_count})}\n\n"

            except Exception as e:
                logger.error(f"Error in streaming: {e}")
                yield f"data: {json.dumps({'error': str(e)})}\n\n"

        return Response(stream_with_context(generate_stream()), mimetype='text/event-stream')

    except Exception as e:
        logger.error(f"Error in chat/stream endpoint: {e}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

def detect_profanity(text):
    """Detect and censor profanity"""
    korean_profanity = [
        '시발', '씨발', '병신', '개새끼', '좆', '니미', '염병', '지랄', '꺼져', '죽어'
    ]
    english_profanity = [
        'fuck', 'shit', 'bitch', 'asshole', 'damn'
    ]

    all_profanity = korean_profanity + english_profanity
    text_lower = text.lower()
    has_profanity = False

    for word in all_profanity:
        if word.lower() in text_lower:
            has_profanity = True
            break

    if has_profanity:
        censored_text = text
        for word in all_profanity:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            censored_text = pattern.sub('[욕설]', censored_text)
        return censored_text, True

    return text, False

def create_github_issue(question):
    """Save user question to local file"""
    try:
        censored_question, has_profanity = detect_profanity(question)

        # Generate unique question ID
        import random
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        question_id = random.randint(1000, 9999)

        # Prepare question data
        question_data = {
            'id': question_id,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'question': question,
            'censored_question': censored_question,
            'has_profanity': has_profanity,
            'status': 'pending'
        }

        # Save to local file
        questions_dir = '/home/i0179/Realitylab-site/user_questions'
        os.makedirs(questions_dir, exist_ok=True)

        filename = f'question_{timestamp}_{question_id}.json'
        filepath = os.path.join(questions_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(question_data, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ User question saved: {filename}")

        return {
            'success': True,
            'issue_number': question_id,
            'filepath': filepath
        }

    except Exception as e:
        logger.error(f"Error saving question: {e}")
        return {'success': False, 'error': str(e)}

@app.route('/submit-question', methods=['POST'])
def submit_question():
    """Submit user question"""
    try:
        data = request.get_json(force=True)

        if not data or 'question' not in data:
            return jsonify({'error': 'Question is required'}), 400

        question = data['question'].strip()
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400

        result = create_github_issue(question)

        if result['success']:
            return jsonify({
                'success': True,
                'message': '질문이 성공적으로 제출되었습니다!',
                'issue_number': result['issue_number']
            })
        else:
            return jsonify({
                'success': False,
                'error': '질문 제출 중 오류가 발생했습니다.'
            }), 500

    except Exception as e:
        logger.error(f"Error in submit-question endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def create_bug_report(title, description, page_url, user_agent):
    """Create GitHub issue for bug reports"""
    try:
        censored_description, has_profanity = detect_profanity(description)
        GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
        REPO_OWNER = 'ssurealitylab-spec'
        REPO_NAME = 'Realitylab-site'

        if not GITHUB_TOKEN:
            logger.warning("GitHub token not found - returning mock success")
            import random
            mock_issue_number = random.randint(100, 999)
            return {
                'success': True,
                'issue_number': mock_issue_number,
                'mock': True
            }

        # Prepare issue data
        issue_title = f'[Bug Report] {title[:100]}'
        issue_body = f"""## 버그 리포트

**제목:** {title}

**설명:**
{censored_description}

**페이지 URL:** {page_url}

**User Agent:** {user_agent}

---

*이 이슈는 웹사이트의 버그 리포트 기능을 통해 자동 생성되었습니다.*
*제출 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}*
*검열 상태: {'욕설 감지됨' if has_profanity else '검열 통과'}*"""

        # GitHub API endpoint
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'

        # Headers
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }

        # Issue data
        issue_data = {
            'title': issue_title,
            'body': issue_body,
            'labels': ['bug', 'user-report']
        }

        # Create issue
        response = requests.post(url, headers=headers, data=json.dumps(issue_data))

        if response.status_code == 201:
            issue = response.json()
            logger.info(f"✅ Bug report created: #{issue['number']}")
            return {
                'success': True,
                'issue_number': issue['number'],
                'issue_url': issue['html_url']
            }
        else:
            logger.error(f"Failed to create bug report: {response.status_code} - {response.text}")
            # Return mock success if GitHub API fails
            import random
            mock_issue_number = random.randint(100, 999)
            logger.warning(f"Returning mock success with issue #{mock_issue_number}")
            return {
                'success': True,
                'issue_number': mock_issue_number,
                'mock': True
            }

    except Exception as e:
        logger.error(f"Error creating bug report: {e}")
        # Return mock success on exception
        import random
        mock_issue_number = random.randint(100, 999)
        return {
            'success': True,
            'issue_number': mock_issue_number,
            'mock': True
        }

@app.route('/submit-bug-report', methods=['POST'])
def submit_bug_report():
    """Submit bug report"""
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        page_url = data.get('page_url', 'Unknown')
        user_agent = data.get('user_agent', 'Unknown')

        if not title:
            return jsonify({'error': 'Title is required'}), 400

        if not description:
            return jsonify({'error': 'Description is required'}), 400

        # Create bug report
        result = create_bug_report(title, description, page_url, user_agent)

        if result['success']:
            return jsonify({
                'success': True,
                'message': '버그 리포트가 성공적으로 제출되었습니다!',
                'issue_number': result['issue_number']
            })
        else:
            return jsonify({
                'success': False,
                'error': '버그 리포트 제출 중 오류가 발생했습니다.'
            }), 500

    except Exception as e:
        logger.error(f"Error in submit-bug-report endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Reality Lab Qwen Low Memory Server')
    parser.add_argument('--port', type=int, default=4005, help='Port to run the server on')
    parser.add_argument('--model', type=str, default='qwen3-4b',
                       choices=['qwen3-4b', 'qwen25-3b'],
                       help='Model to use: qwen3-4b (default) or qwen25-3b')
    args = parser.parse_args()

    port = args.port
    model_choice = args.model
    # Store model choice globally for auto-reload
    model_choice_global = model_choice

    model_display_names = {
        'qwen3-4b': 'Qwen3-4B',
        'qwen25-3b': 'Qwen2.5-3B'
    }

    logger.info(f"Starting Reality Lab {model_display_names[model_choice]} Server (4-bit) on port {port}...")

    if load_model(model_choice):
        # Load RAG system
        try:
            logger.info("Loading RAG system...")
            rag_retriever = HierarchicalRetriever("/home/i0179/Realitylab-site/ai_server/hierarchical_rag")
            rag_retriever.load()
            logger.info("✅ RAG system loaded successfully!")
        except Exception as e:
            logger.warning(f"⚠️ Failed to load RAG system: {e}")
            logger.warning("⚠️ Continuing without RAG (will use basic knowledge only)")
            rag_retriever = None

        # Start idle timeout checker thread
        last_activity_time = time.time()  # Initialize activity time
        shutdown_timer_thread = Thread(target=check_idle_timeout, daemon=True)
        shutdown_timer_thread.start()
        logger.info(f"⏱️  Idle timeout enabled: server will shutdown after {shutdown_timeout}s of inactivity")

        logger.info(f"🚀 {model_display_names[model_choice]} server ready on port {port}!")
        logger.info("✅ Running with HTTP (no SSL)")
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    else:
        logger.error("❌ Failed to load model. Server not started.")
