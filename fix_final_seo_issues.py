#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复最后的SEO问题 - bespoke-bags.com
"""

import os
from bs4 import BeautifulSoup

def fix_final_issues():
    """修复最后的SEO问题"""
    
    # 需要修复的文件列表
    problem_files = [
        './blog/customer-service-excellence.html',
        './blog/luxury-cosmetic-bags-guide-2024.html', 
        './blog/professional-laptop-bags-guide-2024-part2.html',
        './products/carry-on-bags.html'
    ]
    
    fixed_count = 0
    
    print("开始修复最后的SEO问题...")
    print("=" * 50)
    
    for file_path in problem_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            modified = False
            
            # 修复标题过短问题
            title_tag = soup.find('title')
            if title_tag and title_tag.get_text().strip():
                title_text = title_tag.get_text().strip()
                if len(title_text) < 30:
                    # 扩展标题
                    if 'carry-on' in file_path.lower():
                        new_title = title_text + " | Premium Travel Bags | Bespoke Bags"
                    else:
                        new_title = title_text + " | Premium Bespoke Bags"
                    
                    title_tag.string = new_title
                    modified = True
                    print(f"扩展标题: {file_path}")
                    print(f"  原标题: {title_text}")
                    print(f"  新标题: {new_title}")
                    
                    # 同步更新OG和Twitter标题
                    og_title = soup.find('meta', attrs={'property': 'og:title'})
                    if og_title:
                        og_title['content'] = new_title
                    
                    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
                    if twitter_title:
                        twitter_title['content'] = new_title
            
            # 修复缺少H1标签问题
            h1_tags = soup.find_all('h1')
            if not h1_tags:
                body = soup.find('body')
                if body:
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
                    
                    # 查找合适的位置插入H1
                    # 优先插入到main标签中
                    main_tag = soup.find('main')
                    if main_tag:
                        if main_tag.contents:
                            main_tag.insert(0, h1)
                        else:
                            main_tag.append(h1)
                    else:
                        # 如果没有main标签，插入到body开头
                        if body.contents:
                            body.insert(0, h1)
                        else:
                            body.append(h1)
                    
                    modified = True
                    print(f"添加H1标签: {file_path}")
                    print(f"  H1内容: {h1.get_text()}")
            
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
    fix_final_issues()