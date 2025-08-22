# Health Department Website Data

## Website Files

Each `us-{state}.csv` file contains local health department websites for that state.

### CSV Format
```csv
county,department_name,website_url,population,last_updated
Alameda,Alameda County Public Health Department,https://www.acphd.org,1671329,2024-01-15
Los Angeles,Los Angeles County Department of Public Health,http://publichealth.lacounty.gov,10014009,2024-01-15
```

### Available States
- `us-ca.csv` - California (58 counties)
- `us-or.csv` - Oregon (36 counties) 
- `us-tx.csv` - Texas (254 counties)

### Usage in Your Crawler
```python
import csv

# Load a state's health departments
with open('data/state_websites/us-ca.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"Crawling {row['department_name']}: {row['website_url']}")
```

## Notes
- Some websites may be offline or have changed URLs
- Always test with a small sample first
- Respect rate limits when crawling multiple sites