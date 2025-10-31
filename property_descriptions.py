import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os
import json
import re
import random
from typing import Dict, List

class PropertyDescriptionGenerator:
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device.upper()}")
        
        model_name = "Salesforce/blip-image-captioning-base"
        print("Loading BLIP model...")
        
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(
            model_name,
            dtype=torch.float16 if self.device == "cuda" else torch.float32,
            low_cpu_mem_usage=True,
            use_safetensors=True
        ).to(self.device)
        
        self.model.eval()
        print("Model loaded successfully!")
        
        self.room_mapping = {
            'living room': 'spacious living area',
            'kitchen': 'modern kitchen',
            'bedroom': 'comfortable bedroom',
            'bathroom': 'elegant bathroom',
            'dining room': 'formal dining room',
            'office': 'home office',
            'garage': 'attached garage'
        }
        
        self.enhancement_words = {
            'modern': ['contemporary', 'sleek', 'stylish', 'updated'],
            'spacious': ['open-concept', 'expansive', 'generous', 'airy'],
            'beautiful': ['stunning', 'gorgeous', 'elegant', 'charming'],
            'nice': ['lovely', 'attractive', 'appealing', 'inviting']
        }
    
    def generate_description(self, image_path: str, style: str = 'luxury', use_conditional=True) -> Dict[str, str]:
        try:
            image = Image.open(image_path).convert("RGB")
            
            if use_conditional:
                prompt = "A beautiful property featuring"
                inputs = self.processor(image, prompt, return_tensors="pt").to(self.device)
            else:
                inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=60,
                    num_beams=8,
                    early_stopping=True,
                    temperature=0.8,
                    do_sample=True,
                    top_p=0.9
                )
            
            raw_caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            if use_conditional and raw_caption.startswith("A beautiful property featuring"):
                raw_caption = raw_caption.replace("A beautiful property featuring", "").strip()
            
            descriptions = {}
            descriptions['raw'] = raw_caption
            descriptions['basic'] = raw_caption
            descriptions['enhanced'] = self._enhance_description(raw_caption)
            descriptions['luxury'] = self._generate_luxury_description(raw_caption)
            descriptions['family'] = self._generate_family_description(raw_caption)
            descriptions['investment'] = self._generate_investment_description(raw_caption)
            descriptions['social'] = self._generate_social_description(raw_caption)
            
            descriptions['primary'] = descriptions.get(style, descriptions['luxury'])
            
            return descriptions
            
        except Exception as e:
            return {'error': f"Failed to generate description: {str(e)}"}
    
    def _enhance_description(self, description: str) -> str:
        description = description.lower().strip()
        
        for basic_room, enhanced_room in self.room_mapping.items():
            if basic_room in description:
                description = description.replace(basic_room, enhanced_room)
        
        words = description.split()
        enhanced_words = []
        
        for word in words:
            word_clean = re.sub(r'[^\w]', '', word)
            if word_clean in self.enhancement_words:
                enhanced_word = random.choice(self.enhancement_words[word_clean])
                enhanced_words.append(word.replace(word_clean, enhanced_word))
            else:
                enhanced_words.append(word)
        
        enhanced_description = ' '.join(enhanced_words)
        
        enhanced_description = self._add_property_features(enhanced_description)
        
        enhanced_description = enhanced_description.capitalize()
        
        if not enhanced_description.endswith('.'):
            enhanced_description += '.'
        
        return enhanced_description
    
    def _add_property_features(self, description: str) -> str:
        features = []
        
        if 'kitchen' in description:
            features.append("featuring premium finishes")
        if 'living' in description:
            features.append("with abundant natural light")
        if 'bedroom' in description:
            features.append("offering peaceful retreat")
        if 'bathroom' in description:
            features.append("with modern fixtures")
        if 'balcony' in description or 'patio' in description:
            features.append("with outdoor space")
        if 'view' in description:
            features.append("boasting scenic views")
        
        if features:
            description += f" {features[0]}"
        
        return description
    
    def _generate_luxury_description(self, base_caption: str) -> str:
        
        luxury_intros = [
            'This exceptional property',
            'This distinguished residence', 
            'This remarkable home',
            'This prestigious offering',
            'This architectural masterpiece'
        ]
        
        intro = random.choice(luxury_intros)
        enhanced_features = self._enhance_description(base_caption)
        
        luxury_amenities = [
            "featuring premium finishes throughout",
            "with designer touches and high-end appointments",
            "boasting luxurious amenities and modern conveniences",
            "offering an unparalleled living experience"
        ]
        
        amenity = random.choice(luxury_amenities)
        
        cta_endings = [
            'Schedule your private showing today.',
            'Don\'t miss this rare opportunity.',
            'Perfect for the discerning buyer.',
            'A true must-see property.'
        ]
        
        conclusion = random.choice(cta_endings)
        
        luxury_desc = f"{intro} {enhanced_features} {amenity} {conclusion}"
        return self._polish_description(luxury_desc)
    
    def _generate_family_description(self, base_caption: str) -> str:
        
        family_intro = "Perfect for growing families, this wonderful home"
        family_features = self._enhance_description(base_caption)
        
        family_amenities = [
            "offers plenty of space for children to play",
            "features an open floor plan for family gatherings", 
            "includes a spacious backyard for outdoor activities",
            "provides quiet study areas for homework",
            "boasts a family-friendly kitchen layout"
        ]
        
        selected_amenity = random.choice(family_amenities)
        conclusion = "Your family will love calling this place home."
        
        family_desc = f"{family_intro} {family_features} and {selected_amenity}. {conclusion}"
        return self._polish_description(family_desc)
    
    def _generate_investment_description(self, base_caption: str) -> str:
        
        investment_intro = "Excellent investment opportunity featuring this well-maintained property"
        investment_features = self._enhance_description(base_caption)
        
        investment_benefits = [
            "in a high-demand rental market",
            "with strong appreciation potential", 
            "offering excellent cash flow opportunities",
            "in a prime location with growing property values",
            "with minimal maintenance requirements"
        ]
        
        selected_benefit = random.choice(investment_benefits)
        conclusion = "Contact us today for detailed financial projections."
        
        investment_desc = f"{investment_intro} {investment_features} {selected_benefit}. {conclusion}"
        return self._polish_description(investment_desc)
    
    def _generate_social_description(self, base_caption: str) -> str:
        
        social_starters = [
            "🏡 JUST LISTED!",
            "✨ NEW ON MARKET!",
            "🔥 HOT PROPERTY!",
            "💎 LUXURY LISTING!",
            "🌟 STUNNING HOME!"
        ]
        
        starter = random.choice(social_starters)
        short_desc = self._create_short_description(base_caption)
        
        hashtags = "#RealEstate #PropertyForSale #DreamHome #NewListing #RealtyGenie"
        
        return f"{starter} {short_desc} {hashtags}"
    
    def _create_short_description(self, caption: str) -> str:
        words = caption.split()[:8]  # Limit to first 8 words
        short = ' '.join(words)
        
        if len(short) > 60:
            short = short[:57] + "..."
        
        return short.capitalize()
    
    def _polish_description(self, description: str) -> str:
        description = description.strip()
        if description:
            description = description[0].upper() + description[1:]
        
        if not description.endswith('.'):
            description += '.'
        
        import re
        description = re.sub(r'\s+', ' ', description)
        
        description = description.replace(' ,', ',')
        description = description.replace(' .', '.')
        description = description.replace('  ', ' ')
        
        return description
    
    def _generate_luxury_description(self, base_caption: str) -> str:
        luxury_starters = [
            "This exceptional property",
            "This distinguished residence", 
            "This remarkable home",
            "This prestigious offering",
            "This architectural masterpiece"
        ]
        
        luxury_features = [
            "featuring premium finishes throughout",
            "with custom designer elements",
            "boasting luxury amenities",
            "offering sophisticated living spaces",
            "showcasing elegant architectural details"
        ]
        
        cta_endings = [
            "Schedule your private showing today.",
            "Perfect for the discerning buyer.",
            "Don't miss this rare opportunity.",
            "A true must-see property.",
            "Your dream home awaits."
        ]
        
        starter = random.choice(luxury_starters)
        enhanced_caption = self._enhance_description(base_caption)
        feature = random.choice(luxury_features)
        ending = random.choice(cta_endings)
        
        return f"{starter} {enhanced_caption} {feature} {ending}"
    
    def _generate_family_description(self, base_caption: str) -> str:
        family_intro = "Perfect for growing families, this wonderful home"
        enhanced_caption = self._enhance_description(base_caption)
        
        family_features = [
            "offers plenty of space for children to play",
            "features an open floor plan for family gatherings", 
            "includes safe and secure neighborhood living",
            "provides quiet study areas for homework",
            "boasts a family-friendly kitchen layout"
        ]
        
        feature = random.choice(family_features)
        conclusion = "Your family will love calling this place home."
        
        return f"{family_intro} {enhanced_caption} and {feature}. {conclusion}"
    
    def _generate_investment_description(self, base_caption: str) -> str:
        investment_intro = "Excellent investment opportunity featuring this well-maintained property"
        enhanced_caption = self._enhance_description(base_caption)
        
        investment_benefits = [
            "in a high-demand rental market",
            "with strong appreciation potential", 
            "offering excellent cash flow opportunities",
            "in a prime location with growing property values",
            "perfect for rental income generation"
        ]
        
        benefit = random.choice(investment_benefits)
        conclusion = "Contact us today for detailed financial projections."
        
        return f"{investment_intro} {enhanced_caption} {benefit}. {conclusion}"
    
    def _generate_social_description(self, base_caption: str) -> str:
        social_starters = [
            "🏡 JUST LISTED!",
            "✨ NEW ON MARKET!", 
            "🔥 HOT PROPERTY!",
            "💎 LUXURY LISTING!",
            "🌟 STUNNING HOME!"
        ]
        
        starter = random.choice(social_starters)
        enhanced_caption = self._enhance_description(base_caption)
        
        words = enhanced_caption.split()[:8]
        short_desc = ' '.join(words)
        
        hashtags = "#RealEstate #PropertyForSale #DreamHome #NewListing"
        
        return f"{starter} {short_desc} {hashtags}"
    
    def process_all_images(self, image_dir: str, output_dir: str) -> Dict[str, Dict]:
        os.makedirs(output_dir, exist_ok=True)
        results = {}
        
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        
        for filename in os.listdir(image_dir):
            if filename.lower().endswith(supported_formats):
                image_path = os.path.join(image_dir, filename)
                
                try:
                    descriptions = self.generate_description(image_path)
                    
                    output_file = os.path.join(output_dir, f"{filename}_description.txt")
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Enhanced: {descriptions['enhanced']}\\n")
                        f.write(f"Raw: {descriptions['raw']}")
                    
                    results[filename] = descriptions
                    print(f"{filename}: {descriptions['enhanced']}")
                    
                except Exception as e:
                    results[filename] = {'error': str(e)}
                    print(f" Error processing {filename}: {e}")
        
        results_file = os.path.join(output_dir, 'property_descriptions.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return results

def main():
    generator = PropertyDescriptionGenerator()
    
    print("\\nGenerating enhanced property descriptions...")
    results = generator.process_all_images('processed_images', 'descriptions')
    
    print(f"\\n Generated descriptions for {len(results)} images")
    print(" Results saved to descriptions/ folder")

if __name__ == "__main__":
    main()