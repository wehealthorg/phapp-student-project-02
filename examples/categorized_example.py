"""
Categorized Health Resource Crawler
This example shows how to extract and categorize health resources with tags.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from datetime import datetime

class CategorizedHealthCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Educational-Health-Crawler/1.0 (Learning Purpose)'
        })
        
        # Define health topic keywords for auto-tagging
        self.health_keywords = {
            'flu': ['flu', 'influenza', 'flu shot', 'flu vaccine'],
            'covid19': ['covid', 'covid-19', 'coronavirus', 'sars-cov-2'],
            'vaccination': ['vaccine', 'vaccination', 'immunization', 'shot'],
            'mental_health': ['mental health', 'behavioral health', 'counseling', 'therapy'],
            'pediatric': ['pediatric', 'children', 'kids', 'infant', 'child'],
            'dental': ['dental', 'dentist', 'teeth', 'oral health'],
            'emergency_room': ['emergency', 'er', 'trauma', '24 hour'],
            'urgent_care': ['urgent care', 'walk-in', 'immediate care'],
            'crisis_services': ['crisis', 'suicide', 'crisis line', 'hotline'],
            'substance_abuse': ['substance', 'addiction', 'rehab', 'detox'],
            'opioid_treatment': ['opioid', 'methadone', 'suboxone', 'narcan']
        }
    
    def get_page(self, url):
        """Fetch a web page and return the soup object"""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def auto_tag_content(self, text, context_text=""):
        """
        Automatically assign tags based on keywords found in text and context
        """
        text_lower = (text + " " + context_text).lower()
        found_tags = []
        
        for tag, keywords in self.health_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                found_tags.append(tag)
        
        return found_tags
    
    def get_surrounding_context(self, element, target_text, words_around=10):
        """
        Get text context around the found element for better tagging
        """
        # Get parent element text for more context
        parent = element.parent if element.parent else element
        full_text = parent.get_text()
        
        # Find the target text and get surrounding words
        target_index = full_text.lower().find(target_text.lower())
        if target_index != -1:
            words = full_text.split()
            target_words = target_text.split()
            
            # Find approximate word position
            word_index = 0
            for i, word in enumerate(words):
                if target_words[0].lower() in word.lower():
                    word_index = i
                    break
            
            start = max(0, word_index - words_around)
            end = min(len(words), word_index + len(target_words) + words_around)
            
            return " ".join(words[start:end])
        
        return full_text[:200]  # Fallback to first 200 chars
    
    def extract_phone_with_category(self, soup):
        """
        Extract phone numbers and categorize them
        """
        results = []
        phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        
        # Look for phone numbers in different contexts
        phone_contexts = [
            ('.contact-info', 'contact information'),
            ('.emergency', 'emergency services'),
            ('.crisis', 'crisis services'),
            ('.appointment', 'appointment scheduling'),
            ('body', 'general content')
        ]
        
        for selector, context_type in phone_contexts:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text()
                phones = re.findall(phone_pattern, text)
                
                for phone in phones:
                    # Get surrounding context for better tagging
                    context = self.get_surrounding_context(element, phone)
                    tags = self.auto_tag_content(phone, context)
                    
                    # Determine specific category based on context
                    category = "CONTACT_INFO"
                    if any(tag in ['crisis_services', 'emergency_room'] for tag in tags):
                        if 'crisis' in context.lower() or 'suicide' in context.lower():
                            tags.append('crisis_hotline')
                    
                    results.append({
                        'category': category,
                        'type': 'phone_number',
                        'value': phone,
                        'tags': tags,
                        'context': context_type,
                        'confidence': 0.8
                    })
        
        return results
    
    def extract_addresses_with_category(self, soup):
        """
        Extract addresses and categorize them
        """
        results = []
        
        # Look for addresses in specific contexts
        address_selectors = [
            ('.address', 'facility_address'),
            ('.location', 'service_location'), 
            ('[itemtype*="PostalAddress"]', 'structured_address'),
            ('address', 'html_address_tag')
        ]
        
        for selector, context_type in address_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if self.looks_like_address(text):
                    # Get surrounding context
                    context = self.get_surrounding_context(element, text)
                    tags = self.auto_tag_content(text, context)
                    
                    results.append({
                        'category': 'LOCATION',
                        'type': 'address',
                        'value': text,
                        'tags': tags,
                        'context': context_type,
                        'confidence': 0.7
                    })
        
        return results
    
    def extract_facilities_with_category(self, soup):
        """
        Extract facility names and categorize them
        """
        results = []
        
        # Look for facility names in headings and specific elements
        facility_selectors = [
            ('h1, h2, h3', 'heading'),
            ('.facility-name', 'explicit_facility'),
            ('.clinic-name', 'clinic_listing'),
            ('.location-name', 'location_listing')
        ]
        
        for selector, context_type in facility_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if self.looks_like_facility_name(text):
                    context = self.get_surrounding_context(element, text)
                    tags = self.auto_tag_content(text, context)
                    
                    # Add facility-specific tags
                    text_lower = text.lower()
                    if 'hospital' in text_lower:
                        tags.append('hospital')
                    elif 'clinic' in text_lower:
                        tags.append('clinic')
                    elif 'pharmacy' in text_lower:
                        tags.append('pharmacy')
                    
                    results.append({
                        'category': 'FACILITY',
                        'type': 'facility_name',
                        'value': text,
                        'tags': tags,
                        'context': context_type,
                        'confidence': 0.6
                    })
        
        return results
    
    def looks_like_address(self, text):
        """Check if text looks like an address"""
        street_words = ['street', 'st', 'avenue', 'ave', 'road', 'rd', 
                       'boulevard', 'blvd', 'drive', 'dr', 'lane', 'ln']
        
        text_lower = text.lower()
        has_number = any(char.isdigit() for char in text)
        has_street_word = any(word in text_lower for word in street_words)
        
        return has_number and has_street_word and len(text) > 10
    
    def looks_like_facility_name(self, text):
        """Check if text looks like a healthcare facility name"""
        health_keywords = ['clinic', 'hospital', 'medical', 'health', 'center', 
                          'pharmacy', 'dental', 'care', 'urgent', 'family']
        
        text_lower = text.lower()
        has_health_keyword = any(keyword in text_lower for keyword in health_keywords)
        is_reasonable_length = 5 < len(text) < 100
        
        return has_health_keyword and is_reasonable_length
    
    def crawl_page_with_categories(self, url):
        """
        Main function to crawl a page and extract categorized resources
        """
        soup = self.get_page(url)
        if not soup:
            return {}
        
        # Extract all categorized resources
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'resources': []
        }
        
        # Add all extracted resources
        results['resources'].extend(self.extract_phone_with_category(soup))
        results['resources'].extend(self.extract_addresses_with_category(soup))
        results['resources'].extend(self.extract_facilities_with_category(soup))
        
        return results
    
    def print_categorized_results(self, results):
        """
        Pretty print categorized results
        """
        print(f"\n--- Categorized Results for {results['url']} ---")
        print(f"Crawled at: {results['timestamp']}")
        
        # Group by category
        by_category = {}
        for resource in results['resources']:
            category = resource['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(resource)
        
        for category, items in by_category.items():
            print(f"\n📋 {category} ({len(items)} items):")
            for item in items:
                tags_str = ", ".join(item['tags']) if item['tags'] else "general"
                print(f"  • {item['value']}")
                print(f"    Tags: {tags_str}")
                print(f"    Confidence: {item['confidence']}")
        
        if not results['resources']:
            print("  No categorized resources found.")
    
    def save_results(self, results, filename=None):
        """Save results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"categorized_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results saved to: {filename}")

# Example usage
if __name__ == "__main__":
    crawler = CategorizedHealthCrawler()
    
    # Test with a health department page
    test_url = "https://www.cdc.gov/flu/treatment/index.html"
    
    results = crawler.crawl_page_with_categories(test_url)
    crawler.print_categorized_results(results)
    crawler.save_results(results)