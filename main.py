import json
from scripts.generate_schedule import create_isc  # Assuming this is the function that creates an ICS schedule

with open('group_folder.json', 'r', encoding='utf-8') as json_file:
    group_data = json.load(json_file)

for group_name, sub_groups in group_data.items():
    print(f"Group: {group_name}")
    isLektorat = group_name == "*Centrum Językowe*"
    for sub_group in sub_groups:
        sub_group_name = sub_group[0]  # Sub-group name
        sub_group_id = sub_group[1]    # Sub-group ID
        
        # Call create_isc with the sub_group_id
        print(f"{sub_group_name} with ID: {sub_group_id}")
        
        create_isc(sub_group_id, isLektorat)
