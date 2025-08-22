# Health Resource Crawler Assignment Guide

## Overview

Build a web crawler that extracts public health resources from health department websites, categorizes them, and saves structured data for analysis.

## Learning Objectives

- Understand web scraping fundamentals
- Practice regular expressions and HTML parsing
- Learn data categorization and tagging
- Build batch processing workflows
- Create structured datasets

## Assignment Structure

### Part 1: Basic Crawler (`my_crawler.py`)

**Goal:** Extract basic health resources from a single website

**Tasks:**
1. Set up HTTP session with appropriate headers
2. Fetch and parse HTML content
3. Extract phone numbers using regex
4. Extract addresses using CSS selectors
5. Extract facility names from headings
6. Save results to JSON file

**Getting Started:**
```python
# Example regex for phone numbers
phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
phones = re.findall(phone_pattern, text)

# Example CSS selectors for addresses
address_elements = soup.select('.address')
for element in address_elements:
    address = element.get_text(strip=True)
```

### Part 2: Categorization and Tagging

**Goal:** Classify extracted resources with categories and health topic tags

**Categories:**
- **CONTACT_INFO**: Phone numbers, emails
- **LOCATION**: Addresses, geographic areas
- **FACILITY**: Clinic names, hospital names

**Health Topic Tags:**
- `flu`, `covid19`, `vaccination`
- `pediatric`, `dental`, `mental_health`
- `emergency`, `urgent_care`, `crisis_services`

**Implementation:**
```python
def auto_tag_resource(self, text, context=""):
    """Assign health topic tags based on keywords"""
    found_tags = []
    health_keywords = {
        'flu': ['flu', 'influenza', 'flu shot'],
        'pediatric': ['children', 'kids', 'pediatric']
    }
    
    full_text = (text + " " + context).lower()
    for tag, keywords in health_keywords.items():
        if any(keyword in full_text for keyword in keywords):
            found_tags.append(tag)
    
    return found_tags
```

### Part 3: Batch Processing (`my_batch_crawler.py`)

**Goal:** Process multiple health department websites from state CSV files

**Tasks:**
1. Load website list from CSV file
2. Loop through websites with error handling
3. Add delays between requests (be polite!)
4. Collect and aggregate results
5. Generate summary statistics
6. Save detailed and summary reports

**CSV File Format:**
```csv
county,department_name,website_url,population
Alameda,Alameda County Public Health,https://www.acphd.org,1671329
```

**Batch Processing Pattern:**
```python
def crawl_multiple_sites(self, websites, max_sites=5):
    results = []
    for i, site in enumerate(websites[:max_sites]):
        print(f"Crawling {site['county']} County...")
        
        # Crawl the site
        site_results = self.crawler.crawl_page(site['website_url'])
        
        # Add metadata
        site_results['county'] = site['county']
        site_results['department_name'] = site['department_name']
        
        results.append(site_results)
        
        # Be polite - wait between requests
        time.sleep(2)
    
    return results
```

## Step-by-Step Instructions

### Step 1: Environment Setup
```bash
# Install required packages
pip install requests beautifulsoup4 lxml

# Test your setup
python -c "import requests, bs4; print('Setup successful!')"
```

### Step 2: Start with Simple Extraction
1. Open `my_crawler.py`
2. Complete the `get_page()` method
3. Test with a simple website
4. Add phone number extraction
5. Test and debug

### Step 3: Add More Extraction Types
1. Add address extraction using CSS selectors
2. Add facility name extraction
3. Test with different health department sites
4. Handle edge cases and errors

### Step 4: Implement Categorization
1. Define your health keyword dictionary
2. Implement auto-tagging function
3. Categorize each extracted resource
4. Test tagging accuracy

### Step 5: Build Batch Processor
1. Complete CSV loading function
2. Add batch crawling loop
3. Implement error handling
4. Add progress reporting
5. Test with small batches first

### Step 6: Generate Reports
1. Calculate summary statistics
2. Group results by category and tag
3. Identify top-performing counties
4. Create human-readable reports

## Testing Strategy

### Start Small
- Test with 1-2 websites first
- Use well-known, stable sites (CDC, major health departments)
- Verify extraction accuracy manually

### Progressive Testing
1. Single site → Multiple sites
2. Simple extraction → Categorized extraction
3. Manual testing → Automated validation

### Error Handling
```python
try:
    results = crawler.crawl_page(url)
except requests.RequestException as e:
    print(f"Error crawling {url}: {e}")
    results = {}  # Return empty results, continue processing
```

## Expected Output

### Single Site Results
```json
{
  "url": "https://www.acphd.org",
  "timestamp": "2024-12-15T14:30:00",
  "resources": [
    {
      "category": "CONTACT_INFO",
      "type": "phone_number",
      "value": "510-267-8000",
      "tags": ["general"],
      "confidence": 0.8
    },
    {
      "category": "LOCATION", 
      "type": "address",
      "value": "1000 San Leandro Blvd, San Leandro, CA",
      "tags": ["general"],
      "confidence": 0.7
    }
  ]
}
```

### Batch Results Summary
```
=== CRAWLING SUMMARY ===
Total sites crawled: 5
Total resources found: 47

Resources by category:
  CONTACT_INFO: 18
  LOCATION: 12
  FACILITY: 17

Top counties by resources found:
  Alameda: 15 resources
  San Francisco: 12 resources
  Contra Costa: 10 resources
```

## Grading Criteria
The final data package deliverable will be graded using the following criteria

### Basic Requirements (70%)
- [ ] Extracts phone numbers correctly
- [ ] Extracts addresses correctly
- [ ] Extracts facility names correctly
- [ ] Saves results to JSON file
- [ ] Handles basic errors gracefully

### Advanced Features (20%)
- [ ] Implements categorization system
- [ ] Adds health topic tagging
- [ ] Processes multiple sites in batch
- [ ] Generates summary reports

### Code Quality (10%)
- [ ] Well-commented code
- [ ] Follows naming conventions
- [ ] Proper error handling
- [ ] Organized file structure

## Common Challenges and Solutions

### Challenge: No results found
**Solution:** Check your regex patterns and CSS selectors. Different sites use different HTML structures.

### Challenge: Too many false positives
**Solution:** Add validation functions to filter results. For example, check if "phone numbers" actually look like phone numbers.

### Challenge: Sites blocking requests
**Solution:** Add appropriate headers, delays between requests, and respect robots.txt.

### Challenge: Complex HTML structures
**Solution:** Use your browser's developer tools to inspect HTML. Look for patterns in class names and element structure.

## Extension Ideas

Once you complete the basic assignment:

1. **Geographic Analysis**: Use a geocoding service to map addresses
2. **Service Coverage**: Analyze which health topics are well-covered vs. underserved
3. **Website Quality**: Score sites based on completeness of information
4. **Trend Analysis**: Track changes in health resources over time
5. **API Integration**: Connect to other health databases for comparison

## Resources

- **Python Documentation**: https://docs.python.org/3/
- **Beautiful Soup Documentation**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Regular Expressions Tutorial**: https://regexr.com/
- **CSS Selectors Reference**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors

## Getting Help

1. **Check the examples** in `../examples/` - they show working implementations
2. **Read the reference materials** in `../reference/`
3. **Start with small tests** - don't try to crawl 100 sites at once
4. **Ask specific questions** - "My regex isn't matching" is better than "it doesn't work"
5. **Share your code** - your instructor can help debug specific issues

Good luck building your health resource crawler!