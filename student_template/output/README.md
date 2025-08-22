# Your Crawling Results

This folder is where your crawler will save all results.

## File Naming Convention

Use clear, descriptive names for your output files:

```
my_results_YYYYMMDD_HHMMSS.json          # Single crawl with timestamp
batch_ca_20241215_143022.json            # Batch crawl by state and date
batch_ca_summary_20241215_143022.csv     # Summary in CSV format
batch_ca_report_20241215_143022.txt      # Human-readable report
test_single_site.json                    # Test run results
```

## File Types You'll Create

### JSON Files (Detailed Results)
- Best for storing structured data
- Easy to read back into Python
- Good for further analysis

### CSV Files (Summary Data)
- Good for importing into Excel
- Easy to share with non-programmers
- Great for creating charts and graphs

### Text Files (Reports)
- Good for summary reports
- Easy to read
- Perfect for sharing findings

## Example Output Structure

Your JSON output should look like this:
```json
{
  "summary": {
    "total_resources": 15,
    "by_category": {
      "CONTACT_INFO": 6,
      "LOCATION": 4,
      "FACILITY": 5
    },
    "crawl_info": {
      "url": "https://www.acphd.org",
      "timestamp": "2024-12-15T14:30:00",
      "student_name": "Your Name Here"
    }
  },
  "detailed_results": {
    "resources": [
      {
        "category": "CONTACT_INFO",
        "type": "phone_number",
        "value": "510-267-8000",
        "tags": ["general"],
        "context": "general page content"
      }
    ]
  }
}
```

## Keep Your Outputs Organized

- Use consistent naming with timestamps
- Create subfolders for different assignments if needed
- Keep a log of what you've crawled
- Don't commit large output files to git (if using version control)

## Analyzing Your Results

Once you have results, you can:
- Open CSV files in Excel or Google Sheets
- Compare different counties' resource availability
- Identify which health topics are well-covered
- Track your crawler's improvement over time