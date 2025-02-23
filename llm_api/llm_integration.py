from openai import OpenAI
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import requests
from plant_req_api import get_plant_info 
from event_creation import *
import time
import re
from datetime import datetime, timedelta
from ics import Calendar, Event
import re

def process_plant_info(data):
    abbreviations = {
        'kingdom': 'K', 'phylum': 'P', 'class': 'C', 'order': 'O', 
        'family': 'F', 'genus': 'G', 'species': 'S', 'scientificName': 'SciName', 'rank': 'Rank', 'status': 'Status'
    }
    processed_info = []
    for record in data:
        compact_record = []

        for key, value in record.items():
            if key in abbreviations:  
                if value and value != 'None':  
                    compact_record.append(f"{abbreviations[key]}: {value}")
        processed_info.append(" | ".join(compact_record))
    context = "\n".join(processed_info)

    return context

client = OpenAI()

predicted_plant = "Zea mays"
print(get_plant_info(predicted_plant))

def get_plant_info_llm(predicted_plant):

    df_info = get_plant_info(predicted_plant)
    print(df_info)

    context = process_plant_info(df_info)

    PROMPT_INFO = f"""
    You are an expert botanist specializing in the cultivation of various crops. Below is the summarized information about the plant species in question. Based on this context, provide detailed, practical advice for a farmer who wants to grow this specific plant. The farmer may ask questions about:

    Growing Conditions: Temperature, climate zones, and seasonal considerations.
    Ideal Soil Types: Preferred soil pH, drainage, and texture.
    Watering: Best practices for watering frequency, amount, and methods.
    Sunlight: The amount of light the plant requires, along with any shade considerations.
    Pest Management: How to deal with common pests, diseases, and effective control methods.
    Plant Care: Any other maintenance tips like pruning, support, or fertilization needs.
    Harvesting: Guidelines for the optimal time and methods for harvesting the plant.
    Provide clear, actionable advice for a farmer in each of these areas based on the plant's requirements and your botanical expertise.

    If the farmer asks questions unrelated to the plant, kindly inform them that only plant-related questions can be addressed.

    Context: {context}
    """

    user_input = f'User query: Give me information about this plant: {predicted_plant}?'
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "system", "content": PROMPT_INFO},

            {"role": "user", "content": user_input}
        ]
    )

    return completion.choices[0].message.content



def make_sch_info(predicted_plant):
    start_date = '2025-02-22'
    PROMPT = f"""
    Prompt:

    "You are a crop management assistant. Given the user's planting date and crop type, generate a detailed crop growth timeline. For each growth stage, provide:

    The name of the growth stage (e.g., 'Seed Planting', 'Germination', 'Flowering', etc.).
    The duration of the stage (e.g., '7-10 days', '30-45 days').
    The start date of the stage (calculated from the user's planting date).
    The end date of the stage (calculated from the duration).
    A brief description of the activity that happens during the stage (e.g., 'Plant the seeds in well-drained soil', 'Water regularly', 'Harvest when ripe', etc.).
    The frequency of any repetitive tasks (e.g., watering, fertilizing) during the stage (e.g., "every 2 days", "weekly", "every 3 days").
    The user is planting {predicted_plant} on {start_date}. Provide the timeline for this crop in the following format:

    yaml
    Growth Stage 1:
    - Name: [name]
    - Duration: [duration]
    - Start Date: [start_date]
    - End Date: [end_date]
    - Task: [description]
    - Frequency: [watering/fertilizing frequency, if any]

    Growth Stage 2:
    - Name: [name]
    - Duration: [duration]
    - Start Date: [start_date]
    - End Date: [end_date]
    - Task: [description]
    - Frequency: [watering/fertilizing frequency, if any]

    ...
    Example Input:
    "Tomato", "2025-02-22"

    Example Output (for Tomatoes):

    yaml
    Copy
    Growth Stage 1:
    - Name: Seed Planting
    - Duration: 0-7 days
    - Start Date: 2025-02-22
    - End Date: 2025-02-29
    - Task: Plant tomato seeds in well-drained soil after the danger of frost has passed.
    - Frequency: None

    Growth Stage 2:
    - Name: Germination
    - Duration: 5-10 days
    - Start Date: 2025-02-22
    - End Date: 2025-03-04
    - Task: Tomato seeds should start sprouting in warm soil.
    - Frequency: None

    Growth Stage 3:
    - Name: Vegetative Growth
    - Duration: 10-30 days
    - Start Date: 2025-03-05
    - End Date: 2025-04-04
    - Task: Transplant seedlings to outdoor soil once they are strong enough.
    - Frequency: Every 3 days (watering)

    Growth Stage 4:
    - Name: Flowering
    - Duration: 30-70 days
    - Start Date: 2025-03-24
    - End Date: 2025-05-02
    - Task: First flowers will bloom, and fruiting begins.
    - Frequency: Every 7 days (fertilizing)

    Growth Stage 5:
    - Name: Harvesting
    - Duration: 90 days
    - Start Date: 2025-05-22
    - End Date: 2025-05-23
    - Task: Harvest tomatoes when they are firm and fully colored.
    - Frequency: None


    """

    user_input = f'User query: Give me planting timeline for this {predicted_plant}?'
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "system", "content": PROMPT},

            {"role": "user", "content": user_input}
        ]
    )
    print(completion.choices[0].message.content)
    parsed_output = parse_growth_stages(completion.choices[0].message.content)
    calendar = create_ics_calendar(parsed_output)


    with open("crop_growth_calendar.ics", "w") as my_file:
        my_file.writelines(calendar)

    return completion.choices[0].message.content

output_llm = get_plant_info_llm(predicted_plant)
# if __name__ == "__main__":
#     output_llm = get_plant_info_llm(predicted_plant)
#     print(output_llm)

