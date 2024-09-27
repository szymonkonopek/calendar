import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from datetime import datetime, timedelta

from scripts.generate_schedule import create_isc

create_isc(238421)