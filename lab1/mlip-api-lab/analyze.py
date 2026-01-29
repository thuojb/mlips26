import json
import os
from typing import Any, Dict
from litellm import completion

# You can replace these with other models as needed but this is the one we suggest for this lab.
MODEL = "groq/llama-3.3-70b-versatile"

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY not set")

REQUIRED_KEYS = {
    "destination": str,
    "price_range": str,
    "ideal_visit_times": list,
    "top_attractions": list
}

def schema_validation(data: Dict[str, Any]) -> None:
    "Raise value error for invalid schema"
    for key, expected_type in REQUIRED_KEYS.items():
        if key not in data:
          raise ValueError(f"Missing required key: {key}")
        if not isinstance(data[key], expected_type):
          raise ValueError(f"Incorrect type for key: {key}. Expected {expected_type}, got {type(data[key])}")

def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    # implement litellm call here to generate a structured travel itinerary for the given destination

    # See https://docs.litellm.ai/docs/ for reference.
    prompt = f"""Generate a travel itinerary for the destination: {destination}. 
The output should be a JSON object with the following keys: destination, price_range, ideal_visit_times, top_attractions.
Do not include any explanations or markdowns, only return the JSON object."""  
    

    response = completion(
        model=MODEL,
        api_key=api_key,
        max_tokens=500,
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0,
        messages=[
           {"role": "user", "content": prompt},
           {"role": "system", "content": "You are a helpful travel itinerary generator."},
           {"role": "user", "content": "Please provide the itinerary in JSON format only."},
        ],
    )
    try:
        data = json.loads(response.choices[0].message['content'])
        schema_validation(data)
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Invalid response format: {e}")

    return data