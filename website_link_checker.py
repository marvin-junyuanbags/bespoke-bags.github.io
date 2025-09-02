#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站链接检查器
检查网站中的所有链接是否正常工作，检测404错误和其他问题
"""

import os
import re
import json
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import defaultdict

class WebsiteLinkChecker:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.base_url = "https://bespoke-bags.com/"
        self.issues = []
        self.checked_files = set()
        self.all_links = set()
        self.internal_links = set()
        self.external_links = set()
        self.missing_files = set()
        
    def is_html_file(self, file_path):
        """检查是否为HTML文件"""
        return file_path.lower().endswith('.html')
    
    def get_all_html_files(self):
        """获取所有HTML文件"""
        html_files = []
        for root, dirs, files in os.walk(self.root_dir):
            # 跳过隐藏目录和不需要的目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
            
            for file in files:
                if self.is_html_file(file):
                    file_path = os.path.join(root, file)
                    html_files.append(file_path)
        return html_files
    
    def extract_links_from_file(self, file_path):
        """从HTML文件中提取所有链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            links = []
            
            # 提取所有链接
            for tag in soup.find_all(['a', 'link', 'img', 'script']):
                if tag.name == 'a' and tag.get('href'):
                    links.append(('href', tag.get('href')))
                elif tag.name == 'link' and tag.get('href'):
                    links.append(('href', tag.get('href')))
                elif tag.name == 'img' and tag.get('src'):
                    links.append(('src', tag.get('src')))
                elif tag.name == 'script' and tag.get('src'):
                    links.append(('src', tag.get('src')))
            
            return links
            
        except Exception as e:
            self.issues.append({
                'type': 'file_read_error',
                'file': file_path,
                'error': str(e)
            })
            return []
    
    def is_internal_link(self, link):
        """判断是否为内部链接"""
        if link.startswith('http://') or link.startswith('https://'):
            parsed = urlparse(link)
            return parsed.netloc in ['bespoke-bags.com', 'www.bespoke-bags.com']
        return True  # 相对链接视为内部链接
    
    def resolve_link_path(self, link, current_file):
        """解析链接的实际文件路径"""
        if link.startswith('http://') or link.startswith('https://'):
            return None  # 外部链接
        
        if link.startswith('#'):
            return None  # 锚点链接
        
        if link.startswith('mailto:') or link.startswith('tel:'):
            return None  # 邮件和电话链接
        
        # 移除查询参数和锚点
        link = link.split('?')[0].split('#')[0]
        
        if not link:
            return None
        
        # 获取当前文件的目录
        current_dir = os.path.dirname(current_file)
        
        if link.startswith('/'):
            # 绝对路径
            target_path = os.path.join(self.root_dir, link.lstrip('/'))
        else:
            # 相对路径
            target_path = os.path.join(current_dir, link)
        
        # 规范化路径
        target_path = os.path.normpath(target_path)
        
        # 如果链接指向目录，检查是否有index.html
        if os.path.isdir(target_path):
            index_path = os.path.join(target_path, 'index.html')
            if os.path.exists(index_path):
                return index_path
            else:
                return target_path  # 目录存在但没有index.html
        
        return target_path
    
    def check_file_links(self, file_path):
        """检查单个文件中的所有链接"""
        links = self.extract_links_from_file(file_path)
        
        for link_type, link in links:
            self.all_links.add(link)
            
            if self.is_internal_link(link):
                self.internal_links.add(link)
                
                # 解析实际文件路径
                target_path = self.resolve_link_path(link, file_path)
                
                if target_path:
                    if not os.path.exists(target_path):
                        self.missing_files.add(target_path)
                        self.issues.append({
                            'type': 'missing_file',
                            'source_file': file_path,
                            'link': link,
                            'target_path': target_path,
                            'link_type': link_type
                        })
                    elif os.path.isdir(target_path):
                        # 目录存在但没有index.html
                        self.issues.append({
                            'type': 'missing_index',
                            'source_file': file_path,
                            'link': link,
                            'target_path': target_path,
                            'link_type': link_type
                        })
            else:
                self.external_links.add(link)
    
    def check_all_links(self):
        """检查所有HTML文件中的链接"""
        html_files = self.get_all_html_files()
        
        print(f"找到 {len(html_files)} 个HTML文件")
        
        for file_path in html_files:
            print(f"检查文件: {os.path.relpath(file_path, self.root_dir)}")
            self.check_file_links(file_path)
            self.checked_files.add(file_path)
    
    def generate_report(self):
        """生成检查报告"""
        report = {
            'summary': {
                'total_files_checked': len(self.checked_files),
                'total_links_found': len(self.all_links),
                'internal_links': len(self.internal_links),
                'external_links': len(self.external_links),
                'total_issues': len(self.issues),
                'missing_files': len(self.missing_files)
            },
            'issues': self.issues,
            'missing_files': list(self.missing_files),
            'external_links': list(self.external_links)
        }
        
        return report
    
    def print_summary(self):
        """打印检查摘要"""
        print("\n" + "="*60)
        print("网站链接检查报告")
        print("="*60)
        
        print(f"检查的文件数量: {len(self.checked_files)}")
        print(f"发现的链接总数: {len(self.all_links)}")
        print(f"内部链接数量: {len(self.internal_links)}")
        print(f"外部链接数量: {len(self.external_links)}")
        print(f"发现的问题总数: {len(self.issues)}")
        print(f"缺失的文件数量: {len(self.missing_files)}")
        
        if self.issues:
            print("\n问题详情:")
            issue_types = defaultdict(int)
            for issue in self.issues:
                issue_types[issue['type']] += 1
            
            for issue_type, count in issue_types.items():
                print(f"  - {issue_type}: {count} 个")
            
            print("\n前10个问题:")
            for i, issue in enumerate(self.issues[:10]):
                print(f"  {i+1}. {issue['type']}: {issue.get('link', issue.get('target_path', 'N/A'))}")
                print(f"     来源: {os.path.relpath(issue.get('source_file', ''), self.root_dir)}")
        
        if self.missing_files:
            print("\n缺失的文件:")
            for i, missing_file in enumerate(list(self.missing_files)[:10]):
                print(f"  {i+1}. {os.path.relpath(missing_file, self.root_dir)}")

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"开始检查网站: {root_dir}")
    
    checker = WebsiteLinkChecker(root_dir)
    checker.check_all_links()
    
    # 生成报告
    report = checker.generate_report()
    
    # 保存报告到JSON文件
    report_file = os.path.join(root_dir, 'link_check_report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n详细报告已保存到: {report_file}")
    
    # 打印摘要
    checker.print_summary()
    
    return len(checker.issues) == 0

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n发现链接问题，请检查报告文件获取详细信息。")
    else:
        print("\n所有链接检查通过！")