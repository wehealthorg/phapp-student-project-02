# Helpful Resources for Web Crawling

## Python Libraries

### Core Libraries
- **requests** - HTTP library for making web requests
  - Documentation: https://docs.python-requests.org/
  - Key features: Sessions, headers, error handling, timeouts

- **BeautifulSoup** - HTML parsing and navigation
  - Documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  - Key features: CSS selectors, tree navigation, text extraction

- **lxml** - Fast XML/HTML parser (backend for BeautifulSoup)
  - Documentation: https://lxml.de/
  - Key features: XPath support, fast parsing

- **re** (regex) - Pattern matching for text extraction
  - Documentation: https://docs.python.org/3/library/re.html
  - Tool: https://regexr.com/ (for testing patterns)

### Advanced Libraries
- **selenium** - Browser automation for JavaScript-heavy sites
- **scrapy** - Full-featured web crawling framework
- **requests-html** - JavaScript support for requests

## Regular Expression Resources

### Learning Regex
- **RegexOne Tutorial**: https://regexone.com/
- **Regex101**: https://regex101.com/ (testing and explanation)
- **RegExr**: https://regexr.com/ (visual regex builder)

### Common Patterns
```python
# Phone numbers
r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'

# Email addresses
r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# URLs
r'https?://[^\s<>"]+|www\.[^\s<>"]+'

# ZIP codes
r'\b\d{5}(?:-\d{4})?\b'
```

## CSS Selectors

### Learning CSS Selectors
- **MDN CSS Selectors**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors
- **CSS Selector Game**: https://flukeout.github.io/
- **W3Schools CSS**: https://www.w3schools.com/cssref/css_selectors.asp

### Useful Selectors
```css
/* Class selectors */
.address, .location, .contact-info

/* Element selectors */
h1, h2, h3, address, tel

/* Attribute selectors */
[class*="phone"], [id*="contact"]

/* Pseudo-selectors */
:contains("clinic"), :nth-child(2)

/* Descendant selectors */
.contact-info .phone, div.location address
```

## Browser Developer Tools

### Chrome DevTools
1. Right-click → "Inspect" or F12
2. **Elements tab**: View HTML structure, test CSS selectors
3. **Console tab**: Test JavaScript, run selector queries
4. **Network tab**: See AJAX requests and API calls

### Useful Console Commands
```javascript
// Test CSS selectors
document.querySelectorAll('.address')

// Get element text content
$('.clinic-name').textContent

// Find elements containing text
$x("//text()[contains(., 'phone')]")
```

## HTTP and Web Fundamentals

### HTTP Status Codes
- **200**: Success
- **301/302**: Redirects (follow automatically)
- **403**: Forbidden (might need better headers)
- **404**: Not found
- **429**: Rate limited (slow down requests)
- **500**: Server error

### Headers
```python
headers = {
    'User-Agent': 'Educational-Crawler/1.0',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}
```

## Debugging Techniques

### Print Debugging
```python
# Print what you're extracting
print(f"Found {len(phones)} phone numbers")
for phone in phones:
    print(f"  Phone: {phone}")

# Print soup structure
print(soup.prettify()[:500])

# Print element attributes
print(f"Element: {element.name}, Class: {element.get('class')}")
```

