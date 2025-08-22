# Common Extraction Patterns

## Regular Expression Patterns

### Phone Numbers

```python
# Basic US phone number patterns
phone_patterns = [
    r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',    # 555-123-4567, 555.123.4567, 555 123 4567
    r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',        # (555) 123-4567, (555)123-4567
    r'\b1[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 1-555-123-4567
    r'\d{3}-\d{3}-\d{4}',                    # 555-123-4567 (strict)
]

# Toll-free patterns
toll_free_patterns = [
    r'\b1?[-.\s]?800[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 1-800-123-4567
    r'\b1?[-.\s]?888[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 1-888-123-4567
    r'\b1?[-.\s]?877[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 1-877-123-4567
]

# Example usage
import re
text = "Call us at (555) 123-4567 or 1-800-HEALTH"
phones = []
for pattern in phone_patterns:
    phones.extend(re.findall(pattern, text))
```

### Email Addresses

```python
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Example
emails = re.findall(email_pattern, text)
```

### Addresses

```python
# Street address patterns (US)
address_patterns = [
    # Basic street address: 123 Main St
    r'\d+\s+[A-Za-z0-9\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct|Circle|Cir|Place|Pl)\b',
    
    # Address with city, state, zip: 123 Main St, Anytown, CA 90210
    r'\b\d+\s+[A-Za-z0-9\s,]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\b',
    
    # PO Box patterns
    r'\bP\.?O\.?\s+Box\s+\d+\b',
]
```

## CSS Selectors

### Common Address Selectors

```python
address_selectors = [
    '.address',
    '.location',
    '.contact-info',
    '.facility-address',
    '.clinic-location',
    '[itemtype*="PostalAddress"]',  # Schema.org structured data
    'address',  # HTML5 address element
    '.vcard .adr',  # Microformat addresses
    '.location-info',
    '.contact-details',
]
```

### Facility Name Selectors

```python
facility_selectors = [
    'h1', 'h2', 'h3',  # Main headings
    '.facility-name',
    '.clinic-name',
    '.hospital-name',
    '.location-name',
    '.facility-title',
    '.organization-name',
    '[itemtype*="Organization"] .name',
    '.clinic-title',
    '.medical-facility',
]
```

### Contact Information Selectors

```python
contact_selectors = [
    '.contact-info',
    '.contact-details',
    '.phone',
    '.telephone',
    '.contact-phone',
    '.clinic-phone',
    '[itemtype*="ContactPoint"]',
    'tel:',  # Look for tel: links
    '.emergency-contact',
]
```

## XPath Patterns

### Finding Text Near Keywords

```python
from lxml import html

# Find text containing "phone" followed by numbers
xpath_phone = "//text()[contains(translate(., 'PHONE', 'phone'), 'phone')]/following::text()[matches(., '\d{3}')][1]"

# Find addresses near "located at" or "address"
xpath_address = "//text()[contains(translate(., 'ADDRESS', 'address'), 'address')]/following::text()[1]"
```

## Context-Aware Extraction

### Getting Surrounding Context

```python
def get_context_around_element(element, words_before=5, words_after=5):
    """
    Get text context around a BeautifulSoup element
    """
    # Get parent element for more context
    parent = element.parent if element.parent else element
    
    # Get all text from parent
    full_text = parent.get_text()
    
    # Split into words
    words = full_text.split()
    
    # Find target text position
    target_text = element.get_text()
    target_words = target_text.split()
    
    # Find where target appears in parent text
    for i, word in enumerate(words):
        if target_words[0].lower() in word.lower():
            start = max(0, i - words_before)
            end = min(len(words), i + len(target_words) + words_after)
            return " ".join(words[start:end])
    
    return full_text[:200]  # Fallback
```

### Finding Services by Context

```python
def find_services_by_context(soup):
    """
    Find services mentioned near keywords
    """
    service_keywords = ['services', 'offers', 'provides', 'available']
    services = []
    
    for keyword in service_keywords:
        # Find elements containing service keywords
        elements = soup.find_all(text=re.compile(keyword, re.I))
        
        for element in elements:
            # Get the parent element
            parent = element.parent
            
            # Look for lists or structured content nearby
            service_lists = parent.find_next_siblings(['ul', 'ol', 'div'])
            
            for service_list in service_lists:
                # Extract service items
                items = service_list.find_all(['li', 'p', 'span'])
                for item in items:
                    service_text = item.get_text(strip=True)
                    if len(service_text) > 5 and len(service_text) < 100:
                        services.append(service_text)
    
    return services
```

## Validation Patterns

### Phone Number Validation

