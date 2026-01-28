from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

OUTPUT = "python_job/data/trends.json"
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

COUNTRIES = ['KR', 'US', 'JP', 'GB', 'DE', 'FR', 'IN', 'BR', 'CA', 'AU', 'IT', 'ES', 'MX']


def extract_trend_data(full_text):
    """Google Trends HTML에서 트렌드 데이터 추출"""
    # 검색어 추출 (숫자 앞까지, "검색" 단어 제거)
    keyword_match = re.search(r'^(.+?)\s*(?:검색|Searches)?\s*(\d+)', full_text)
    keyword = keyword_match.group(1).strip() if keyword_match else ''
    keyword = keyword.replace('검색', '').strip()  # "검색" 제거
    
    # 검색량 추출 (K, M, B, 천, 만 단위 처리)
    # KR: "5천+", US: "100K+"
    volume_match = re.search(r'(\d+)(천|만|K|M|B)?', full_text)
    volume_num = 0
    if volume_match:
        num = int(volume_match.group(1))
        unit = volume_match.group(2)
        
        if unit in ['K', '천']:
            volume_num = num * 1000
        elif unit in ['M', '만']:
            volume_num = num * 1000000 if unit == '만' else num * 1000000  # M은 백만
        elif unit == 'B':
            volume_num = num * 1000000000
        else:
            volume_num = num
    
    # 시작일 추출
    time_match = re.search(r'(\d+)\s*(?:h|hr|시간|hour|時間|小時)', full_text)
    start_time = f"~{time_match.group(1)}" if time_match else ''
    
    # 분석 결과
    if 'trending' in full_text:
        analysis = 'trending_up'
    elif 'timelapse' in full_text:
        analysis = 'timelapse'
    else:
        analysis = ''
    
    return {
        'trend': keyword,
        'search_volume': volume_num if volume_num > 0 else '',
        'start_date': start_time,
        'analysis': analysis
    }


def scrape_trends(country):
    """Google Trends에서 국가별 트렌드 수집"""
    url = "https://trends.google.co.kr/trending?geo=KR&sort=search-volume" if country == 'KR' \
        else f"https://trends.google.com/trending?geo={country}&sort=search-volume"
    
    print(f"\n[{country}] 수집 중...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()
    
    soup = BeautifulSoup(html, 'html.parser')
    trends = []
    
    for row in soup.find_all('tr'):
        cols = row.find_all('td')
        if cols and len(cols) >= 2:
            full_text = cols[1].get_text(strip=True)
            trend_data = extract_trend_data(full_text)
            
            if trend_data['trend'] and len(trend_data['trend']) > 1:
                trends.append(trend_data)
                print(f"  {len(trends)}. {trend_data['trend']} | {trend_data['search_volume']} | {trend_data['start_date']}")
    
    return trends


# 메인
all_data = {}
for country in COUNTRIES:
    try:
        all_data[country] = scrape_trends(country)
        print(f"[{country}] {len(all_data[country])}개 완료")
    except Exception as e:
        print(f"[{country}] 에러: {e}")
        all_data[country] = []

# 타임스탐프와 함께 저장
output_data = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "data": all_data
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"\n저장 완료: {OUTPUT}")
print(f"데이터: {', '.join([f'{k}({len(v)}개)' for k, v in all_data.items()])}")
