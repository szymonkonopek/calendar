import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta

# Function to check if a date is in Daylight Saving Time (DST) for Poland
def is_dst(date):
    # DST in Poland: Last Sunday of March to Last Sunday of October
    # March: 31 - (31 - x) % 7 = last Sunday in March
    last_sunday_march = datetime(date.year, 3, 31) - timedelta(days=(datetime(date.year, 3, 31).weekday() + 1) % 7)
    # October: 31 - (31 - x) % 7 = last Sunday in October
    last_sunday_october = datetime(date.year, 10, 31) - timedelta(days=(datetime(date.year, 10, 31).weekday() + 1) % 7)
    
    return last_sunday_march <= date < last_sunday_october


def create_isc(id, isLecturer):
    # Step 1: Fetch the HTML content from the URL
    url = f"https://planzajec.uek.krakow.pl/index.php?typ=G&id={id}&okres=3"
    response = requests.get(url)
    response.encoding = 'utf-8'  # Set encoding to UTF-8 to handle Polish characters
    html_content = response.text

    # Step 2: Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Create a new calendar object
    calendar = Calendar()

    # Step 4: Find all table rows containing the schedule information
    table_rows = soup.find_all('tr')

    # Step 5: Iterate over each row and extract schedule details
    for row in table_rows[1:]:  # Skip the first row (headers)
        columns = row.find_all('td')
        
        if len(columns) >= 6:
            # Extract date, time, subject, type, teacher, and location
            date_str = columns[0].text.strip()
            day_time_str = columns[1].text.strip()
            subject = columns[2].text.strip()
            class_type = columns[3].text.strip()
            teacher = columns[4].text.strip() if columns[4] else "Unknown"
            location = columns[5].text.strip() if columns[5] else "Unknown"
            
            if class_type == "lektorat" and isLecturer == False:
                continue
            
            # Split day_time_str to get start time and duration
            if "(" in day_time_str:
                time_info, duration_str = day_time_str.split("(")
                duration_hours = int(duration_str.split('g')[0].strip()) * 0.75  # Extract duration

            # Parse the date and time
            start_time_str = time_info.split(' ')[1]
            start_time = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")

            # Check if the date is in DST
            if is_dst(start_time):
                # If in DST, subtract 2 hours (UTC+2)
                start_time -= timedelta(hours=2)
            else:
                # If not in DST, subtract 1 hour (UTC+1)
                start_time -= timedelta(hours=1)

            end_time = start_time + timedelta(hours=duration_hours)

            # print(f"{start_time} {end_time} - {subject} ({class_type})")

            # Step 6: Create an event and add it to the calendar
            event = Event()
            event.name = f"{subject} ({class_type})"
            event.begin = start_time
            event.end = end_time
            event.location = location
            event.description = f"Instructor: {teacher}"
            
            # Add event to calendar
            calendar.events.add(event)

    # Step 7: Save the calendar as an .ics file in the repository root
    ics_filename = f"schedules/{id}.ics"  # Update the path to the schedules folder
    with open(ics_filename, 'w', encoding='utf-8') as f:
        f.writelines(calendar)

    print(f"Calendar saved to {ics_filename}")