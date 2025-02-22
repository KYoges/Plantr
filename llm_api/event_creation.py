import re
from datetime import datetime

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

