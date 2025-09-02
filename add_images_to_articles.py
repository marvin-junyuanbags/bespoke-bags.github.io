import os
import re
import random

# 定义文章类型和对应的图片映射
article_image_mapping = {
    'travel': ['bespoke-bags (1).webp', 'bespoke-bags (15).webp', 'bespoke-bags (25).webp', 'bespoke-bags (35).webp', 'bespoke-bags (45).webp'],
    'business': ['bespoke-bags (2).webp', 'bespoke-bags (12).webp', 'bespoke-bags (22).webp', 'bespoke-bags (32).webp', 'bespoke-bags (42).webp'],
    'luxury': ['bespoke-bags (3).webp', 'bespoke-bags (13).webp', 'bespoke-bags (23).webp', 'bespoke-bags (33).webp', 'bespoke-bags (43).webp'],
    'handbag': ['bespoke-bags (4).webp', 'bespoke-bags (14).webp', 'bespoke-bags (24).webp', 'bespoke-bags (34).webp', 'bespoke-bags (44).webp'],
    'manufacturing': ['bespoke-bags (5).webp', 'bespoke-bags (55).webp', 'bespoke-bags (65).webp', 'bespoke-bags (75).webp', 'bespoke-bags (85).webp'],
    'strategy': ['bespoke-bags (6).webp', 'bespoke-bags (16).webp', 'bespoke-bags (26).webp', 'bespoke-bags (36).webp', 'bespoke-bags (46).webp'],
    'management': ['bespoke-bags (7).webp', 'bespoke-bags (17).webp', 'bespoke-bags (27).webp', 'bespoke-bags (37).webp', 'bespoke-bags (47).webp'],
    'leather': ['bespoke-bags (8).webp', 'bespoke-bags (18).webp', 'bespoke-bags (28).webp', 'bespoke-bags (38).webp', 'bespoke-bags (48).webp'],
    'quality': ['bespoke-bags (9).webp', 'bespoke-bags (19).webp', 'bespoke-bags (29).webp', 'bespoke-bags (39).webp', 'bespoke-bags (49).webp'],
    'innovation': ['bespoke-bags (10).webp', 'bespoke-bags (20).webp', 'bespoke-bags (30).webp', 'bespoke-bags (40).webp', 'bespoke-bags (50).webp'],
    'default': ['bespoke-bags (11).webp', 'bespoke-bags (21).webp', 'bespoke-bags (31).webp', 'bespoke-bags (41).webp', 'bespoke-bags (51).webp']
}

def get_article_category(filename):
    """根据文件名确定文章类别"""
    filename_lower = filename.lower()
    
    if any(word in filename_lower for word in ['travel', 'backpack', 'luggage', 'suitcase']):
        return 'travel'
    elif any(word in filename_lower for word in ['business', 'executive', 'professional', 'briefcase']):
        return 'business'
    elif any(word in filename_lower for word in ['luxury', 'premium', 'designer']):
        return 'luxury'
    elif any(word in filename_lower for word in ['handbag', 'clutch', 'tote', 'shoulder', 'crossbody']):
        return 'handbag'
    elif any(word in filename_lower for word in ['manufacturing', 'production', 'craftsmanship', 'oem']):
        return 'manufacturing'
    elif any(word in filename_lower for word in ['strategy', 'marketing', 'brand', 'competitive']):
        return 'strategy'
    elif any(word in filename_lower for word in ['management', 'leadership', 'team', 'employee']):
        return 'management'
    elif any(word in filename_lower for word in ['leather', 'material', 'eco-friendly', 'sustainable']):
        return 'leather'
    elif any(word in filename_lower for word in ['quality', 'testing', 'certification', 'standards']):
        return 'quality'
    elif any(word in filename_lower for word in ['innovation', 'technology', 'digital', 'smart']):
        return 'innovation'
    else:
        return 'default'

def add_image_to_article(file_path):
    """为文章添加图片"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经有图片
        if '<div class="article-image">' in content:
            print(f"文章 {os.path.basename(file_path)} 已经有图片，跳过")
            return False
        
        # 获取文章类别和对应图片
        filename = os.path.basename(file_path)
        category = get_article_category(filename)
        image_options = article_image_mapping.get(category, article_image_mapping['default'])
        selected_image = random.choice(image_options)
        
        # 生成图片HTML
        image_html = f'''                    <div class="article-image">
                        <img src="../images/{selected_image}" alt="{filename.replace('.html', '').replace('-', ' ').title()}" loading="lazy">
                    </div>
                    
'''
        
        # 尝试多种插入位置
        patterns = [
            # 模式1: article-body div之后
            (r'(<div class="article-body">\s*\n)', f'\\1{image_html}'),
            # 模式2: post-content div之后，在第一个p标签之前
            (r'(<div class="post-content">\s*\n)(\s*<p class="lead">)', f'\\1{image_html}\\2'),
            # 模式3: post-content div之后，在任何p标签之前
            (r'(<div class="post-content">\s*\n)(\s*<p)', f'\\1{image_html}\\2'),
            # 模式4: post-content div之后，在任何h2标签之前
            (r'(<div class="post-content">\s*\n)(\s*<h2)', f'\\1{image_html}\\2')
        ]
        
        new_content = content
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                break
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已为文章 {filename} 添加图片: {selected_image}")
            return True
        else:
            print(f"未找到合适的插入位置: {filename}")
            return False
            
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {str(e)}")
        return False

def main():
    blog_dir = 'C:/Users/A1775/bespoke-bags.com/blog'
    
    if not os.path.exists(blog_dir):
        print(f"博客目录不存在: {blog_dir}")
        return
    
    html_files = [f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'index.html']
    
    print(f"找到 {len(html_files)} 个HTML文件")
    
    success_count = 0
    for html_file in html_files:
        file_path = os.path.join(blog_dir, html_file)
        if add_image_to_article(file_path):
            success_count += 1
    
    print(f"\n完成！成功为 {success_count} 篇文章添加了图片")

if __name__ == '__main__':
    main()