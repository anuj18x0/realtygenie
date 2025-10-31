from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os
import json
import tempfile
import shutil
from typing import Tuple, Optional, Union
import numpy as np

class PropertyImageProcessor:
    
    def __init__(self, target_size: Tuple[int, int] = (1080, 810), quality: int = 85):
        self.target_size = target_size
        self.quality = quality
        self.enhancement_profiles = {
            'light': {'brightness': 1.05, 'contrast': 1.08, 'saturation': 1.05, 'sharpness': 1.1},
            'medium': {'brightness': 1.1, 'contrast': 1.15, 'saturation': 1.1, 'sharpness': 1.2},
            'strong': {'brightness': 1.15, 'contrast': 1.25, 'saturation': 1.15, 'sharpness': 1.3}
        }
    
    def enhance_image(self, image_path: str, enhancement_level: str = 'medium') -> str:
        try:
            image = Image.open(image_path).convert('RGB')
            
            profile = self.enhancement_profiles.get(enhancement_level, self.enhancement_profiles['medium'])
            
            image = self._enhance_brightness(image, profile['brightness'])
            image = self._enhance_contrast(image, profile['contrast'])
            image = self._enhance_saturation(image, profile['saturation'])
            image = self._enhance_sharpness(image, profile['sharpness'])
            image = self._auto_balance_colors(image)
            image = self._reduce_noise(image)
            
            enhanced_path = image_path.replace('.', '_enhanced.')
            if not enhanced_path.endswith(('.jpg', '.jpeg')):
                enhanced_path = os.path.splitext(enhanced_path)[0] + '.jpg'
            
            image.save(enhanced_path, 'JPEG', quality=95, optimize=True)
            return enhanced_path
            
        except Exception as e:
            raise Exception(f"Error enhancing {image_path}: {str(e)}")
    
    def resize_image(self, image_path: str, target_width: int = 1080, target_height: int = 810) -> str:
        try:
            image = Image.open(image_path).convert('RGB')
            
            resized_image = self._smart_resize(image, (target_width, target_height))
            
            resized_path = image_path.replace('.', '_resized.')
            if not resized_path.endswith(('.jpg', '.jpeg')):
                resized_path = os.path.splitext(resized_path)[0] + '.jpg'
            
            resized_image.save(resized_path, 'JPEG', quality=92, optimize=True)
            return resized_path
            
        except Exception as e:
            raise Exception(f"Error resizing {image_path}: {str(e)}")
    
    def compress_image(self, image_path: str, quality: int = 85) -> str:
        try:
            image = Image.open(image_path).convert('RGB')
            
            image = self._optimize_for_web(image)
            
            compressed_path = image_path.replace('.', '_compressed.')
            if not compressed_path.endswith(('.jpg', '.jpeg')):
                compressed_path = os.path.splitext(compressed_path)[0] + '.jpg'
            
            image.save(compressed_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            return compressed_path
            
        except Exception as e:
            raise Exception(f"Error compressing {image_path}: {str(e)}")
    
    def process_image(self, image_path: str, output_path: str = None, enhancement_level: str = 'medium') -> dict:
        try:
            if output_path is None:
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(os.path.dirname(image_path), f"{base_name}_processed.jpg")
            
            original_size = os.path.getsize(image_path)
            original_image = Image.open(image_path)
            original_dimensions = original_image.size
            
            enhanced_path = self.enhance_image(image_path, enhancement_level)
            resized_path = self.resize_image(enhanced_path, *self.target_size)
            final_path = self.compress_image(resized_path, self.quality)
            
            shutil.move(final_path, output_path)
            
            for temp_path in [enhanced_path, resized_path]:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            final_size = os.path.getsize(output_path)
            final_image = Image.open(output_path)
            final_dimensions = final_image.size
            
            compression_ratio = (1 - final_size / original_size) * 100
            
            metadata = {
                'status': 'success',
                'original_file_size': original_size,
                'final_file_size': final_size,
                'compression_ratio': f"{compression_ratio:.1f}%",
                'original_dimensions': original_dimensions,
                'final_dimensions': final_dimensions,
                'enhancement_level': enhancement_level,
                'quality_setting': self.quality,
                'output_path': output_path
            }
            
            return metadata
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'input_path': image_path
            }
    
    def _enhance_brightness(self, image: Image.Image, factor: float) -> Image.Image:
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def _enhance_contrast(self, image: Image.Image, factor: float) -> Image.Image:
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def _enhance_saturation(self, image: Image.Image, factor: float) -> Image.Image:
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    def _enhance_sharpness(self, image: Image.Image, factor: float) -> Image.Image:
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)
    
    def _auto_balance_colors(self, image: Image.Image) -> Image.Image:
        return ImageOps.autocontrast(image, cutoff=1)
    
    def _reduce_noise(self, image: Image.Image) -> Image.Image:
        return image.filter(ImageFilter.MedianFilter(size=1))
    
    def _smart_resize(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        img_ratio = image.width / image.height
        target_ratio = target_size[0] / target_size[1]
        
        if img_ratio > target_ratio:
            new_height = target_size[1]
            new_width = int(new_height * img_ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            left = (new_width - target_size[0]) // 2
            image = image.crop((left, 0, left + target_size[0], target_size[1]))
        else:
            new_width = target_size[0]
            new_height = int(new_width / img_ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            top = (new_height - target_size[1]) // 2
            image = image.crop((0, top, target_size[0], top + target_size[1]))
        
        return image
    
    def _optimize_for_web(self, image: Image.Image) -> Image.Image:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image.filter(ImageFilter.UnsharpMask(radius=0.5, percent=110, threshold=2))
    
    def get_image_stats(self, image_path: str) -> dict:
        try:
            image = Image.open(image_path)
            file_size = os.path.getsize(image_path)
            
            return {
                'dimensions': image.size,
                'mode': image.mode,
                'format': image.format,
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'aspect_ratio': round(image.width / image.height, 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def process_batch(self, input_dir: str, output_dir: str, enhancement_level: str = 'medium') -> dict:
        os.makedirs(output_dir, exist_ok=True)
        results = {}
        
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_formats)]
        
        total_original_size = 0
        total_final_size = 0
        successful_count = 0
        
        for filename in image_files:
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + '_processed.jpg'
            output_path = os.path.join(output_dir, output_filename)
            
            print(f"🔄 Processing: {filename}")
            metadata = self.process_image(input_path, output_path, enhancement_level)
            
            if metadata['status'] == 'success':
                successful_count += 1
                total_original_size += metadata['original_file_size']
                total_final_size += metadata['final_file_size']
                print(f"Success: {filename} -> {output_filename}")
            else:
                print(f"Failed: {filename} - {metadata.get('error', 'Unknown error')}")
            
            results[filename] = metadata
        
        overall_compression = 0
        if total_original_size > 0:
            overall_compression = (1 - total_final_size / total_original_size) * 100
        
        summary = {
            'total_images': len(image_files),
            'successful': successful_count,
            'failed': len(image_files) - successful_count,
            'total_original_size_mb': round(total_original_size / (1024 * 1024), 2),
            'total_final_size_mb': round(total_final_size / (1024 * 1024), 2),
            'overall_compression_ratio': f"{overall_compression:.1f}%",
            'enhancement_level': enhancement_level
        }
        
        return {
            'summary': summary,
            'results': results
        }

def main():
    processor = PropertyImageProcessor(target_size=(1080, 810), quality=85)
    results = processor.process_batch('images', 'processed_images', 'medium')
    
    with open('processing_report.json', 'w') as f:
        json.dump(results, f, indent=2)
    
if __name__ == "__main__":
    main()