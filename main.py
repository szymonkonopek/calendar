import json
import argparse
from scripts.generate_schedule import generate_isc_files, generate_isc_files_lecturer

from dotenv import load_dotenv
load_dotenv()

# Set up argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate schedule ICS files.")
    parser.add_argument(
        '--resume',
        type=bool,
        default=False,
        help='Pass true to resume from the last state, false to start fresh (default: false).'
    )
    return parser.parse_args()

# Main function to execute the script logic
def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    # Load the JSON file
    with open('group_folder.json', 'r', encoding='utf-8') as json_file:
        group_data = json.load(json_file)

    # Generate ICS files, passing the resume argument from the command line
    generate_isc_files(group_data, schedules_dir="schedules", resume=args.resume)

    with open('lecturer_folder.json', 'r', encoding='utf-8') as json_file:
        lecturer_data = json.load(json_file)   

    # Generate ICS files for lecturers, passing the resume argument from the command line
    generate_isc_files_lecturer(lecturer_data, schedules_dir="schedules_lecturers", resume=args.resume)

# Run the script
if __name__ == "__main__":
    main()
