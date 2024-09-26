import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta

# Step 1: Fetch the HTML content from the URL
url = "https://planzajec.uek.krakow.pl/index.php?typ=G&id=238421&okres=2"
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
        
        # Split day_time_str to get start time and duration
        if "(" in day_time_str:
            time_info, duration_str = day_time_str.split("(")
            duration_hours = int(duration_str.split('g')[0].strip()) * 0.75  # Extract duration

        # Parse the date and time
        start_time_str = time_info.split(' ')[1]
        start_time = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(hours=duration_hours)

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
ics_filename = "schedule.ics"
with open(ics_filename, 'w', encoding='utf-8') as f:
    f.writelines(calendar)

print(f"Calendar saved to {ics_filename}")
