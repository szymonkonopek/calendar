import os
import json
from scripts.generate_schedule import create_isc  # Assuming this is the function that creates an ICS schedule

def generate_isc_files(group_data, schedules_dir="schedules", resume=False):
    """
    Function to generate ISC files based on group data.
    
    :param group_data: The dictionary with groups and sub-groups.
    :param schedules_dir: Directory where .ics files are saved.
    :param resume: If True, only create new .ics files. If False, start from the beginning.
    """
    # Ensure the schedules directory exists
    if not os.path.exists(schedules_dir):
        os.makedirs(schedules_dir)

    for group_name, sub_groups in group_data.items():
        print(f"Group: {group_name}")
        isLektorat = group_name == "*Centrum Językowe*"
        
        for sub_group in sub_groups:
            sub_group_name = sub_group[0]  # Sub-group name
            sub_group_id = sub_group[1]    # Sub-group ID
            
            ics_file_path = os.path.join(schedules_dir, f"{sub_group_id}.ics")
            
            # If resuming, skip if the .ics file already exists
            if resume and os.path.exists(ics_file_path):
                print(f"Skipping {sub_group_name} with ID: {sub_group_id}, file already exists.")
                continue
            
            # Call create_isc if the file doesn't exist or resume is False
            print(f"Creating ICS for {sub_group_name} with ID: {sub_group_id}")
            create_isc(sub_group_id, isLektorat)
            
            # Log the creation
            print(f"{sub_group_name} with ID: {sub_group_id} has been processed.")

# Load the JSON file
with open('group_folder.json', 'r', encoding='utf-8') as json_file:
    group_data = json.load(json_file)

# Call the function, with the option to resume or start fresh
generate_isc_files(group_data, schedules_dir="schedules", resume=True)
