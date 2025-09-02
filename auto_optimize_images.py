#!/usr/bin/env python3
"""
Automated Image Optimization Script for Bespoke Bags Website
Optimizes images by compressing them and converting to modern formats
"""

import os
import sys
from PIL import Image
import json
from pathlib import Path
import shutil
from datetime import datetime

class AutoImageOptimizer:
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
            'files_processed': [],
            'errors': []
        }
    
    def create_backup(self):
        """Create backup of original images"""
        if not self.backup_dir.exists():
            print(f"Creating backup directory: {self.backup_dir}")
            shutil.copytree(self.images_dir, self.backup_dir)
            print("✓ Backup created successfully")
        else:
            print("✓ Backup directory already exists")
    
    def get_image_files(self):
        """Get all image files in the images directory"""
        image_files = []
        if not self.images_dir.exists():
            print(f"Images directory not found: {self.images_dir}")
            return image_files
        
        for file_path in self.images_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                image_files.append(file_path)
        
        return image_files
    
    def optimize_image(self, image_path, quality=85):
        """Optimize a single image"""
        try:
            original_size = image_path.stat().st_size
            
            with Image.open(image_path) as img:
                # Convert RGBA to RGB if saving as JPEG
                if img.mode in ('RGBA', 'LA', 'P') and image_path.suffix.lower() in ['.jpg', '.jpeg']:
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # Optimize and save
                save_kwargs = {
                    'optimize': True,
                    'quality': quality
                }
                
                if image_path.suffix.lower() == '.png':
                    save_kwargs = {'optimize': True}
                
                img.save(image_path, **save_kwargs)
            
            new_size = image_path.stat().st_size
            size_reduction = original_size - new_size
            
            file_info = {
                'path': str(image_path.relative_to(self.base_dir)),
                'original_size': original_size,
                'new_size': new_size,
                'size_reduction': size_reduction,
                'reduction_percentage': (size_reduction / original_size * 100) if original_size > 0 else 0
            }
            
            self.optimization_report['files_processed'].append(file_info)
            self.optimization_report['total_size_before'] += original_size
            self.optimization_report['total_size_after'] += new_size
            self.optimization_report['optimized_files'] += 1
            
            return True, size_reduction
            
        except Exception as e:
            error_info = {
                'path': str(image_path.relative_to(self.base_dir)),
                'error': str(e)
            }
            self.optimization_report['errors'].append(error_info)
            print(f"✗ Error optimizing {image_path.name}: {e}")
            return False, 0
    
    def create_webp_versions(self, image_files):
        """Create WebP versions of images"""
        print("\nCreating WebP versions...")
        webp_created = 0
        
        for image_path in image_files:
            if image_path.suffix.lower() == '.webp':
                continue
            
            try:
                webp_path = image_path.with_suffix('.webp')
                
                with Image.open(image_path) as img:
                    # Convert RGBA to RGB for better WebP compression
                    if img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'RGBA':
                            background.paste(img, mask=img.split()[-1])
                        else:
                            background.paste(img)
                        img = background
                    
                    img.save(webp_path, 'WebP', quality=85, optimize=True)
                    webp_created += 1
                    print(f"✓ Created WebP: {webp_path.name}")
                    
            except Exception as e:
                print(f"✗ Error creating WebP for {image_path.name}: {e}")
        
        print(f"\n✓ Created {webp_created} WebP versions")
        return webp_created
    
    def generate_report(self):
        """Generate optimization report"""
        total_reduction = self.optimization_report['total_size_before'] - self.optimization_report['total_size_after']
        reduction_percentage = (total_reduction / self.optimization_report['total_size_before'] * 100) if self.optimization_report['total_size_before'] > 0 else 0
        
        print(f"\n" + "="*50)
        print("IMAGE OPTIMIZATION REPORT")
        print("="*50)
        print(f"Total files found: {self.optimization_report['total_files']}")
        print(f"Files optimized: {self.optimization_report['optimized_files']}")
        print(f"Errors encountered: {len(self.optimization_report['errors'])}")
        print(f"\nSize reduction:")
        print(f"  Before: {self.optimization_report['total_size_before']:,} bytes")
        print(f"  After:  {self.optimization_report['total_size_after']:,} bytes")
        print(f"  Saved:  {total_reduction:,} bytes ({reduction_percentage:.1f}%)")
        
        # Save detailed report
        report_path = self.base_dir / 'image_optimization_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.optimization_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Detailed report saved to: {report_path}")
    
    def run_optimization(self):
        """Run the complete optimization process"""
        print("Bespoke Bags Automated Image Optimizer")
        print("=====================================")
        
        # Create backup
        self.create_backup()
        
        # Get image files
        image_files = self.get_image_files()
        self.optimization_report['total_files'] = len(image_files)
        
        if not image_files:
            print("No image files found to optimize.")
            return
        
        print(f"\nFound {len(image_files)} image files to optimize")
        
        # Optimize images
        print("\nOptimizing images...")
        total_saved = 0
        
        for i, image_path in enumerate(image_files, 1):
            print(f"[{i}/{len(image_files)}] Optimizing {image_path.name}...", end=" ")
            success, saved = self.optimize_image(image_path)
            if success:
                total_saved += saved
                print(f"✓ Saved {saved:,} bytes")
            else:
                print("✗ Failed")
        
        # Create WebP versions
        self.create_webp_versions(image_files)
        
        # Generate report
        self.generate_report()
        
        print("\n🎉 Image optimization completed!")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = Path(__file__).parent
    
    # Initialize optimizer
    optimizer = AutoImageOptimizer(script_dir)
    
    # Run optimization
    optimizer.run_optimization()