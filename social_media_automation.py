import json
import os
import random
from datetime import datetime
from typing import Dict, List, Tuple

class SocialMediaGenerator:
    
    def __init__(self):
        
        self.post_templates = [
            "🏡 {description} Perfect for families looking for their dream home! {price_cta}",
            "✨ {description} Don't miss this incredible opportunity! {price_cta}",
            "🌟 FEATURED LISTING: {description} {price_cta}",
            "🔑 NEW ON MARKET: {description} Schedule your viewing today! {price_cta}",
            "💎 {description} This won't last long! {price_cta}",
            "🏠 JUST LISTED: {description} Your future home awaits! {price_cta}"
        ]
        
        self.cta_templates = [
            "DM for details!",
            "Call now for private showing!",
            "Link in bio for more info!",
            "Contact us today!",
            "Book your tour now!",
            "Don't wait - inquire now!"
        ]
        
        self.base_hashtags = [
            "#RealEstate", "#PropertyForSale", "#HomeSweetHome", "#DreamHome",
            "#RealEstateAgent", "#PropertyListing", "#HomeSearch", "#Investment"
        ]
        
        self.property_hashtags = {
            'modern': ['#ModernHome', '#ContemporaryDesign', '#ModernLiving'],
            'luxury': ['#LuxuryRealEstate', '#LuxuryHome', '#PremiumProperty'],
            'family': ['#FamilyHome', '#KidsRoom', '#FamilyFriendly'],
            'apartment': ['#ApartmentLiving', '#CondoLife', '#UrbanLiving'],
            'house': ['#HouseForSale', '#SingleFamily', '#Homeownership'],
            'kitchen': ['#ModernKitchen', '#ChefKitchen', '#KitchenGoals'],
            'bedroom': ['#MasterBedroom', '#BedroomDesign', '#RestfulSpace'],
            'bathroom': ['#LuxuryBathroom', '#SpaLikeBathroom', '#BathroomDesign'],
            'view': ['#RoomWithAView', '#ScenicViews', '#PanoramicViews'],
            'outdoor': ['#OutdoorSpace', '#Patio', '#BackyardGoals']
        }
        
        self.platform_configs = {
            'instagram': {
                'max_length': 2200,
                'hashtag_limit': 30,
                'recommended_hashtags': 20
            },
            'facebook': {
                'max_length': 63206,
                'hashtag_limit': 10,
                'recommended_hashtags': 5
            },
            'twitter': {
                'max_length': 280,
                'hashtag_limit': 10,
                'recommended_hashtags': 3
            },
            'linkedin': {
                'max_length': 3000,
                'hashtag_limit': 15,
                'recommended_hashtags': 8
            }
        }
    
    def generate_hashtags(self, description: str, platform: str = 'instagram') -> List[str]:
        config = self.platform_configs[platform]
        hashtags = self.base_hashtags.copy()
        
        description_lower = description.lower()
        
        for keyword, related_hashtags in self.property_hashtags.items():
            if keyword in description_lower:
                hashtags.extend(related_hashtags)
        
        hashtags = list(set(hashtags))
        random.shuffle(hashtags)
        
        return hashtags[:config['recommended_hashtags']]
    
    def generate_post(self, description: str, filename: str, platform: str = 'instagram') -> Dict[str, str]:
        config = self.platform_configs[platform]
        
        template = random.choice(self.post_templates)
        cta = random.choice(self.cta_templates)
        
        hashtags = self.generate_hashtags(description, platform)
        hashtag_string = ' '.join(hashtags)
        
        post_content = template.format(
            description=description,
            price_cta=cta
        )
        
        full_post = f"{post_content}\\n\\n{hashtag_string}"
        
        if len(full_post) > config['max_length']:
            available_space = config['max_length'] - len(post_content) - 4  # 4 for "\\n\\n"
            hashtag_string = hashtag_string[:available_space]
            full_post = f"{post_content}\\n\\n{hashtag_string}"
        
        return {
            'platform': platform,
            'content': full_post,
            'caption': post_content,
            'hashtags': hashtag_string,
            'image_file': filename,
            'character_count': len(full_post),
            'estimated_engagement': self._estimate_engagement(hashtags, description)
        }
    
    def _estimate_engagement(self, hashtags: List[str], description: str) -> str:
        score = len(hashtags) * 10  # Base score from hashtags
        
        engaging_words = ['luxury', 'modern', 'stunning', 'beautiful', 'spacious', 'view']
        for word in engaging_words:
            if word in description.lower():
                score += 15
        
        if score >= 200:
            return "High"
        elif score >= 150:
            return "Medium-High"
        elif score >= 100:
            return "Medium"
        else:
            return "Low-Medium"
    
    def generate_multi_platform_content(self, descriptions: Dict[str, Dict], output_file: str = 'social_media_posts.json'):
        
        platforms = ['instagram', 'facebook', 'twitter', 'linkedin']
        all_posts = {}
        
        print("📱 Generating social media content...")
        
        for filename, desc_data in descriptions.items():
            if 'error' in desc_data:
                continue
                
            description = desc_data.get('enhanced', desc_data.get('raw', ''))
            if not description:
                continue
            
            file_posts = {}
            
            for platform in platforms:
                try:
                    post = self.generate_post(description, filename, platform)
                    file_posts[platform] = post
                    print(f"  ✅ {platform.capitalize()}: {filename}")
                except Exception as e:
                    print(f"  ❌ {platform.capitalize()}: {filename} - {e}")
                    continue
            
            if file_posts:
                all_posts[filename] = file_posts
        
        output_data = {
            'generated_at': datetime.now().isoformat(),
            'total_properties': len(all_posts),
            'total_posts': sum(len(posts) for posts in all_posts.values()),
            'posts_by_property': all_posts
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\\n📄 Social media content saved to {output_file}")
        return output_data
    
    def generate_posting_schedule(self, posts_data: Dict, output_file: str = 'posting_schedule.json'):
        
        from datetime import timedelta
        
        schedule = []
        current_date = datetime.now()
        
        optimal_times = {
            'instagram': [(9, 0), (12, 0), (17, 0), (19, 0)],  # 9am, 12pm, 5pm, 7pm
            'facebook': [(9, 0), (13, 0), (15, 0)],  # 9am, 1pm, 3pm
            'twitter': [(8, 0), (12, 0), (18, 0), (20, 0)],  # 8am, 12pm, 6pm, 8pm
            'linkedin': [(8, 0), (12, 0), (17, 0)]  # 8am, 12pm, 5pm (business hours)
        }
        
        post_index = 0
        
        for property_name, platforms in posts_data['posts_by_property'].items():
            for platform, post_data in platforms.items():
                times = optimal_times.get(platform, [(12, 0)])
                time_hour, time_minute = times[post_index % len(times)]
                
                scheduled_time = current_date + timedelta(days=post_index // 4, hours=time_hour, minutes=time_minute)
                
                schedule.append({
                    'property': property_name,
                    'platform': platform,
                    'scheduled_time': scheduled_time.isoformat(),
                    'content_preview': post_data['caption'][:100] + '...',
                    'estimated_engagement': post_data['estimated_engagement']
                })
                
                post_index += 1
        
        schedule_data = {
            'created_at': datetime.now().isoformat(),
            'total_scheduled_posts': len(schedule),
            'schedule_period_days': (schedule[-1]['scheduled_time'][:10] if schedule else None),
            'schedule': schedule
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(schedule_data, f, indent=2, ensure_ascii=False)
        
        print(f"📅 Posting schedule saved to {output_file}")
        return schedule_data

def main():
    
    descriptions_file = 'descriptions/property_descriptions.json'
    
    if not os.path.exists(descriptions_file):
        print("Property descriptions not found. Run property_descriptions.py first.")
        return
    
    with open(descriptions_file, 'r', encoding='utf-8') as f:
        descriptions = json.load(f)
    
    generator = SocialMediaGenerator()
    posts_data = generator.generate_multi_platform_content(descriptions)
    
    # Generate posting schedule
    generator.generate_posting_schedule(posts_data)
    
    print(f"\\n Social media automation complete!")
    print(f"Generated content for {posts_data['total_properties']} properties")
    print(f" Total posts created: {posts_data['total_posts']}")

if __name__ == "__main__":
    main()