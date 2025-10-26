#!/usr/bin/env python3
"""
Reality Lab Website Crawler for RAG Knowledge Base
Crawls the entire website and extracts structured information
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict, Any
from datetime import datetime
import time

class RealityLabCrawler:
    def __init__(self, base_url: str = "https://ssurealitylab.github.io/Realitylab-site"):
        self.base_url = base_url.rstrip('/')
        self.documents = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RealityLabRAGBot/1.0'
        })

    def fetch_page(self, path: str) -> BeautifulSoup:
        """Fetch and parse a page"""
        url = f"{self.base_url}/{path}"
        print(f"Fetching: {url}")
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"  Error fetching {url}: {e}")
            return None

    def add_document(self, content: str, metadata: Dict[str, Any]):
        """Add a document to the knowledge base"""
        if content.strip():
            self.documents.append({
                "content": content.strip(),
                "metadata": metadata
            })

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep Korean, English, numbers, and basic punctuation
        text = re.sub(r'[^\w\s가-힣.,!?@\-:/()\[\]&+]', '', text)
        return text.strip()

    def crawl_home_page(self):
        """Crawl home page for lab info"""
        print("\n=== Crawling Home Page ===")
        soup = self.fetch_page("")
        if not soup:
            return

        # Extract lab mission/vision from hero section
        hero = soup.find('header', class_='masthead')
        if hero:
            title = hero.find('div', class_='intro-text')
            if title:
                mission_text = self.clean_text(title.get_text())
                self.add_document(mission_text, {
                    "type": "lab_info",
                    "source": "home",
                    "category": "mission",
                    "language": "ko"
                })

        # Extract research areas
        research_section = soup.find('section', id='services')
        if research_section:
            areas = research_section.find_all('div', class_='service-heading')
            for area in areas:
                area_text = self.clean_text(area.get_text())
                if area_text:
                    self.add_document(f"연구 분야: {area_text}", {
                        "type": "research_area",
                        "source": "home",
                        "language": "ko"
                    })

    def crawl_news(self):
        """Crawl news page"""
        print("\n=== Crawling News Page ===")
        soup = self.fetch_page("news.html")
        if not soup:
            return

        news_cards = soup.find_all('div', class_='news-card')
        for card in news_cards:
            title_elem = card.find('h5', class_='card-title')
            subtitle_elem = card.find('p', class_='card-subtitle')
            text_elem = card.find('p', class_='card-text')
            date_elem = card.find('small', class_='text-muted')

            if title_elem:
                title = self.clean_text(title_elem.get_text())
                subtitle = self.clean_text(subtitle_elem.get_text()) if subtitle_elem else ""
                text = self.clean_text(text_elem.get_text()) if text_elem else ""
                date = self.clean_text(date_elem.get_text()) if date_elem else ""

                content = f"뉴스: {title}\n"
                if subtitle:
                    content += f"참여자: {subtitle}\n"
                if text:
                    content += f"내용: {text}\n"
                if date:
                    content += f"날짜: {date}"

                self.add_document(content, {
                    "type": "news",
                    "source": "news",
                    "title": title,
                    "language": "ko"
                })

    def crawl_faculty(self):
        """Crawl faculty page"""
        print("\n=== Crawling Faculty Page ===")
        soup = self.fetch_page("faculty.html")
        if not soup:
            return

        # Faculty page uses different structure
        faculty_info = soup.find('div', class_='member-info')
        if faculty_info:
            name_elem = faculty_info.find('h3', class_='member-name')
            name_ko_elem = faculty_info.find('p', class_='member-name-ko')
            position_elem = faculty_info.find('p', class_='member-position')
            affiliation_elem = faculty_info.find('p', class_='member-affiliation')
            email_elem = faculty_info.find('p', class_='member-email')
            phone_elem = faculty_info.find('p', class_='member-contact')

            if name_elem:
                name = self.clean_text(name_elem.get_text())
                name_ko = self.clean_text(name_ko_elem.get_text()) if name_ko_elem else ""
                position = self.clean_text(position_elem.get_text()) if position_elem else ""
                affiliation = self.clean_text(affiliation_elem.get_text()) if affiliation_elem else ""

                # Extract email text from span
                email = ""
                if email_elem:
                    email_span = email_elem.find('span')
                    email = self.clean_text(email_span.get_text()) if email_span else self.clean_text(email_elem.get_text())

                # Extract phone from contact
                phone = ""
                if phone_elem:
                    phone = self.clean_text(phone_elem.get_text())

                # Create both Korean and English versions
                content_ko = f"교수: {name_ko} ({name})\n"
                if position:
                    content_ko += f"직책: {position}\n"
                if affiliation:
                    content_ko += f"소속: {affiliation}\n"
                if email:
                    content_ko += f"이메일: {email}\n"
                if phone:
                    content_ko += f"전화: {phone}"

                self.add_document(content_ko, {
                    "type": "faculty",
                    "source": "faculty",
                    "name": name,
                    "language": "ko"
                })

                # Also add English version for better search
                content_en = f"Professor: {name}\n"
                if position:
                    content_en += f"Position: {position}\n"
                if email:
                    content_en += f"Email: {email}\n"
                if phone:
                    content_en += f"Phone: {phone}"

                self.add_document(content_en, {
                    "type": "faculty",
                    "source": "faculty",
                    "name": name,
                    "language": "en"
                })

    def crawl_students(self):
        """Crawl students page"""
        print("\n=== Crawling Students Page ===")
        soup = self.fetch_page("students.html")
        if not soup:
            return

        # Count students by section
        ms_students = []
        interns = []

        # Find Master's Students section
        sections = soup.find_all('h2')
        current_section = None

        for section in sections:
            section_title = self.clean_text(section.get_text())
            if "Master" in section_title or "석사" in section_title:
                current_section = "ms"
                # Find student cards after this section
                next_elem = section.find_next('div', class_='members-grid')
                if next_elem:
                    cards = next_elem.find_all('div', class_='member-card')
                    for card in cards:
                        name_elem = card.find('h3', class_='member-name')
                        if name_elem:
                            ms_students.append(self.clean_text(name_elem.get_text()))
            elif "Intern" in section_title or "인턴" in section_title:
                current_section = "intern"
                next_elem = section.find_next('div', class_='members-grid')
                if next_elem:
                    cards = next_elem.find_all('div', class_='member-card')
                    for card in cards:
                        name_elem = card.find('h3', class_='member-name')
                        if name_elem:
                            interns.append(self.clean_text(name_elem.get_text()))

        # Add summary document (Q&A style for better RAG matching)
        total_students = len(ms_students) + len(interns)
        summary_ko = f"""Reality Lab의 연구원은 총 {total_students}명입니다.

