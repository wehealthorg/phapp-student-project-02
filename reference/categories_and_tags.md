# Health Resource Categories and Tags

## Main Categories

Every extracted resource should be assigned to exactly one category:

### CONTACT_INFO
Contact information for health services
- Phone numbers
- Email addresses
- Contact forms
- Fax numbers

### LOCATION  
Physical addresses and geographic information
- Street addresses
- Clinic locations
- Service areas
- Geographic boundaries

### FACILITY
Names and identifiers of healthcare facilities
- Hospital names
- Clinic names
- Pharmacy names
- Health center names

### SERVICE
Specific health services offered
- Vaccination programs
- Testing services
- Treatment programs
- Health screenings

### RESOURCE
Information and external resources
- Document links
- Website URLs
- Information pages
- Educational materials

## Health Topic Tags

Resources can have multiple tags that describe what health topics they relate to:

### Infectious Diseases
- `flu` - Influenza services, flu shots, flu information
- `covid19` - COVID-19 testing, vaccines, information
- `rsv` - Respiratory syncytial virus services
- `measles` - Measles vaccination and information
- `tuberculosis` - TB testing and treatment
- `hepatitis` - Hepatitis testing and vaccination
- `std` - Sexually transmitted disease services

### Mental Health & Substance Use
- `mental_health` - Mental health services, counseling
- `opioid_treatment` - Opioid addiction treatment programs
- `substance_abuse` - Substance abuse treatment and prevention
- `crisis_services` - Mental health crisis intervention
- `crisis_hotline` - Crisis phone lines and hotlines

### Preventive Care
- `vaccination` - General vaccination services
- `screening` - Health screenings and checkups
- `wellness_checkup` - Routine wellness visits
- `family_planning` - Reproductive health services
- `prenatal` - Prenatal and pregnancy services

### Specialized Care
- `pediatric` - Children's health services
- `dental` - Dental and oral health services
- `vision` - Eye care and vision services
- `womens_health` - Women's health services
- `senior_care` - Services for older adults
- `disability_services` - Services for people with disabilities

### Emergency Services
- `emergency_room` - Emergency room services
- `urgent_care` - Urgent care centers
- `poison_control` - Poison control information
- `emergency_services` - General emergency services

### Community Support
- `food_assistance` - Food banks, nutrition programs
- `housing_assistance` - Housing support services
- `transportation` - Medical transportation services
- `language_services` - Translation and interpretation
- `insurance_help` - Health insurance assistance

### Environmental Health
- `extreme_heat` - Heat-related health services
- `air_quality` - Air quality monitoring and alerts
- `water_safety` - Water quality and safety
- `food_safety` - Food safety inspections and information

### Healthcare Facilities
- `hospital` - Hospital facilities
- `clinic` - Clinic facilities
- `pharmacy` - Pharmacy locations
- `urgent_care_center` - Urgent care facilities
- `testing_site` - Testing locations

## Tagging Guidelines

### Be Specific
Instead of just `clinic`, also add the service type like `pediatric` or `dental`

### Use Multiple Tags
A pediatric dental clinic should have both `pediatric` and `dental` tags

### Context Matters
A phone number next to "Crisis Line" should get the `crisis_hotline` tag

### Health Topic Priority
Focus on what health services are actually offered, not just generic terms

## Tagging Examples

```python
# Flu vaccination phone number
{
    "category": "CONTACT_INFO",
    "type": "phone_number",
    "value": "555-FLU-SHOT",
    "tags": ["flu", "vaccination"],
    "context": "flu clinic appointment line"
}

# Pediatric clinic address
{
    "category": "LOCATION",
    "type": "address", 
    "value": "123 Children's Way, Anytown, CA 90210",
    "tags": ["pediatric", "wellness_checkup"],
    "context": "children's clinic location"
}

# Mental health crisis hotline
{
    "category": "CONTACT_INFO",
    "type": "phone_number",
    "value": "1-800-CRISIS-1",
    "tags": ["mental_health", "crisis_services", "crisis_hotline"],
    "context": "24/7 crisis support line"
}

# Community health center
{
    "category": "FACILITY",
    "type": "facility_name",
    "value": "Eastside Community Health Center",
    "tags": ["clinic", "community_health"],
    "context": "main facility name"
}

# Emergency room address
{
    "category": "LOCATION", 
    "type": "address",
    "value": "456 Hospital Drive, Anytown, CA 90210",
    "tags": ["emergency_room", "hospital"],
    "context": "emergency department location"
}
```

## Common Keyword Patterns

Use these patterns to help with auto-tagging:

### Flu/Influenza
- Keywords: "flu", "influenza", "flu shot", "flu vaccine", "seasonal vaccine"

### COVID-19
- Keywords: "covid", "covid-19", "coronavirus", "sars-cov-2", "covid vaccine", "covid test"

### Pediatric
- Keywords: "pediatric", "children", "kids", "infant", "child", "adolescent", "teen"

### Mental Health
- Keywords: "mental health", "behavioral health", "counseling", "therapy", "psychiatry"

### Emergency
- Keywords: "emergency", "er", "trauma", "24 hour", "24/7", "urgent"

### Crisis Services
- Keywords: "crisis", "suicide", "crisis line", "hotline", "emergency mental health"

## Auto-Tagging Implementation

```python
def auto_tag_resource(self, text, context=""):
    """Example auto-tagging function"""
    health_keywords = {
        'flu': ['flu', 'influenza', 'flu shot', 'flu vaccine'],
        'covid19': ['covid', 'covid-19', 'coronavirus'],
        'vaccination': ['vaccine', 'vaccination', 'immunization'],
        'pediatric': ['pediatric', 'children', 'kids', 'child'],
        'dental': ['dental', 'dentist', 'teeth', 'oral health'],
        'mental_health': ['mental health', 'counseling', 'therapy'],
        'emergency': ['emergency', 'er', '24 hour', 'trauma'],
        'crisis_services': ['crisis', 'suicide', 'crisis line']
    }
    
    found_tags = []
    full_text = (text + " " + context).lower()
    
    for tag, keywords in health_keywords.items():
        if any(keyword in full_text for keyword in keywords):
            found_tags.append(tag)
    
    return found_tags
```

## Quality Control

### Review Your Tags
- Do the tags make sense for the resource?
- Are you missing obvious health topics?
- Are the tags too broad or too specific?

### Common Mistakes
- Tagging everything as "general" instead of specific health topics
- Missing context clues (like "pediatric" in facility names)
- Over-tagging with irrelevant terms

### Validation Tips
- Check that phone numbers tagged as "crisis_hotline" are actually crisis lines
- Verify that "emergency" tags are for actual emergency services
- Make sure "pediatric" tags are for children's services

This categorization and tagging system helps create structured, searchable datasets that can be used for public health analysis and resource mapping.