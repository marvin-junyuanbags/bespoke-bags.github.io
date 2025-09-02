#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复网站中的断开链接
根据链接检查报告修复常见的链接问题
"""

import os
import re
import json
from bs4 import BeautifulSoup
from collections import defaultdict

class BrokenLinkFixer:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.fixes_applied = 0
        self.files_modified = 0
        
        # 常见的链接修复映射
        self.link_fixes = {
            # 根目录页面修复
            '../products.html': '../products/index.html',
            '../about.html': '../about/index.html',
            '../blog.html': '../blog/index.html',
            '../contact.html': '../contact/index.html',
            '../services.html': '../services/index.html',
            
            # 产品页面修复
            'products.html': 'products/index.html',
            'about.html': 'about/index.html',
            'blog.html': 'blog/index.html',
            'contact.html': 'contact/index.html',
            'services.html': 'services/index.html',
            
            # 带锚点的链接修复
            '../products.html#business-bags': '../products/business-bags.html',
            '../products.html#travel-bags': '../products/travel-bags.html',
            '../products.html#handbags': '../products/handbags.html',
            '../products.html#backpacks': '../products/backpacks.html',
            '../products.html#luxury-handbags': '../products/luxury-handbags.html',
            '../products.html#leather-accessories': '../products/leather-accessories.html',
            '../products.html#evening-bags': '../products/evening-bags.html',
            '../products.html#custom-collections': '../products/custom-collections.html',
            '../products.html#travel-luggage': '../products/travel-luggage.html',
            
            # 服务页面修复
            '../services.html#oem-manufacturing': '../services/oem-manufacturing.html',
            '../services.html#odm-solutions': '../services/odm-solutions.html',
            '../services.html#custom-design': '../services/custom-design.html',
            '../services.html#private-label': '../services/private-label.html',
            '../services.html#quality-assurance': '../services/quality-assurance.html',
            '../services.html#packaging-logistics': '../services/packaging-logistics.html',
        }
        
        # 缺失的博客文章 - 创建重定向到相关现有文章
        self.blog_redirects = {
            'leather-care-maintenance-guide-2024.html': 'leather-care-maintenance-guide.html',
            'traditional-vs-modern-leather-techniques-2024.html': 'artisan-leather-craftsmanship-techniques-2024.html',
            'leather-tool-selection-guide-2024.html': 'bag-materials-selection-guide.html',
            'luxury-travel-style-guide-2024.html': 'luxury-travel-bags-guide.html',
        }
    
    def fix_file_links(self, file_path):
        """修复单个文件中的链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            soup = BeautifulSoup(content, 'html.parser')
            modified = False
            
            # 修复href链接
            for tag in soup.find_all(['a', 'link']):
                href = tag.get('href')
                if href and href in self.link_fixes:
                    tag['href'] = self.link_fixes[href]
                    modified = True
                    self.fixes_applied += 1
                    print(f"  修复链接: {href} -> {self.link_fixes[href]}")
            
            # 修复src链接
            for tag in soup.find_all(['img', 'script']):
                src = tag.get('src')
                if src and src in self.link_fixes:
                    tag['src'] = self.link_fixes[src]
                    modified = True
                    self.fixes_applied += 1
                    print(f"  修复资源: {src} -> {self.link_fixes[src]}")
            
            if modified:
                # 保存修改后的文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                self.files_modified += 1
                return True
            
            return False
            
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            return False
    
    def create_missing_blog_redirects(self):
        """为缺失的博客文章创建重定向页面"""
        blog_dir = os.path.join(self.root_dir, 'blog')
        
        for missing_file, redirect_to in self.blog_redirects.items():
            missing_path = os.path.join(blog_dir, missing_file)
            redirect_path = os.path.join(blog_dir, redirect_to)
            
            if not os.path.exists(missing_path) and os.path.exists(redirect_path):
                # 创建重定向页面
                redirect_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <meta http-equiv="refresh" content="0; url={redirect_to}">
    <link rel="canonical" href="https://bespoke-bags.com/blog/{redirect_to}" />
</head>
<body>
    <p>If you are not redirected automatically, <a href="{redirect_to}">click here</a>.</p>
    <script>
        window.location.href = "{redirect_to}";
    </script>
</body>
</html>'''
                
                try:
                    with open(missing_path, 'w', encoding='utf-8') as f:
                        f.write(redirect_content)
                    print(f"创建重定向页面: {missing_file} -> {redirect_to}")
                    self.fixes_applied += 1
                except Exception as e:
                    print(f"创建重定向页面失败 {missing_file}: {e}")
    
    def fix_all_links(self):
        """修复所有HTML文件中的链接"""
        html_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # 跳过隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                if file.lower().endswith('.html'):
                    file_path = os.path.join(root, file)
                    html_files.append(file_path)
        
        print(f"开始修复 {len(html_files)} 个HTML文件中的链接...")
        
        for file_path in html_files:
            rel_path = os.path.relpath(file_path, self.root_dir)
            print(f"检查文件: {rel_path}")
            self.fix_file_links(file_path)
        
        # 创建缺失的博客重定向页面
        print("\n创建缺失的博客文章重定向页面...")
        self.create_missing_blog_redirects()
    
    def generate_report(self):
        """生成修复报告"""
        print("\n" + "="*60)
        print("链接修复报告")
        print("="*60)
        print(f"修复的链接数量: {self.fixes_applied}")
        print(f"修改的文件数量: {self.files_modified}")
        
        if self.fixes_applied > 0:
            print("\n主要修复内容:")
            print("- 修正了指向根目录页面的错误链接")
            print("- 修正了带锚点的产品和服务页面链接")
            print("- 为缺失的博客文章创建了重定向页面")
            print("\n建议:")
            print("- 重新运行链接检查器验证修复效果")
            print("- 检查是否还有其他需要手动修复的链接")
        else:
            print("没有发现需要自动修复的链接问题。")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"开始修复网站链接: {root_dir}")
    
    fixer = BrokenLinkFixer(root_dir)
    fixer.fix_all_links()
    fixer.generate_report()
    
    return fixer.fixes_applied > 0

if __name__ == "__main__":
    success = main()
    if success:
        print("\n链接修复完成！建议重新运行链接检查器验证结果。")
    else:
        print("\n没有发现需要修复的链接。")