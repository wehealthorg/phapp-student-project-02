# Sample Output Examples

This folder contains example outputs from the health resource crawler to show students what their results should look like.

## File Types

### single_site_example.json
Example output from crawling a single health department website with categorized resources.

### batch_crawl_example.json  
Example output from batch crawling multiple counties in a state.

### summary_report_example.txt
Example human-readable summary report from a batch crawl.

## Using These Examples

1. **Compare your output** - Make sure your JSON structure matches
2. **Check categorization** - Verify your categories and tags are similar
3. **Validate completeness** - See what types of resources should be found
4. **Format reference** - Use for consistent naming and structure

## Quality Expectations

Your results should include:
- Proper categorization (CONTACT_INFO, LOCATION, FACILITY)
- Relevant health topic tags
- Clean, validated data (no obvious false positives)
- Metadata (timestamps, source URLs, confidence scores)
- Summary statistics

## Output Standards

- Use ISO format timestamps
- Include confidence scores (0.0-1.0)
- Provide context for each extraction
- Remove duplicate entries
- Validate phone numbers and addresses