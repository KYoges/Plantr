import re
from datetime import datetime, timedelta
from ics import Calendar, Event
import re


def parse_growth_stages(text):
    stages = {}
    
    growth_stages = text.strip().split("\n\n") 
    
    for stage in growth_stages:
        match = re.match(r"Growth Stage (\d+):", stage)
        if match:
            stage_number = int(match.group(1))
            stage_data = {}

            name_match = re.search(r"- Name: (.+)", stage)
            duration_match = re.search(r"- Duration: (.+)", stage)
            start_date_match = re.search(r"- Start Date: (.+)", stage)
            end_date_match = re.search(r"- End Date: (.+)", stage)
            task_match = re.search(r"- Task: (.+)", stage)
            frequency_match = re.search(r"- Frequency: (.+)", stage)
            
            if name_match:
                stage_data["name"] = name_match.group(1)
            if duration_match:
                stage_data["duration"] = duration_match.group(1)
            if start_date_match:
                stage_data["start_date"] = datetime.strptime(start_date_match.group(1), "%Y-%m-%d")
            if end_date_match:
                stage_data["end_date"] = datetime.strptime(end_date_match.group(1), "%Y-%m-%d")
            if task_match:
                stage_data["task"] = task_match.group(1)
            if frequency_match:
                stage_data["frequency"] = frequency_match.group(1)
            else:
                stage_data["frequency"] = "None" 
            
            stages[stage_number] = stage_data
    
    return stages


def convert_frequency_to_recurrence(frequency, start_date, end_date):
    recurrence = []
    
    if 'Water' in frequency or 'fertilize' in frequency:
        interval = int(re.search(r'(\d+)', frequency).group(1))
        
        if 'day' in frequency:
            freq = 'daily'
            recurrence.append({
                'freq': freq,
                'interval': interval,
                'start_date': start_date,
                'end_date': end_date
            })
        elif 'week' in frequency:
            freq = 'weekly'
            recurrence.append({
                'freq': freq,
                'interval': interval,
                'start_date': start_date,
                'end_date': end_date
            })
    return recurrence

def create_ics_calendar(crop_stages):
    calendar = Calendar()

    for stage_id, stage in crop_stages.items():
        # Create an event for the growth stage
        event = Event()
        event.name = stage['name']
        event.begin = stage['start_date'].isoformat()
        event.end = stage['end_date'].isoformat()
        event.description = stage['task']
        
        calendar.events.add(event)

        if 'Water' in stage['frequency'] or 'fertilize' in stage['frequency']:
            recurrence = convert_frequency_to_recurrence(stage['frequency'], stage['start_date'], stage['end_date'])
            
            for rec in recurrence:
                recurring_event = Event()
                recurring_event.name = f"Watering - {stage['name']}"
                recurring_event.begin = rec['start_date'].isoformat()
                recurring_event.end = rec['end_date'].isoformat()
                recurring_event.description = f"Water the crop every {rec['interval']} days"
                
                recurring_event.make_all_day()
                
                calendar.events.add(recurring_event)
    
    return calendar



