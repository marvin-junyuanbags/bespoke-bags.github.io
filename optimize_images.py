#!/usr/bin/env python3
"""
Image Optimization Script for Bespoke Bags Website
Optimizes images by compressing them and converting to modern formats
"""

import os
import sys
from PIL import Image
import json
from pathlib import Path
import shutil
from datetime import datetime

class ImageOptimizer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.images_dir = self.base_dir / 'images'
        self.backup_dir = self.base_dir / 'images_backup'
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        self.optimization_report = {
            'timestamp': datetime.now().isoformat(),
            'total_files': 0,
            'optimized_files': 0,
            'total_size_before': 0,
            'total_size_after': 0,
            'space_saved': 0,
            'files': []
        }
    
    def create_backup(self):
        """Create backup of original images"""
        if self.backup_dir.exists():
            print(f"Backup directory already exists: {self.backup_dir}")
            return
        
        print(f"Creating backup of images to: {self.backup_dir}")
        shutil.copytree(self.images_dir, self.backup_dir)
        print("Backup created successfully!")
    
    def get_image_files(self):
        """Get all image files in the images directory"""
        image_files = []
        
        for root, dirs, files in os.walk(self.images_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.supported_formats:
                    image_files.append(file_path)
        
        return image_files
    
    def optimize_image(self, image_path, quality=85, max_width=1920, max_height=1080):
        """Optimize a single image"""
        try:
            # Get original file size
            original_size = image_path.stat().st_size
            
            # Open image
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if saving as JPEG
                if img.mode in ('RGBA', 'LA', 'P') and image_path.suffix.lower() in ['.jpg', '.jpeg']:
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Resize if image is too large
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    print(f"  Resized to: {img.width}x{img.height}")
                
                # Optimize and save
                save_kwargs = {
                    'optimize': True,
                    'quality': quality
                }
                
                # Add format-specific optimizations
                if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                    save_kwargs['progressive'] = True
                elif image_path.suffix.lower() == '.png':
                    save_kwargs['compress_level'] = 9
                
                # Save optimized image
                img.save(image_path, **save_kwargs)
            
            # Get new file size
            new_size = image_path.stat().st_size
            space_saved = original_size - new_size
            compression_ratio = (space_saved / original_size) * 100 if original_size > 0 else 0
            
            return {
                'success': True,
                'original_size': original_size,
                'new_size': new_size,
                'space_saved': space_saved,
                'compression_ratio': compression_ratio
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def convert_to_webp(self, image_path, quality=85):
        """Convert image to WebP format for better compression"""
        try:
            webp_path = image_path.with_suffix('.webp')
            
            # Skip if WebP already exists and is newer
            if webp_path.exists() and webp_path.stat().st_mtime > image_path.stat().st_mtime:
                return {'success': True, 'skipped': True, 'path': webp_path}
            
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    
                    # For WebP, we can keep transparency
                    if img.mode == 'RGBA':
                        pass  # Keep RGBA for WebP
                    else:
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if len(img.split()) > 3 else None)
                        img = background
                
                # Save as WebP
                img.save(webp_path, 'WebP', quality=quality, optimize=True)
            
            original_size = image_path.stat().st_size
            webp_size = webp_path.stat().st_size
            space_saved = original_size - webp_size
            
            return {
                'success': True,
                'original_size': original_size,
                'webp_size': webp_size,
                'space_saved': space_saved,
                'path': webp_path
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_responsive_images(self, image_path, sizes=[480, 768, 1024, 1920]):
        """Generate responsive image sizes"""
        try:
            responsive_images = []
            
            with Image.open(image_path) as img:
                original_width = img.width
                
                for size in sizes:
                    if size >= original_width:
                        continue  # Skip if size is larger than original
                    
                    # Calculate new height maintaining aspect ratio
                    aspect_ratio = img.height / img.width
                    new_height = int(size * aspect_ratio)
                    
                    # Create resized image
                    resized_img = img.copy()
                    resized_img.thumbnail((size, new_height), Image.Resampling.LANCZOS)
                    
                    # Generate filename with size suffix
                    name_parts = image_path.stem.split('.')
                    base_name = name_parts[0]
                    extension = image_path.suffix
                    
                    responsive_path = image_path.parent / f"{base_name}_{size}w{extension}"
                    
                    # Save responsive image
                    save_kwargs = {'optimize': True, 'quality': 85}
                    if extension.lower() in ['.jpg', '.jpeg']:
                        save_kwargs['progressive'] = True
                    elif extension.lower() == '.png':
                        save_kwargs['compress_level'] = 9
                    
                    resized_img.save(responsive_path, **save_kwargs)
                    responsive_images.append({
                        'size': size,
                        'path': responsive_path,
                        'dimensions': f"{resized_img.width}x{resized_img.height}"
                    })
            
            return {
                'success': True,
                'responsive_images': responsive_images
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def optimize_all_images(self, create_webp=True, create_responsive=True):
        """Optimize all images in the images directory"""
        print("Starting image optimization...")
        
        # Create backup first
        self.create_backup()
        
        # Get all image files
        image_files = self.get_image_files()
        self.optimization_report['total_files'] = len(image_files)
        
        print(f"Found {len(image_files)} image files to optimize")
        
        for i, image_path in enumerate(image_files, 1):
            print(f"\n[{i}/{len(image_files)}] Processing: {image_path.name}")
            
            file_report = {
                'filename': image_path.name,
                'path': str(image_path.relative_to(self.base_dir)),
                'original_size': image_path.stat().st_size,
                'optimizations': []
            }
            
            # Original optimization
            print("  Optimizing original image...")
            opt_result = self.optimize_image(image_path)
            
            if opt_result['success']:
                file_report['optimizations'].append({
                    'type': 'compression',
                    'original_size': opt_result['original_size'],
                    'new_size': opt_result['new_size'],
                    'space_saved': opt_result['space_saved'],
                    'compression_ratio': opt_result['compression_ratio']
                })
                
                self.optimization_report['total_size_before'] += opt_result['original_size']
                self.optimization_report['total_size_after'] += opt_result['new_size']
                self.optimization_report['space_saved'] += opt_result['space_saved']
                
                print(f"    Compressed: {self.format_size(opt_result['space_saved'])} saved ({opt_result['compression_ratio']:.1f}%)")
            else:
                print(f"    Error: {opt_result['error']}")
                file_report['optimizations'].append({
                    'type': 'compression',
                    'error': opt_result['error']
                })
            
            # Create WebP version
            if create_webp and image_path.suffix.lower() != '.webp':
                print("  Creating WebP version...")
                webp_result = self.convert_to_webp(image_path)
                
                if webp_result['success']:
                    if webp_result.get('skipped'):
                        print("    WebP version already exists and is up to date")
                    else:
                        file_report['optimizations'].append({
                            'type': 'webp_conversion',
                            'original_size': webp_result['original_size'],
                            'webp_size': webp_result['webp_size'],
                            'space_saved': webp_result['space_saved'],
                            'webp_path': str(webp_result['path'].relative_to(self.base_dir))
                        })
                        print(f"    WebP created: {self.format_size(webp_result['space_saved'])} saved")
                else:
                    print(f"    WebP error: {webp_result['error']}")
                    file_report['optimizations'].append({
                        'type': 'webp_conversion',
                        'error': webp_result['error']
                    })
            
            # Create responsive images
            if create_responsive and image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                print("  Creating responsive sizes...")
                responsive_result = self.generate_responsive_images(image_path)
                
                if responsive_result['success']:
                    file_report['optimizations'].append({
                        'type': 'responsive_images',
                        'responsive_images': responsive_result['responsive_images']
                    })
                    print(f"    Created {len(responsive_result['responsive_images'])} responsive sizes")
                else:
                    print(f"    Responsive error: {responsive_result['error']}")
                    file_report['optimizations'].append({
                        'type': 'responsive_images',
                        'error': responsive_result['error']
                    })
            
            self.optimization_report['files'].append(file_report)
            self.optimization_report['optimized_files'] += 1
        
        # Save optimization report
        self.save_report()
        
        # Print summary
        self.print_summary()
    
    def format_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def save_report(self):
        """Save optimization report to JSON file"""
        report_path = self.base_dir / 'image_optimization_report.json'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.optimization_report, f, indent=2, ensure_ascii=False)
        
        print(f"\nOptimization report saved to: {report_path}")
    
    def print_summary(self):
        """Print optimization summary"""
        report = self.optimization_report
        
        print("\n" + "="*60)
        print("IMAGE OPTIMIZATION SUMMARY")
        print("="*60)
        print(f"Total files processed: {report['total_files']}")
        print(f"Files optimized: {report['optimized_files']}")
        print(f"Original total size: {self.format_size(report['total_size_before'])}")
        print(f"Optimized total size: {self.format_size(report['total_size_after'])}")
        print(f"Space saved: {self.format_size(report['space_saved'])}")
        
        if report['total_size_before'] > 0:
            compression_ratio = (report['space_saved'] / report['total_size_before']) * 100
            print(f"Overall compression: {compression_ratio:.1f}%")
        
        print("\nOptimization completed successfully!")
        print(f"Backup of original images saved to: {self.backup_dir}")
    
    def create_picture_elements_guide(self):
        """Create a guide for using picture elements with responsive images"""
        guide_content = '''
<!-- Guide for Using Optimized Images -->

<!-- For modern browsers with WebP support and responsive images -->
<picture>
  <source media="(max-width: 480px)" 
          srcset="images/product_480w.webp" 
          type="image/webp">
  <source media="(max-width: 768px)" 
          srcset="images/product_768w.webp" 
          type="image/webp">
  <source media="(max-width: 1024px)" 
          srcset="images/product_1024w.webp" 
          type="image/webp">
  <source srcset="images/product.webp" 
          type="image/webp">
  
  <!-- Fallback for browsers that don't support WebP -->
  <source media="(max-width: 480px)" 
          srcset="images/product_480w.jpg">
  <source media="(max-width: 768px)" 
          srcset="images/product_768w.jpg">
  <source media="(max-width: 1024px)" 
          srcset="images/product_1024w.jpg">
  
  <!-- Final fallback -->
  <img src="images/product.jpg" 
       alt="Product description" 
       loading="lazy"
       width="800" 
       height="600">
</picture>

<!-- Simple responsive image with srcset -->
<img src="images/product.jpg"
     srcset="images/product_480w.jpg 480w,
             images/product_768w.jpg 768w,
             images/product_1024w.jpg 1024w,
             images/product.jpg 1920w"
     sizes="(max-width: 480px) 100vw,
            (max-width: 768px) 100vw,
            (max-width: 1024px) 100vw,
            1920px"
     alt="Product description"
     loading="lazy">

<!-- CSS for lazy loading placeholder -->
<style>
img[loading="lazy"] {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
'''
        
        guide_path = self.base_dir / 'responsive_images_guide.html'
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"Responsive images guide created: {guide_path}")

def main():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent
    
    print("Bespoke Bags Image Optimizer")
    print("============================\n")
    
    # Check if images directory exists
    images_dir = script_dir / 'images'
    if not images_dir.exists():
        print(f"Error: Images directory not found at {images_dir}")
        print("Please make sure you're running this script from the website root directory.")
        return
    
    # Initialize optimizer
    optimizer = ImageOptimizer(script_dir)
    
    # Ask user for optimization options
    print("Optimization Options:")
    print("1. Full optimization (compression + WebP + responsive)")
    print("2. Compression only")
    print("3. Compression + WebP")
    print("4. Custom options")
    
    try:
        choice = input("\nSelect option (1-4) [1]: ").strip() or "1"
        
        create_webp = True
        create_responsive = True
        
        if choice == "2":
            create_webp = False
            create_responsive = False
        elif choice == "3":
            create_responsive = False
        elif choice == "4":
            create_webp = input("Create WebP versions? (y/n) [y]: ").strip().lower() != 'n'
            create_responsive = input("Create responsive sizes? (y/n) [y]: ").strip().lower() != 'n'
        
        # Run optimization
        optimizer.optimize_all_images(
            create_webp=create_webp,
            create_responsive=create_responsive
        )
        
        # Create guide
        if create_responsive:
            optimizer.create_picture_elements_guide()
        
    except KeyboardInterrupt:
        print("\nOptimization cancelled by user.")
    except Exception as e:
        print(f"\nError during optimization: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())