### File Debugging
```python
# Save HTML for offline analysis
with open('debug_page.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

# Save extraction results
with open('debug_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Common Issues and Solutions

### No Results Found
**Problem**: Your selectors aren't matching anything
**Solutions**:
- Use browser DevTools to inspect actual HTML structure
- Try broader selectors first (like 'div', 'span')
- Check if content is loaded by JavaScript
- Print the soup to see what HTML you're actually getting

### Too Many False Positives
**Problem**: Extracting irrelevant content
**Solutions**:
- Add validation functions
- Use more specific selectors
- Filter results by length, content, context
- Exclude common false positive patterns

### Getting Blocked
**Problem**: Website returns errors or blocks requests
**Solutions**:
- Add appropriate User-Agent header
- Add delays between requests (`time.sleep()`)
- Respect robots.txt
- Use session cookies if needed

### Inconsistent Results
**Problem**: Different pages have different structures
**Solutions**:
- Try multiple selector strategies
- Use try/except blocks for error handling
- Validate extracted data
- Create site-specific configurations

## Best Practices

### Ethical Crawling
1. **Read robots.txt**: Check `website.com/robots.txt`
2. **Rate limiting**: Add delays between requests
3. **Respect terms of service**: Don't violate website policies
4. **Identify yourself**: Use descriptive User-Agent
5. **Handle errors gracefully**: Don't hammer broken endpoints

### Code Organization
```python
class HealthCrawler:
    def __init__(self):
        self.session = self.setup_session()
        
    def setup_session(self):
        session = requests.Session()
        session.headers.update({'User-Agent': 'Educational-Crawler/1.0'})
        return session
    
    def extract_phones(self, soup):
        # Specific extraction logic
        pass
    
    def validate_phone(self, phone):
        # Validation logic
        pass
```

### Error Handling
```python
def safe_crawl(self, url):
    try:
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Testing Your Crawler

### Start Small
1. Test with one page first
2. Use well-known, stable websites
3. Manually verify a few extractions
4. Check edge cases (empty pages, errors)

### Validation Checklist
- [ ] Phone numbers look like actual phone numbers
- [ ] Addresses contain street names and numbers  
- [ ] Facility names are health-related
- [ ] No obvious false positives
- [ ] Handles errors gracefully
- [ ] Respects rate limits

### Test Sites
Good sites for testing (stable, public health focus):
- CDC: https://www.cdc.gov/
- Local health departments (usually stable)
- Major hospital systems
- Community health center directories

## Performance Tips

### Efficient Parsing
```python
# Use lxml parser for speed
soup = BeautifulSoup(html, 'lxml')

# Compile regex patterns once
phone_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')

# Use specific selectors instead of searching all text
phones = soup.select('.contact-phone')
```

### Memory Management
```python
# Clear large variables when done
del soup
del response

# Use generators for large datasets
def crawl_sites(urls):
    for url in urls:
        yield crawl_single_site(url)
```

## Data Management

### File Formats
- **JSON**: Best for structured data, easy to read back
- **CSV**: Good for tabular data, Excel compatibility
- **TXT**: Human-readable reports

### Data Validation
```python
def validate_results(results):
    """Validate extraction results"""
    if not results.get('resources'):
        return False, "No resources found"
    
    for resource in results['resources']:
        if not resource.get('category'):
            return False, "Missing category"
        if not resource.get('value'):
            return False, "Missing value"
    
    return True, "Valid"
```

## Getting Help

### Documentation
- Python docs: https://docs.python.org/3/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Requests: https://docs.python-requests.org/

### Community
- Stack Overflow: Tag questions with 'web-scraping', 'beautifulsoup'
- Reddit: r/learnpython, r/webscraping
- Discord: Python community servers

### Debugging Strategy
1. **Isolate the problem**: Test each component separately
2. **Check your assumptions**: Print intermediate results
3. **Start simple**: Use basic selectors first, then get specific
4. **Read error messages**: They usually tell you what's wrong
5. **Search for solutions**: Someone has probably had your problem before

## Advanced Topics

### Handling JavaScript
```python
# Using selenium for JS-heavy sites
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.quit()
```

### Session Management
```python
# Maintaining sessions for login-required sites
session = requests.Session()

# Login
login_data = {'username': 'user', 'password': 'pass'}
session.post('https://site.com/login', data=login_data)

# Now use session for authenticated requests
response = session.get('https://site.com/protected-page')
```

### Parallel Processing
```python
# Using concurrent.futures for faster crawling
from concurrent.futures import ThreadPoolExecutor

def crawl_site(url):
    # Your crawling logic
    return results

urls = ['url1', 'url2', 'url3']
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(crawl_site, urls))
```

Remember: Web crawling is both an art and a science. Each website is different, so be prepared to adapt your approach. Start simple, test thoroughly, and be respectful of the websites you're crawling!