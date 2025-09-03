#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复不完整的HTML文件 - bespoke-bags.com
"""

import os
from bs4 import BeautifulSoup

def fix_incomplete_html():
    """修复不完整的HTML文件"""
    
    # 需要修复的文件列表
    problem_files = [
        './blog/customer-service-excellence.html',
        './blog/luxury-cosmetic-bags-guide-2024.html', 
        './blog/professional-laptop-bags-guide-2024-part2.html',
        './products/carry-on-bags.html'
    ]
    
    fixed_count = 0
    
    print("开始修复不完整的HTML文件...")
    print("=" * 50)
    
    for file_path in problem_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            modified = False
            
            # 检查是否缺少body标签
            body = soup.find('body')
            if not body:
                # 创建完整的HTML结构
                html_tag = soup.find('html')
                if html_tag:
                    # 添加body标签
                    body = soup.new_tag('body')
                    html_tag.append(body)
                    modified = True
                    print(f"添加body标签: {file_path}")
            
            # 检查是否缺少H1标签
            h1_tags = soup.find_all('h1')
            if not h1_tags and body:
                # 创建H1标签
                h1 = soup.new_tag('h1')
                
                # 从title获取H1内容
                title_tag = soup.find('title')
                if title_tag and title_tag.get_text().strip():
                    h1_text = title_tag.get_text().strip()
                    # 移除品牌后缀
                    h1_text = h1_text.replace(' | Premium Travel Bags | Bespoke Bags', '')
                    h1_text = h1_text.replace(' | Premium Bespoke Bags', '')
                    h1_text = h1_text.replace(' | Bespoke Bags', '')
                    h1.string = h1_text
                else:
                    # 从文件名生成H1
                    filename = os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
                    h1.string = filename
                
                # 添加H1到body
                body.append(h1)
                modified = True
                print(f"添加H1标签: {file_path}")
                print(f"  H1内容: {h1.get_text()}")
                
                # 添加一些基本内容
                if 'customer-service' in file_path:
                    content_div = soup.new_tag('div', **{'class': 'container'})
                    content_p = soup.new_tag('p')
                    content_p.string = "At Bespoke Bags, we pride ourselves on delivering exceptional customer service excellence. Our commitment to quality and customer satisfaction drives everything we do."
                    content_div.append(content_p)
                    body.append(content_div)
                elif 'cosmetic-bags' in file_path:
                    content_div = soup.new_tag('div', **{'class': 'container'})
                    content_p = soup.new_tag('p')
                    content_p.string = "Discover our comprehensive guide to luxury cosmetic bags for 2024. From premium materials to innovative designs, explore the latest trends in beauty accessories."
                    content_div.append(content_p)
                    body.append(content_div)
                elif 'laptop-bags' in file_path:
                    content_div = soup.new_tag('div', **{'class': 'container'})
                    content_p = soup.new_tag('p')
                    content_p.string = "Professional laptop bags guide 2024 - Part 2. Explore advanced features, security options, and premium materials for the modern professional."
                    content_div.append(content_p)
                    body.append(content_div)
                elif 'carry-on' in file_path:
                    content_div = soup.new_tag('div', **{'class': 'container'})
                    content_p = soup.new_tag('p')
                    content_p.string = "Premium carry-on bags designed for the discerning traveler. Combining functionality with luxury craftsmanship for your travel needs."
                    content_div.append(content_p)
                    body.append(content_div)
            
            # 修复标题过长问题
            title_tag = soup.find('title')
            if title_tag and title_tag.get_text().strip():
                title_text = title_tag.get_text().strip()
                if len(title_text) > 60:
                    # 截断标题
                    new_title = title_text[:57] + "..."
                    title_tag.string = new_title
                    modified = True
                    print(f"截断过长标题: {file_path}")
                    print(f"  原标题: {title_text}")
                    print(f"  新标题: {new_title}")
                    
                    # 同步更新OG和Twitter标题
                    og_title = soup.find('meta', attrs={'property': 'og:title'})
                    if og_title:
                        og_title['content'] = new_title
                    
                    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
                    if twitter_title:
                        twitter_title['content'] = new_title
            
            # 保存修改后的文件
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                fixed_count += 1
                print(f"✅ 修复完成: {file_path}")
                print()
            else:
                print(f"ℹ️  无需修复: {file_path}")
                
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时出错: {str(e)}")
    
    print(f"\n修复完成！共修复了 {fixed_count} 个文件")

if __name__ == '__main__':
    fix_incomplete_html()