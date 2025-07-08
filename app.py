import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
history=[]

temperature = 0.7
top_p = 0.9
top_k = 40
max_output_tokens = 2048

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

headers = {
    'Content-Type': 'application/json',
    'X-goog-api-key': api_key
}

def save_chat_to_file():
    with open(r"D:\task1\chat_log.txt","a") as f:
        for hist in history:
            f.write(hist[0]+" : ")
            f.write(hist[1]+"\n")



def send_message(message):
    content=[]
    history.append(("user",message))
    for chat in history:
        content.append({
        "role":chat[0],
        "parts": [{"text": chat[1]}]
    })
        
    payload = {
        "contents": content,
        "generationConfig": {
            "temperature": temperature,
            "topP": top_p,
            "topK": top_k,
            "maxOutputTokens": max_output_tokens
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        return "API Error"
    data = response.json()
    reply=data['candidates'][0]['content']['parts'][0]['text']
    history.append(("model",reply))
    return reply

print("Gemini Chat - Type 'exit' to save and quit ")
print(f"Settings: temp={temperature}, top_p={top_p}, top_k={top_k}, max_tokens={max_output_tokens}")
print("-" * 50)

while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() == 'exit':
        save_chat_to_file()
        print("chats saved")
        break
    else:
        print("Gemini:", send_message(user_input))