현재 연구실 구성원:
- 석사과정 학생: {len(ms_students)}명
- 연구 인턴: {len(interns)}명

석사과정 학생 수는 {len(ms_students)}명이고, 연구 인턴 수는 {len(interns)}명입니다.
학생 수를 포함하여 전체 연구원은 {total_students}명입니다.

석사과정 학생 명단: {', '.join(ms_students)}
연구 인턴 명단: {', '.join(interns)}"""

        self.add_document(summary_ko, {
            "type": "members_summary",
            "source": "students",
            "total": total_students,
            "ms_count": len(ms_students),
            "intern_count": len(interns),
            "language": "ko"
        })

        # Also add English version
        summary_en = f"""Reality Lab has a total of {total_students} researchers.

Current lab members:
- Master's Students: {len(ms_students)} members
- Research Interns: {len(interns)} members

The number of Master's students is {len(ms_students)}, and the number of research interns is {len(interns)}.
Including all students, the total number of researchers is {total_students}.

Master's Students: {', '.join(ms_students)}
Research Interns: {', '.join(interns)}"""

        self.add_document(summary_en, {
            "type": "members_summary",
            "source": "students",
            "total": total_students,
            "ms_count": len(ms_students),
            "intern_count": len(interns),
            "language": "en"
        })

        # Now add individual student cards
        student_cards = soup.find_all('div', class_='member-card')
        for card in student_cards:
            name_elem = card.find('h3', class_='member-name')
            email_elem = card.find('p', class_='member-email')
            research_elem = card.find('p', class_='member-research')

            if name_elem:
                name = self.clean_text(name_elem.get_text())
                email = self.clean_text(email_elem.get_text()) if email_elem else ""
                research = self.clean_text(research_elem.get_text()) if research_elem else ""

                content = f"학생: {name}\n"
                if email:
                    content += f"이메일: {email}\n"
                if research:
                    content += f"연구분야: {research}"

                self.add_document(content, {
                    "type": "student",
                    "source": "students",
                    "name": name,
                    "language": "ko"
                })

    def crawl_alumni(self):
        """Crawl alumni page"""
        print("\n=== Crawling Alumni Page ===")
        soup = self.fetch_page("alumni.html")
        if not soup:
            return

        # Count alumni
        alumni_names = []
        alumni_cards = soup.find_all('div', class_='member-card')

        for card in alumni_cards:
            name_elem = card.find('h3', class_='member-name')
            if name_elem:
                alumni_names.append(self.clean_text(name_elem.get_text()))

        # Add summary document (Q&A style for better RAG matching)
        if alumni_names:
            summary_ko = f"""Reality Lab의 졸업생(Alumni)은 총 {len(alumni_names)}명입니다.

