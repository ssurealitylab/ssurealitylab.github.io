#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CU 크롤러 테스트 스크립트 (처음 10개 제품만)
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_crawler():
    base_url = "https://cu.bgfretail.com"
    ajax_url = f"{base_url}/product/searchAjax.do"
    detail_url = f"{base_url}/product/view.do"

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'{base_url}/product/search.do'
    })

    # 1. 첫 페이지에서 10개 제품 ID 가져오기
    logger.info("첫 페이지 제품 ID 수집 중...")

    data = {'pageIndex': '1', 'listType': '1'}
    response = session.post(ajax_url, data=data)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('li.prod_list')

    product_ids = []
    for item in items[:10]:  # 처음 10개만
        link = item.select_one('a.prod_item')
        if link and 'href' in link.attrs:
            match = re.search(r'view\((\d+)\)', link['href'])
            if match:
                product_ids.append(int(match.group(1)))

    logger.info(f"{len(product_ids)}개 제품 ID 수집 완료: {product_ids}")

    # 2. 각 제품 상세 정보 수집
    products = []
    for idx, product_id in enumerate(product_ids, 1):
        logger.info(f"제품 {idx}/{len(product_ids)}: ID={product_id} 수집 중...")

        params = {'category': 'event', 'gdIdx': product_id}
        response = session.get(detail_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 제품명
        name_elem = soup.select_one('p.tit')
        name = name_elem.get_text(strip=True) if name_elem else ''

        # 가격
        price_elem = soup.select_one('.prodPrice span')
        price = price_elem.get_text(strip=True) if price_elem else ''

        # 설명
        description_elems = soup.select('.prodExplain li')
        description = ' '.join([elem.get_text(strip=True) for elem in description_elems])

        # 태그
        tag_elems = soup.select('ul.prodTag#taglist li')
        tags = [tag.get_text(strip=True) for tag in tag_elems if tag.get_text(strip=True)]
        tags_str = ', '.join(tags)

        product = {
            'product_id': product_id,
            'name': name,
            'price': price,
            'description': description,
            'tags': tags_str
        }
        products.append(product)

        logger.info(f"  상품명: {name}")
        logger.info(f"  가격: {price}원")
        logger.info(f"  태그: {tags_str}")

        time.sleep(0.5)

    # 3. CSV 저장
    output_file = 'cu_products_test.csv'
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['product_id', 'name', 'price', 'description', 'tags']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    logger.info(f"\n✓ 테스트 완료! {len(products)}개 제품이 {output_file}에 저장되었습니다.")


if __name__ == '__main__':
    test_crawler()
