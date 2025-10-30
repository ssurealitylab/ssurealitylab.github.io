#!/usr/bin/env python3
"""
Reality Lab Data Crawler
Crawls YAML data files and converts them to searchable text format
"""

import yaml
import json
from pathlib import Path
from datetime import datetime

def load_yaml(filepath):
    """Load YAML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def format_members(members_data):
    """Convert members.yml to searchable text"""
    text_parts = []

    # Faculty
    if 'faculty' in members_data and isinstance(members_data['faculty'], list):
        text_parts.append("=== 교수진 (Faculty) ===\n")
        for member in members_data['faculty']:
            text_parts.append(f"\n이름: {member.get('name', '')} ({member.get('name_ko', '')})")
            if member.get('position'):
                text_parts.append(f"직책: {member.get('position', '')}")
            text_parts.append(f"이메일: {member.get('email', '')}")
            if member.get('phone'):
                text_parts.append(f"전화: {member.get('phone', '')}")
            if member.get('affiliation'):
                text_parts.append(f"소속: {member.get('affiliation', '')}")
            text_parts.append("")

    # Students
    if 'students' in members_data and isinstance(members_data['students'], dict):
        text_parts.append("\n=== 학생 연구원 (Students) ===\n")

        # MS Students
        if 'ms_students' in members_data['students']:
            text_parts.append("\n## 석사과정 (Master's Students) ##")
            for student in members_data['students']['ms_students']:
                text_parts.append(f"\n이름: {student.get('name', '')} ({student.get('name_ko', '')})")
                text_parts.append(f"이메일: {student.get('email', '')}")
                if student.get('university'):
                    text_parts.append(f"학력: {student.get('university', '')}")
                if student.get('research'):
                    text_parts.append(f"연구 분야: {student.get('research', '')}")
                text_parts.append("")

        # Interns
        if 'interns' in members_data['students']:
            text_parts.append("\n## 연구 인턴 (Research Interns) ##")
            for student in members_data['students']['interns']:
                text_parts.append(f"\n이름: {student.get('name', '')} ({student.get('name_ko', '')})")
                text_parts.append(f"이메일: {student.get('email', '')}")
                if student.get('university'):
                    text_parts.append(f"학력: {student.get('university', '')}")
                if student.get('research'):
                    text_parts.append(f"연구 분야: {student.get('research', '')}")
                text_parts.append("")

    # Alumni
    if 'alumni' in members_data and isinstance(members_data['alumni'], list):
        text_parts.append("\n=== 졸업생 (Alumni) ===\n")
        for alumnus in members_data['alumni']:
            text_parts.append(f"\n이름: {alumnus.get('name', '')} ({alumnus.get('name_ko', '')})")
            if alumnus.get('year'):
                text_parts.append(f"졸업 연도: {alumnus.get('year', '')}")
            if alumnus.get('current'):
                text_parts.append(f"현재: {alumnus.get('current', '')}")
            text_parts.append("")

    return "\n".join(text_parts)

def format_publications(publications_data):
    """Convert publications.yml to searchable text"""
    text_parts = []
    text_parts.append("=== 논문 (Publications) ===\n")

    if isinstance(publications_data, list):
        for pub in publications_data:
            if isinstance(pub, dict):
                text_parts.append(f"\n제목: {pub.get('title', '')}")
                if pub.get('title_ko'):
                    text_parts.append(f"한글 제목: {pub.get('title_ko', '')}")
                text_parts.append(f"저자: {pub.get('authors', '')}")
                text_parts.append(f"학회/저널: {pub.get('venue', '')}")
                if pub.get('year'):
                    text_parts.append(f"연도: {pub.get('year', '')}")
                if pub.get('abstract'):
                    text_parts.append(f"초록: {pub.get('abstract', '')}")
                if pub.get('award'):
                    text_parts.append(f"수상: {pub.get('award', '')}")
                text_parts.append("")

    return "\n".join(text_parts)

def format_news(news_data):
    """Convert news.yml to searchable text"""
    text_parts = []
    text_parts.append("=== 뉴스 (News) ===\n")

    if isinstance(news_data, list):
        for item in news_data:
            if isinstance(item, dict):
                text_parts.append(f"\n날짜: {item.get('date', '')}")
                text_parts.append(f"내용: {item.get('content', '')}")
                if item.get('content_ko'):
                    text_parts.append(f"한글: {item.get('content_ko', '')}")
                text_parts.append("")

    return "\n".join(text_parts)

def format_chatbot_knowledge(knowledge_data):
    """Convert chatbot_knowledge.yml to searchable text"""
    text_parts = []
    text_parts.append("=== 연구실 정보 (Lab Information) ===\n")

    if isinstance(knowledge_data, dict):
        if 'basic_info' in knowledge_data and isinstance(knowledge_data['basic_info'], dict):
            text_parts.append("\n## 기본 정보 ##")
            for key, value in knowledge_data['basic_info'].items():
                text_parts.append(f"{key}: {value}")
            text_parts.append("")

        if 'research_areas' in knowledge_data and isinstance(knowledge_data['research_areas'], list):
            text_parts.append("\n## 연구 분야 ##")
            text_parts.append(", ".join(knowledge_data['research_areas']))
            text_parts.append("")

        if 'faq' in knowledge_data and isinstance(knowledge_data['faq'], list):
            text_parts.append("\n## 자주 묻는 질문 ##")
            for faq in knowledge_data['faq']:
                if isinstance(faq, dict):
                    text_parts.append(f"\nQ: {faq.get('question', '')}")
                    text_parts.append(f"A: {faq.get('answer', '')}")
                    text_parts.append("")

    return "\n".join(text_parts)

def main():
    """Main crawler function"""
    print("🕷️  Starting Reality Lab data crawler...")

    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / "_data"
    output_dir = base_dir / "ai_server" / "crawled_data"

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    all_text = []
    metadata = {
        "crawled_at": datetime.now().isoformat(),
        "files_processed": []
    }

    # Process members.yml
    try:
        members = load_yaml(data_dir / "members.yml")
        members_text = format_members(members)
        all_text.append(members_text)
        metadata["files_processed"].append("members.yml")
        print("✅ Processed members.yml")
    except Exception as e:
        print(f"❌ Error processing members.yml: {e}")

    # Process publications.yml
    try:
        publications = load_yaml(data_dir / "publications.yml")
        publications_text = format_publications(publications)
        all_text.append(publications_text)
        metadata["files_processed"].append("publications.yml")
        print("✅ Processed publications.yml")
    except Exception as e:
        print(f"❌ Error processing publications.yml: {e}")

    # Process news.yml
    try:
        news = load_yaml(data_dir / "news.yml")
        news_text = format_news(news)
        all_text.append(news_text)
        metadata["files_processed"].append("news.yml")
        print("✅ Processed news.yml")
    except Exception as e:
        print(f"❌ Error processing news.yml: {e}")

    # Process chatbot_knowledge.yml
    try:
        knowledge = load_yaml(data_dir / "chatbot_knowledge.yml")
        knowledge_text = format_chatbot_knowledge(knowledge)
        all_text.append(knowledge_text)
        metadata["files_processed"].append("chatbot_knowledge.yml")
        print("✅ Processed chatbot_knowledge.yml")
    except Exception as e:
        print(f"❌ Error processing chatbot_knowledge.yml: {e}")

    # Combine all text
    combined_text = "\n\n" + "="*80 + "\n\n".join(all_text)

    # Save combined text
    output_file = output_dir / "knowledge_base.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_text)

    # Save metadata
    metadata_file = output_dir / "metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Crawling complete!")
    print(f"📄 Knowledge base saved to: {output_file}")
    print(f"📊 Metadata saved to: {metadata_file}")
    print(f"📏 Total text length: {len(combined_text)} characters")

if __name__ == "__main__":
    main()
