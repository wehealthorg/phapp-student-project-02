import csv
from collections import defaultdict

input_file = 'US.csv'
columns = ['name', 'parent_id', 'community_id', 'category', 'pha', 'population_proper', 'state_id', 'pha_url']
rows_by_state = defaultdict(list)

with open(input_file, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    
    for row_num, row in enumerate(reader, start=2):  # Start at 2 since row 1 is header
        # Convert to string and strip whitespace to handle any data type issues
        state = str(row.get('state_id', '')).strip()
        name = str(row.get('name', '')).strip()
        
        # Debug: Print rows with empty names
        if not name or name == 'None':
            print(f"Row {row_num}: Empty name found - state_id: '{state}', community_id: '{row.get('community_id', '')}'")
            continue  # Skip rows with empty names entirely
        
        if state and state != 'None' and name and name != 'None':
            # Convert all values to strings and strip whitespace
            filtered_row = {col: str(row.get(col, '')).strip() for col in columns}
            rows_by_state[state].append(filtered_row)
            print(f"Row {row_num}: Added - name: '{name}', state: '{state}'")
        else:
            print(f"Row {row_num}: Skipping - name: '{name}', state: '{state}'")

# Write output files
for state, rows in rows_by_state.items():
    if not rows:  # Skip if no valid rows for this state
        print(f"No valid rows found for state: {state}")
        continue
        
    output_file = f'us-{state.lower()}.csv'
    print(f"Writing {len(rows)} rows to {output_file}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=columns, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

print("Processing complete!")