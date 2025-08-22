"""
Batch Health Resource Crawler
Shows how to crawl multiple health departments from state CSV files
"""

import csv
import time
import json
from datetime import datetime
from categorized_example import CategorizedHealthCrawler

class BatchHealthCrawler:
    def __init__(self):
        self.crawler = CategorizedHealthCrawler()
        self.results = []
    
    def load_state_websites(self, state_code):
        """
        Load health department websites for a specific state
        
        Args:
            state_code: Two-letter state code (e.g., 'ca', 'or', 'tx')
        """
        filename = f"../data/state_websites/us-{state_code.lower()}.csv"
        websites = []
        
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    websites.append({
                        'county': row['county'],
                        'department_name': row['department_name'],
                        'website_url': row['website_url'],
                        'population': row.get('population', 'Unknown')
                    })
            
            print(f"Loaded {len(websites)} health departments for {state_code.upper()}")
            return websites
            
        except FileNotFoundError:
            print(f"File not found: {filename}")
            return []
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []
    
    def crawl_state(self, state_code, max_sites=5, delay=2):
        """
        Crawl health departments for an entire state
        
        Args:
            state_code: Two-letter state code
            max_sites: Maximum number of sites to crawl (for testing)
            delay: Seconds to wait between requests
        """
        print(f"\n=== Crawling {state_code.upper()} Health Departments ===")
        
        websites = self.load_state_websites(state_code)
        if not websites:
            return
        
        # Limit for testing/demo purposes
        websites = websites[:max_sites]
        
        for i, site in enumerate(websites, 1):
            print(f"\n[{i}/{len(websites)}] {site['county']} County")
            print(f"Department: {site['department_name']}")
            print(f"URL: {site['website_url']}")
            
            # Crawl the main page
            results = self.crawler.crawl_page_with_categories(site['website_url'])
            
            # Add metadata
            results.update({
                'county': site['county'],
                'department_name': site['department_name'],
                'population': site['population'],
                'crawled_at': datetime.now().isoformat()
            })
            
            # Store results
            self.results.append(results)
            
            # Show quick summary
            total_resources = len(results.get('resources', []))
            print(f"Found {total_resources} resources")
            
            # Be polite - wait between requests
            if i < len(websites):
                print(f"Waiting {delay} seconds...")
                time.sleep(delay)
    
    def save_results(self, filename=None):
        """
        Save crawling results to a JSON file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_crawl_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.results, file, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to {filename}")
    
    def print_summary(self):
        """
        Print a summary of all crawling results
        """
        if not self.results:
            print("No results to summarize")
            return
        
        print(f"\n=== CRAWLING SUMMARY ===")
        print(f"Total sites crawled: {len(self.results)}")
        
        total_resources = sum(len(r.get('resources', [])) for r in self.results)
        print(f"Total resources found: {total_resources}")
        
        # Count by category
        category_counts = {}
        for result in self.results:
            for resource in result.get('resources', []):
                category = resource.get('category', 'Unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\nResources by category:")
        for category, count in category_counts.items():
            print(f"  {category}: {count}")
        
        # Show which counties had the most resources
        print(f"\nTop counties by resources found:")
        county_counts = []
        for result in self.results:
            count = len(result.get('resources', []))
            county_name = result.get('county', 'Unknown')
            county_counts.append((county_name, count))
        
        county_counts.sort(key=lambda x: x[1], reverse=True)
        for county, count in county_counts[:5]:
            print(f"  {county}: {count} resources")

# Example usage
if __name__ == "__main__":
    # Create batch crawler
    batch_crawler = BatchHealthCrawler()
    
    # Crawl a few sites from California (limited for demo)
    batch_crawler.crawl_state('ca', max_sites=3, delay=2)
    
    # Show summary
    batch_crawler.print_summary()
    
    # Save results
    batch_crawler.save_results()
    
    print("\nDone! Check the generated JSON file for detailed results.")