```python
def validate_phone_number(phone):
    """
    Validate that extracted text is actually a phone number
    """
    # Remove all non-digit characters
    digits_only = re.sub(r'\D', '', phone)
    
    # Check length (US numbers)
    if len(digits_only) == 10:
        return True
    elif len(digits_only) == 11 and digits_only[0] == '1':
        return True
    
    return False
```

### Address Validation

```python
def validate_address(address):
    """
    Basic address validation
    """
    address_lower = address.lower()
    
    # Must contain a number
    if not any(char.isdigit() for char in address):
        return False
    
    # Must contain street words
    street_words = ['street', 'st', 'avenue', 'ave', 'road', 'rd', 
                   'boulevard', 'blvd', 'drive', 'dr', 'lane', 'ln']
    if not any(word in address_lower for word in street_words):
        return False
    
    # Reasonable length
    if len(address) < 10 or len(address) > 200:
        return False
    
    # Exclude common false positives
    exclude_words = ['copyright', 'website', 'email', 'phone']
    if any(word in address_lower for word in exclude_words):
        return False
    
    return True
```

### Facility Name Validation

```python
def validate_facility_name(name):
    """
    Check if text looks like a healthcare facility name
    """
    name_lower = name.lower()
    
    # Must contain health-related keywords
    health_keywords = ['clinic', 'hospital', 'medical', 'health', 'center', 
                      'pharmacy', 'dental', 'care', 'urgent', 'family',
                      'community', 'wellness', 'pediatric']
    
    if not any(keyword in name_lower for keyword in health_keywords):
        return False
    
    # Reasonable length
    if len(name) < 5 or len(name) > 100:
        return False
    
    # Exclude navigation/UI elements
    exclude_words = ['menu', 'navigation', 'footer', 'header', 'login',
                    'search', 'home', 'about', 'contact', 'privacy']
    if any(word in name_lower for word in exclude_words):
        return False
    
    return True
```

## Common False Positives

### Phone Numbers
- Copyright notices: "© 2024"
- Version numbers: "Version 1.2.3.4567"
- Dates: "12/31/2024"
- File sizes: "123.456.7890 MB"

### Addresses
- Website URLs: "Visit www.example.com/about"
- Email signatures
- Copyright text
- Navigation breadcrumbs

### Facility Names
- Page titles and headers
- Navigation menu items
- Footer text
- Button labels

## Site-Specific Patterns

### Government Health Departments

```python
gov_selectors = {
    'phone': ['.contact-phone', '.office-phone', '.main-number'],
    'address': ['.office-address', '.location-address', '.facility-location'],
    'facilities': ['.facility-name', '.office-name', '.department-name']
}
```

### Hospital Systems

```python
hospital_selectors = {
    'phone': ['.hospital-phone', '.patient-info', '.contact-number'],
    'address': ['.hospital-address', '.campus-location', '.facility-address'],
    'facilities': ['.hospital-name', '.medical-center', '.campus-name']
}
```

### Community Health Centers

```python
clinic_selectors = {
    'phone': ['.clinic-phone', '.appointment-phone', '.main-line'],
    'address': ['.clinic-address', '.center-location', '.site-address'],
    'facilities': ['.clinic-name', '.health-center', '.community-clinic']
}
```

## Dynamic Content Handling

### JavaScript-Rendered Content

```python
# For sites that load content with JavaScript, you might need:
# - Selenium WebDriver
# - requests-html
# - Splash

# Example with requests-html
from requests_html import HTMLSession

session = HTMLSession()
r = session.get(url)
r.html.render()  # Execute JavaScript
soup = BeautifulSoup(r.html.html, 'html.parser')
```

### AJAX Content

```python
# Look for AJAX endpoints in network tab
# Often data is available as JSON at specific URLs
import json

# Example: many sites have JSON endpoints
json_url = "https://example.com/api/locations.json"
response = requests.get(json_url)
data = response.json()

# Extract from JSON instead of HTML
for location in data['locations']:
    print(f"Name: {location['name']}")
    print(f"Phone: {location['phone']}")
    print(f"Address: {location['address']}")
```

## Error Handling Patterns

```python
def safe_extract_phone(text):
    """
    Safely extract phone numbers with error handling
    """
    try:
        pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        matches = re.findall(pattern, text)
        
        # Validate each match
        valid_phones = []
        for match in matches:
            if validate_phone_number(match):
                valid_phones.append(match)
        
        return valid_phones
        
    except Exception as e:
        print(f"Error extracting phones: {e}")
        return []

def safe_select_elements(soup, selector):
    """
    Safely select elements with error handling
    """
    try:
        return soup.select(selector)
    except Exception as e:
        print(f"Error with selector '{selector}': {e}")
        return []
```

These patterns provide a solid foundation for extracting health resources from various types of websites. Remember to always validate your extractions and handle errors gracefully!
