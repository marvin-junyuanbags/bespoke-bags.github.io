#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余的SEO问题 - bespoke-bags.com
"""

import os
import re
from bs4 import BeautifulSoup
import json

def generate_title_from_content(soup, file_path):
    """从内容生成标题"""
    # 尝试从H1标签获取
    h1 = soup.find('h1')
    if h1 and h1.get_text().strip():
        title = h1.get_text().strip()
        if len(title) < 60:
            return title + " | Bespoke Bags"
        return title[:57] + "..."
    
    # 从文件名生成
    filename = os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
    return f"{filename} | Bespoke Bags"

def generate_description_from_content(soup, file_path):
    """从内容生成描述"""
    # 尝试从第一个段落获取
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text = p.get_text().strip()
        if len(text) > 50:
            if len(text) > 160:
                return text[:157] + "..."
            elif len(text) < 120:
                return text + " Discover premium bespoke bags and leather goods crafted with excellence."
            return text
    
    # 默认描述
    filename = os.path.basename(file_path).replace('.html', '').replace('-', ' ')
    return f"Explore {filename} at Bespoke Bags. Premium leather goods and custom bags crafted with traditional techniques and modern innovation."

def generate_keywords_from_content(soup, file_path):
    """从内容生成关键词"""
    filename = os.path.basename(file_path).replace('.html', '').replace('-', ' ')
    base_keywords = "bespoke bags, leather goods, custom bags, premium leather, handcrafted bags"
    
    # 从文件名添加特定关键词
    if 'leather' in filename.lower():
        base_keywords += ", leather care, leather maintenance"
    if 'customer' in filename.lower():
        base_keywords += ", customer service, customer satisfaction"
    if 'carry-on' in filename.lower():
        base_keywords += ", carry-on bags, travel bags, luggage"
    
    return base_keywords

def fix_seo_issues(file_path):
    """修复单个HTML文件的SEO问题"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        # 确保有html和head标签
        if not soup.find('html'):
            # 如果没有完整的HTML结构，需要重新构建
            new_soup = BeautifulSoup('<!DOCTYPE html><html><head></head><body></body></html>', 'html.parser')
            new_soup.body.replace_with(soup)
            soup = new_soup
            modified = True
        
        head = soup.find('head')
        if not head:
            head = soup.new_tag('head')
            soup.html.insert(0, head)
            modified = True
        
        # 修复title标签
        title = soup.find('title')
        if not title or not title.get_text().strip():
            if title:
                title.decompose()
            title = soup.new_tag('title')
            title.string = generate_title_from_content(soup, file_path)
            head.insert(0, title)
            modified = True
            print(f"添加title标签: {file_path}")
        elif len(title.get_text().strip()) < 30:
            # 标题过短，需要扩展
            old_title = title.get_text().strip()
            new_title = old_title + " | Premium Bespoke Bags"
            title.string = new_title
            modified = True
            print(f"扩展标题: {file_path}")
        
        # 修复meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc or not meta_desc.get('content', '').strip():
            if meta_desc:
                meta_desc.decompose()
            meta_desc = soup.new_tag('meta')
            meta_desc['name'] = 'description'
            meta_desc['content'] = generate_description_from_content(soup, file_path)
            head.append(meta_desc)
            modified = True
            print(f"添加meta description: {file_path}")
        elif len(meta_desc.get('content', '').strip()) < 120:
            # 描述过短，需要扩展
            old_desc = meta_desc.get('content', '').strip()
            new_desc = old_desc + " Discover premium bespoke bags crafted with excellence."
            meta_desc['content'] = new_desc[:160]
            modified = True
            print(f"扩展描述: {file_path}")
        
        # 添加viewport设置
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            viewport = soup.new_tag('meta')
            viewport['name'] = 'viewport'
            viewport['content'] = 'width=device-width, initial-scale=1.0'
            head.append(viewport)
            modified = True
        
        # 添加meta keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if not keywords or not keywords.get('content', '').strip():
            if keywords:
                keywords.decompose()
            keywords = soup.new_tag('meta')
            keywords['name'] = 'keywords'
            keywords['content'] = generate_keywords_from_content(soup, file_path)
            head.append(keywords)
            modified = True
        
        # 添加canonical链接
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if not canonical:
            canonical = soup.new_tag('link')
            canonical['rel'] = 'canonical'
            # 从文件路径生成URL
            relative_path = os.path.relpath(file_path, '.').replace('\\', '/')
            canonical['href'] = f'https://bespoke-bags.com/{relative_path}'
            head.append(canonical)
            modified = True
        
        # 添加H1标签（如果缺少）
        h1_tags = soup.find_all('h1')
        if not h1_tags:
            body = soup.find('body')
            if body:
                h1 = soup.new_tag('h1')
                title_text = soup.find('title')
                if title_text:
                    h1.string = title_text.get_text().replace(' | Bespoke Bags', '').replace(' | Premium Bespoke Bags', '')
                else:
                    h1.string = generate_title_from_content(soup, file_path).replace(' | Bespoke Bags', '')
                # 在body的开始处插入H1
                if body.contents:
                    body.insert(0, h1)
                else:
                    body.append(h1)
                modified = True
                print(f"添加H1标签: {file_path}")
        
        # 添加Open Graph标签
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        if not og_title:
            og_title = soup.new_tag('meta')
            og_title['property'] = 'og:title'
            title_tag = soup.find('title')
            og_title['content'] = title_tag.get_text() if title_tag else generate_title_from_content(soup, file_path)
            head.append(og_title)
            modified = True
        
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if not og_desc:
            og_desc = soup.new_tag('meta')
            og_desc['property'] = 'og:description'
            meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
            og_desc['content'] = meta_desc_tag.get('content') if meta_desc_tag else generate_description_from_content(soup, file_path)
            head.append(og_desc)
            modified = True
        
        og_url = soup.find('meta', attrs={'property': 'og:url'})
        if not og_url:
            og_url = soup.new_tag('meta')
            og_url['property'] = 'og:url'
            relative_path = os.path.relpath(file_path, '.').replace('\\', '/')
            og_url['content'] = f'https://bespoke-bags.com/{relative_path}'
            head.append(og_url)
            modified = True
        
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        if not og_image:
            og_image = soup.new_tag('meta')
            og_image['property'] = 'og:image'
            og_image['content'] = 'https://bespoke-bags.com/images/bespoke-bags-og-image.jpg'
            head.append(og_image)
            modified = True
        
        # 添加Twitter Card标签
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        if not twitter_card:
            twitter_card = soup.new_tag('meta')
            twitter_card['name'] = 'twitter:card'
            twitter_card['content'] = 'summary_large_image'
            head.append(twitter_card)
            modified = True
        
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if not twitter_title:
            twitter_title = soup.new_tag('meta')
            twitter_title['name'] = 'twitter:title'
            title_tag = soup.find('title')
            twitter_title['content'] = title_tag.get_text() if title_tag else generate_title_from_content(soup, file_path)
            head.append(twitter_title)
            modified = True
        
        twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
        if not twitter_desc:
            twitter_desc = soup.new_tag('meta')
            twitter_desc['name'] = 'twitter:description'
            meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
            twitter_desc['content'] = meta_desc_tag.get('content') if meta_desc_tag else generate_description_from_content(soup, file_path)
            head.append(twitter_desc)
            modified = True
        
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if not twitter_image:
            twitter_image = soup.new_tag('meta')
            twitter_image['name'] = 'twitter:image'
            twitter_image['content'] = 'https://bespoke-bags.com/images/bespoke-bags-twitter-image.jpg'
            head.append(twitter_image)
            modified = True
        
        # 添加JSON-LD结构化数据
        json_ld = soup.find('script', attrs={'type': 'application/ld+json'})
        if not json_ld:
            json_ld = soup.new_tag('script')
            json_ld['type'] = 'application/ld+json'
            
            title_tag = soup.find('title')
            meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
            
            structured_data = {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": title_tag.get_text() if title_tag else generate_title_from_content(soup, file_path),
                "description": meta_desc_tag.get('content') if meta_desc_tag else generate_description_from_content(soup, file_path),
                "url": f"https://bespoke-bags.com/{os.path.relpath(file_path, '.').replace(chr(92), '/')}",
                "publisher": {
                    "@type": "Organization",
                    "name": "Bespoke Bags",
                    "url": "https://bespoke-bags.com"
                }
            }
            
            json_ld.string = json.dumps(structured_data, ensure_ascii=False, indent=2)
            head.append(json_ld)
            modified = True
        
        # 保存修改后的文件
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True
        
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return False
    
    return False

def main():
    """主函数"""
    website_dir = '.'
    fixed_files = 0
    total_files = 0
    
    print("开始修复 bespoke-bags.com 网站的剩余SEO问题...")
    print("=" * 50)
    
    # 遍历所有HTML文件
    for root, dirs, files in os.walk(website_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                total_files += 1
                
                if fix_seo_issues(file_path):
                    fixed_files += 1
    
    print(f"\n修复完成！")
    print(f"总处理文件数: {total_files}")
    print(f"修复的文件数: {fixed_files}")

if __name__ == '__main__':
    main()