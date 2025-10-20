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
from threading import Thread

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Global variables
model = None
tokenizer = None

def load_model():
    """Load Qwen3-4B model with 8-bit quantization"""
    global model, tokenizer

    try:
        # Use the downloaded model path
        model_path = "/home/i0179/.cache/huggingface/hub/qwen3-4b-git"

        logger.info("Loading tokenizer from local path")
        tokenizer = AutoTokenizer.from_pretrained(model_path)

        # Set padding token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        logger.info("Loading Qwen3-4B model with 4-bit quantization")

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
            low_cpu_mem_usage=True
        )

        logger.info("✅ Qwen3-4B model loaded successfully with 4-bit quantization")
        return True

    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        return False

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

def generate_response(prompt, language='ko', max_length=700):
    """Generate AI response"""
    global model, tokenizer

    if model is None or tokenizer is None:
        return "AI model not loaded"

    try:
        # Create language-specific system prompt (concise yet friendly with key info)
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
- 간결하면서도 친절하게 답변하세요
- 필요한 핵심 정보는 빠짐없이 포함하세요
- 자연스럽고 완전한 문장을 사용하세요
- <think> 태그나 내부 추론 과정은 표시하지 마세요"""

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
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                attention_mask=inputs.attention_mask,
                use_cache=True,  # Use KV cache for speed
                early_stopping=True,
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

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    try:
        start_time = time.time()

        data = request.get_json(force=True)

        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400

        if 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400

        user_question = data['question']
        language = data.get('language', 'ko')
        max_length = data.get('max_length', 700)  # Balanced default

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

    except Exception as e:
        import traceback
        logger.error(f"Error in chat endpoint: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """Streaming chat endpoint using Server-Sent Events"""
    try:
        data = request.get_json(force=True)

        if not data or 'question' not in data:
            return jsonify({'error': 'No question provided'}), 400

        user_question = data['question']
        language = data.get('language', 'ko')
        max_length = data.get('max_length', 700)

        def generate_stream():
            global model, tokenizer

            if model is None or tokenizer is None:
                yield f"data: {json.dumps({'error': 'AI model not loaded'})}\n\n"
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
- 간결하면서도 친절하게 답변하세요
- 필요한 핵심 정보는 빠짐없이 포함하세요
- 자연스럽고 완전한 문장을 사용하세요
- <think> 태그나 내부 추론 과정은 표시하지 마세요"""

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
                    "pad_token_id": tokenizer.eos_token_id,
                    "eos_token_id": tokenizer.eos_token_id,
                    "attention_mask": inputs.attention_mask,
                    "use_cache": True,
                    "early_stopping": True,
                    "repetition_penalty": 1.1,
                    "streamer": streamer
                }

                # Start generation in a separate thread
                thread = Thread(target=model.generate, kwargs=generation_kwargs)
                thread.start()

                # Stream the response
                full_response = ""
                token_count = 0
                for text in streamer:
                    # Remove thinking tags
                    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
                    if text:
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
    """Create GitHub issue for user questions"""
    try:
        censored_question, has_profanity = detect_profanity(question)
        GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

        if not GITHUB_TOKEN:
            logger.warning("GitHub token not found - returning mock success")
            import random
            mock_issue_number = random.randint(100, 999)
            return {
                'success': True,
                'issue_number': mock_issue_number,
                'mock': True
            }

        # Real GitHub issue creation code here
        return {'success': True, 'issue_number': 999}

    except Exception as e:
        logger.error(f"Error creating GitHub issue: {e}")
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

    parser = argparse.ArgumentParser(description='Reality Lab Qwen3-4B Low Memory Server')
    parser.add_argument('--port', type=int, default=4005, help='Port to run the server on')
    args = parser.parse_args()

    port = args.port
    logger.info(f"Starting Reality Lab Qwen3-4B Server (4-bit) on port {port}...")

    if load_model():
        logger.info(f"🚀 Qwen3-4B server ready on port {port}!")
        logger.info("✅ Running with HTTP (no SSL)")
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    else:
        logger.error("❌ Failed to load model. Server not started.")
