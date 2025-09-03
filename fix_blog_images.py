#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 bespoke-bags.com 博客首页的配图问题
1. 为缺少配图的文章添加配图
2. 调整配图尺寸确保完整显示
3. 为其他页面添加合适的配图
"""

import os
import re
from bs4 import BeautifulSoup
import random

def get_available_images(images_dir):
    """获取可用的图片列表"""
    images = []
    if os.path.exists(images_dir):
        for file in os.listdir(images_dir):
            if file.endswith(('.webp', '.jpg', '.jpeg', '.png')):
                images.append(file)
    return sorted(images)

def fix_blog_index_images(file_path, images_dir):
    """修复博客首页的配图问题"""
    print(f"正在修复博客首页配图: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    available_images = get_available_images(images_dir)
    
    # 修复缺少配图的文章
    missing_images = [
        ('Global Luxury Leather Goods Market Analysis 2024', 'luxury-market-analysis.jpg'),
        ('The Art of Craftsmanship: Maintaining Excellence in Mass Production', 'craftsmanship-excellence.jpg'),
        ('Supply Chain Optimization for Luxury Leather Goods', 'supply-chain-optimization.jpg')
    ]
    
    # 为缺少配图的文章添加配图
    blog_cards = soup.find_all('article', class_='blog-card')
    image_index = 0
    
    for card in blog_cards:
        blog_image = card.find('div', class_='blog-image')
        if blog_image:
            style = blog_image.get('style', '')
            if not style or 'background-image' not in style:
                # 为缺少配图的文章添加配图
                if image_index < len(available_images):
                    new_image = available_images[image_index % len(available_images)]
                    blog_image['style'] = f"background-image: url('../images/{new_image}');"
                    print(f"为文章添加配图: {new_image}")
                    image_index += 1
    
    # 添加CSS样式来确保配图完整显示
    style_tag = soup.find('style')
    if not style_tag:
        style_tag = soup.new_tag('style')
        head = soup.find('head')
        if head:
            head.append(style_tag)
    
    # 添加或更新CSS样式
    css_fixes = """
    /* 修复博客配图显示问题 */
    .blog-image {
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        height: 200px !important;
        border-radius: 8px 8px 0 0;
    }
    
    .featured-article-main .article-image {
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        height: 300px !important;
        border-radius: 8px;
    }
    
    .featured-article-small .article-image {
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        height: 120px !important;
        border-radius: 8px;
    }
    
    /* 确保配图在不同屏幕尺寸下都能完整显示 */
    @media (max-width: 768px) {
        .blog-image {
            height: 180px !important;
        }
        .featured-article-main .article-image {
            height: 250px !important;
        }
        .featured-article-small .article-image {
            height: 100px !important;
        }
    }
    """
    
    if style_tag.string:
        style_tag.string += css_fixes
    else:
        style_tag.string = css_fixes
    
    # 保存修改后的文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"博客首页配图修复完成: {file_path}")

def add_images_to_other_pages(root_dir, images_dir):
    """为其他页面添加配图"""
    print("正在为其他页面添加配图...")
    
    available_images = get_available_images(images_dir)
    if not available_images:
        print("没有找到可用的图片")
        return
    
    # 需要添加配图的页面目录
    page_dirs = ['about', 'services', 'products', 'contact']
    
    for page_dir in page_dirs:
        dir_path = os.path.join(root_dir, page_dir)
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.endswith('.html'):
                    file_path = os.path.join(dir_path, file)
                    add_image_to_page(file_path, available_images, images_dir)

def add_image_to_page(file_path, available_images, images_dir):
    """为单个页面添加配图"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否已经有hero section的背景图
        hero_section = soup.find('section', class_='hero')
        if hero_section:
            style = hero_section.get('style', '')
            if 'background-image' not in style:
                # 添加背景图
                random_image = random.choice(available_images)
                new_style = f"background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('../images/{random_image}'); background-size: cover; background-position: center;"
                if style:
                    hero_section['style'] = style + '; ' + new_style
                else:
                    hero_section['style'] = new_style
                print(f"为页面 {file_path} 添加hero背景图: {random_image}")
        
        # 查找其他可能需要配图的元素
        image_containers = soup.find_all(['div', 'section'], class_=re.compile(r'.*image.*|.*photo.*|.*picture.*'))
        for container in image_containers:
            if not container.find('img') and 'background-image' not in container.get('style', ''):
                random_image = random.choice(available_images)
                container['style'] = f"background-image: url('../images/{random_image}'); background-size: cover; background-position: center; min-height: 300px;"
                print(f"为容器添加背景图: {random_image}")
        
        # 添加CSS样式确保图片适当显示
        style_tag = soup.find('style')
        if not style_tag:
            style_tag = soup.new_tag('style')
            head = soup.find('head')
            if head:
                head.append(style_tag)
        
        css_additions = """
        /* 页面配图优化 */
        .hero {
            min-height: 400px;
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
        }
        
        @media (max-width: 768px) {
            .hero {
                min-height: 300px;
            }
        }
        """
        
        if style_tag.string:
            style_tag.string += css_additions
        else:
            style_tag.string = css_additions
        
        # 保存修改后的文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"页面配图添加完成: {file_path}")
        
    except Exception as e:
        print(f"处理页面 {file_path} 时出错: {e}")

def main():
    """主函数"""
    root_dir = r'C:\Users\A1775\bespoke-bags.com'
    images_dir = os.path.join(root_dir, 'images')
    blog_index_path = os.path.join(root_dir, 'blog', 'index.html')
    
    print("开始修复 bespoke-bags.com 网站配图问题...")
    
    # 1. 修复博客首页配图问题
    if os.path.exists(blog_index_path):
        fix_blog_index_images(blog_index_path, images_dir)
    else:
        print(f"博客首页文件不存在: {blog_index_path}")
    
    # 2. 为其他页面添加配图
    add_images_to_other_pages(root_dir, images_dir)
    
    print("\n配图优化完成！")
    print("主要修复内容:")
    print("1. 为博客首页缺少配图的文章添加了配图")
    print("2. 调整了配图CSS样式，确保配图完整显示")
    print("3. 为其他页面添加了合适的配图")
    print("4. 优化了响应式设计，适配不同屏幕尺寸")

if __name__ == '__main__':
    main()