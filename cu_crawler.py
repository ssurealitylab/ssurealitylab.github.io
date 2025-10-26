#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CU 편의점 제품 정보 크롤러
모든 제품의 상품명, 가격, 설명, 태그 등을 수집하여 CSV로 저장
"""

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
import re
from typing import List, Dict
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CUCrawler:
    def __init__(self):
        self.base_url = "https://cu.bgfretail.com"
        self.ajax_url = f"{self.base_url}/product/searchAjax.do"
        self.detail_url = f"{self.base_url}/product/view.do"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': f'{self.base_url}/product/search.do'
        })

    def get_product_ids(self) -> List[int]:
        """AJAX API를 통해 모든 제품 ID 수집"""
        product_ids = []
        page = 1

        logger.info("제품 ID 수집 시작...")

        while True:
            try:
                # AJAX 요청
                data = {
                    'pageIndex': str(page),
                    'listType': '1'
                }

                response = self.session.post(self.ajax_url, data=data)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.select('li.prod_list')

                if not items:
                    logger.info(f"페이지 {page}에서 더 이상 제품이 없습니다.")
                    break

                # 제품 ID 추출 (javascript:view(ID) 형태)
                for item in items:
                    link = item.select_one('a.prod_item')
                    if link and 'href' in link.attrs:
                        match = re.search(r'view\((\d+)\)', link['href'])
                        if match:
                            product_id = int(match.group(1))
                            product_ids.append(product_id)

                logger.info(f"페이지 {page}: {len(items)}개 제품 발견 (총 {len(product_ids)}개)")
                page += 1

                # 서버 부하 방지
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"페이지 {page} 수집 중 오류: {e}")
                break

        logger.info(f"총 {len(product_ids)}개 제품 ID 수집 완료")
        return product_ids

    def get_product_detail(self, product_id: int) -> Dict:
        """제품 상세 정보 추출"""
        try:
            params = {
                'category': 'event',
                'gdIdx': product_id
            }

            response = self.session.get(self.detail_url, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 제품명
            name_elem = soup.select_one('p.tit')
            name = name_elem.get_text(strip=True) if name_elem else ''

            # 가격
            price_elem = soup.select_one('.prodPrice span')
            price = price_elem.get_text(strip=True) if price_elem else ''

            # 상품 설명
            description_elems = soup.select('.prodExplain li')
            description = ' '.join([elem.get_text(strip=True) for elem in description_elems])

            # 태그
            tag_elems = soup.select('ul.prodTag#taglist li')
            tags = [tag.get_text(strip=True) for tag in tag_elems if tag.get_text(strip=True)]
            tags_str = ', '.join(tags)

            # 이벤트/배지 정보
            badge_elem = soup.select_one('.badge')
            badge = ''
            if badge_elem:
                if 'plus2' in badge_elem.get('class', []):
                    badge = '2+1'
                elif 'plus1' in badge_elem.get('class', []):
                    badge = '1+1'

            # 카테고리
            category_elem = soup.select_one('.category')
            category = category_elem.get_text(strip=True) if category_elem else ''

            # 이미지 URL
            image_elem = soup.select_one('.prodDetail-w img')
            image_url = ''
            if image_elem and 'src' in image_elem.attrs:
                image_url = image_elem['src']
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url

            return {
                'product_id': product_id,
                'name': name,
                'price': price,
                'description': description,
                'tags': tags_str,
                'badge': badge,
                'category': category,
                'image_url': image_url
            }

        except Exception as e:
            logger.error(f"제품 {product_id} 상세 정보 수집 중 오류: {e}")
            return {
                'product_id': product_id,
                'name': '',
                'price': '',
                'description': '',
                'tags': '',
                'badge': '',
                'category': '',
                'image_url': ''
            }

    def crawl_all_products(self, output_file: str = 'cu_products'):
        """모든 제품 정보를 수집하여 CSV와 Excel로 저장"""
        # 1단계: 모든 제품 ID 수집
        product_ids = self.get_product_ids()

        if not product_ids:
            logger.error("제품 ID를 찾을 수 없습니다.")
            return

        # 2단계: 각 제품 상세 정보 수집
        logger.info(f"\n제품 상세 정보 수집 시작... (총 {len(product_ids)}개)")

        products = []
        for idx, product_id in enumerate(product_ids, 1):
            product = self.get_product_detail(product_id)
            products.append(product)

            if idx % 50 == 0:
                logger.info(f"진행률: {idx}/{len(product_ids)} ({idx/len(product_ids)*100:.1f}%)")

            # 서버 부하 방지
            time.sleep(0.3)

        # 3단계: CSV 저장
        csv_file = f"{output_file}.csv"
        logger.info(f"\nCSV 파일 저장 중: {csv_file}")

        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['product_id', 'name', 'price', 'description', 'tags', 'badge', 'category', 'image_url']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(products)

        logger.info(f"✓ CSV 저장 완료: {csv_file}")

        # 4단계: Excel 저장
        excel_file = f"{output_file}.xlsx"
        logger.info(f"\nExcel 파일 저장 중: {excel_file}")

        df = pd.DataFrame(products)
        df.to_excel(excel_file, index=False, engine='openpyxl')

        logger.info(f"✓ Excel 저장 완료: {excel_file}")
        logger.info(f"\n✓ 모든 작업 완료! {len(products)}개 제품 정보가 저장되었습니다.")


def main():
    crawler = CUCrawler()
    crawler.crawl_all_products('cu_products')


if __name__ == '__main__':
    main()