연구실을 졸업한 학생 수는 {len(alumni_names)}명이며, 이들은 다양한 분야에서 활동하고 있습니다.

졸업생 명단: {', '.join(alumni_names)}"""

            self.add_document(summary_ko, {
                "type": "alumni_summary",
                "source": "alumni",
                "total": len(alumni_names),
                "language": "ko"
            })

            summary_en = f"""Reality Lab has a total of {len(alumni_names)} alumni.

The number of graduated students is {len(alumni_names)}, and they are active in various fields.

Alumni: {', '.join(alumni_names)}"""

            self.add_document(summary_en, {
                "type": "alumni_summary",
                "source": "alumni",
                "total": len(alumni_names),
                "language": "en"
            })

        # Add individual alumni details
        for card in alumni_cards:
            name_elem = card.find('h3', class_='member-name')
            university_elem = card.find('p', class_='member-university')
            period_elem = card.find('p', class_='member-period')

            if name_elem:
                name = self.clean_text(name_elem.get_text())
                university = self.clean_text(university_elem.get_text()) if university_elem else ""
                period = self.clean_text(period_elem.get_text()) if period_elem else ""

                content = f"졸업생: {name}\n"
                if university:
                    content += f"소속: {university}\n"
                if period:
                    content += f"기간: {period}"

                self.add_document(content, {
                    "type": "alumni",
                    "source": "alumni",
                    "name": name,
                    "language": "ko"
                })

    def crawl_publications(self, page_name: str, pub_type: str):
        """Crawl publications page (international or domestic)"""
        print(f"\n=== Crawling {pub_type.upper()} Publications ===")
        soup = self.fetch_page(page_name)
        if not soup:
            return

        # Try publication list items
        pub_items = soup.find_all('div', class_='publication-list-item')
        for item in pub_items:
            title_elem = item.find('h5', class_='list-title')
            authors_elem = item.find('p', class_='list-authors')
            venue_elem = item.find('div', class_='publication-badge')

            if title_elem:
                title = self.clean_text(title_elem.get_text())
                authors = self.clean_text(authors_elem.get_text()) if authors_elem else ""
                venue = self.clean_text(venue_elem.get_text()) if venue_elem else ""

                content = f"논문: {title}\n"
                if authors:
                    content += f"저자: {authors}\n"
                if venue:
                    content += f"학회: {venue}"

                self.add_document(content, {
                    "type": "publication",
                    "source": pub_type,
                    "title": title,
                    "language": "ko"
                })

    def crawl_courses(self):
        """Crawl courses page"""
        print("\n=== Crawling Courses Page ===")
        soup = self.fetch_page("courses.html")
        if not soup:
            return

        course_items = soup.find_all('div', class_='course-item')
        if not course_items:
            # Try alternative structure
            course_items = soup.find_all('div', class_='col-lg-4')

        for item in course_items:
            title_elem = item.find(['h3', 'h4', 'h5'])
            desc_elem = item.find('p')

            if title_elem:
                title = self.clean_text(title_elem.get_text())
                desc = self.clean_text(desc_elem.get_text()) if desc_elem else ""

                content = f"과목: {title}\n"
                if desc:
                    content += f"설명: {desc}"

                self.add_document(content, {
                    "type": "course",
                    "source": "courses",
                    "title": title,
                    "language": "ko"
                })

    def crawl_all(self):
        """Crawl all pages"""
        print("\n" + "="*60)
        print("Starting Reality Lab Website Crawl")
        print(f"Base URL: {self.base_url}")
        print("="*60)

        self.crawl_home_page()
        time.sleep(1)

        self.crawl_news()
        time.sleep(1)

        self.crawl_faculty()
        time.sleep(1)

        self.crawl_students()
        time.sleep(1)

        self.crawl_alumni()
        time.sleep(1)

        self.crawl_publications("international.html", "international")
        time.sleep(1)

        self.crawl_publications("domestic.html", "domestic")
        time.sleep(1)

        self.crawl_courses()

        print("\n" + "="*60)
        print(f"Crawl Complete! Total documents: {len(self.documents)}")
        print("="*60)

    def save(self, output_file: str):
        """Save documents to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(self.documents)} documents to: {output_file}")


def main():
    crawler = RealityLabCrawler()
    crawler.crawl_all()

    # Save to knowledge_base.json
    output_file = "/home/i0179/Realitylab-site/ai_server/knowledge_base.json"
    crawler.save(output_file)

    print("\n✅ Knowledge base updated successfully!")
    print(f"   File: {output_file}")
    print(f"   Documents: {len(crawler.documents)}")


if __name__ == "__main__":
    main()
