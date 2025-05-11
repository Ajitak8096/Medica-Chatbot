import os
import base64
from groq import Groq

def encode_image(image_path):
    """Encode image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_query(query, encoded_image=None, model="llama3-70b-8192"):
    """Analyze query with optional image using Groq API"""
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    messages = [{
        "role": "system",
        "content": "You are a helpful medical assistant."
    }, {
        "role": "user",
        "content": query
    }]
    
    try:
        response = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing your request: {str(e)}"