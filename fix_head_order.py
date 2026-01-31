#!/usr/bin/env python3
import os
import re
from pathlib import Path

def reorganize_head_correct(content):
    """head 섹션: 메타(모두) → 타이틀 → 스크립트/링크"""
    
    head_match = re.search(r'<head>(.*?)</head>', content, re.DOTALL)
    if not head_match:
        return content
    
    head_content = head_match.group(1)
    
    # 모든 메타 태그 추출
    metas = re.findall(r'<meta[^>]*/?>', head_content)
    
    # 타이틀
    title_match = re.search(r'<title>[^<]*</title>', head_content)
    title = title_match.group(0) if title_match else None
    
    # GA 스크립트
    ga_script_match = re.search(r'<script\s+async\s+src="https://www\.googletagmanager\.com[^>]*></script>', head_content)
    ga_script = ga_script_match.group(0) if ga_script_match else None
    
    # GA 설정 스크립트
    ga_config_match = re.search(r'<script>\s*window\.dataLayer[^<]*</script>', head_content, re.DOTALL)
    ga_config = ga_config_match.group(0) if ga_config_match else None
    
    # jQuery 스크립트
    jquery_match = re.search(r'<script\s+src="/dev-tools/assets/dist/js/jquery[^>]*></script>', head_content)
    jquery = jquery_match.group(0) if jquery_match else None
    
    # 링크들
    links = re.findall(r'<link[^>]*/?>', head_content)
    
    # 새로운 head 구성
    new_head = '\n    <!-- ====== Online Tools Cafe 공통 head 시작 ====== -->\n'
    
    # 1. 모든 메타 태그
    for meta in metas:
        new_head += meta + '\n'
    
    # 2. 타이틀
    if title:
        new_head += title + '\n'
    
    # 3. GA 스크립트들
    if ga_script:
        new_head += ga_script + '\n'
    if ga_config:
        new_head += ga_config + '\n'
    
    # 4. jQuery 스크립트
    if jquery:
        new_head += jquery + '\n'
    
    # 5. 모든 링크
    for link in links:
        new_head += link + '\n'
    
    new_head += '    <!-- ====== Online Tools Cafe 공통 head 끝 (각 도구 페이지에도 복사) ====== -->'
    
    content = content[:head_match.start(1)] + new_head + content[head_match.end(1):]
    
    return content

def process_html_files():
    """tools 디렉토리의 모든 HTML 파일 처리"""
    tools_dir = Path("c:/themoka7/dev-tools/tools")
    
    html_files = list(tools_dir.rglob("*.html"))
    
    print(f"Fixing head organization for {len(html_files)} files...\n")
    
    for file_path in sorted(html_files):
        if file_path.name == "template.html":
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = reorganize_head_correct(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ {file_path.relative_to(tools_dir.parent)}")
        
        except Exception as e:
            print(f"✗ {file_path.name}: {e}")

if __name__ == "__main__":
    process_html_files()
    print("\nDone!")
