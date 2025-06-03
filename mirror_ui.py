import requests
import speech_recognition as sr
import pygame
import time
import os
import json
import datetime

# Load API Key
if not os.path.exists("api_key.txt"):
    print("❌ ERROR: api_key.txt not found!")
    exit()

with open("api_key.txt", "r") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    weather_api_key = lines[1].strip()

city_name = "Hyderabad"
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

# Initialize Pygame
pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Smart Mirror")
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Colors
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
BOX_COLOR = (30, 30, 30)

def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return "Weather Error"
        temp = data["main"]["temp"]
        return f"{temp:.1f}°C"
    except:
        return "Weather Error"

def split_into_lines(text, max_len=50):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        if len(current_line) + len(word) + 1 > max_len:
            lines.append(current_line)
            current_line = word
        else:
            current_line += (" " if current_line else "") + word
    if current_line:
        lines.append(current_line)
    return lines
def display_top_right_info(weather):
    now = datetime.datetime.now()
    date_text = now.strftime("%d %b %Y")
    time_text = now.strftime("%H:%M:%S")

    # Load and scale the cloud icon
    cloud_icon = pygame.image.load("cloud_icon.png")
    cloud_icon = pygame.transform.scale(cloud_icon, (24, 24))  # Adjust size for alignment

    # Draw background box
    pygame.draw.rect(screen, BOX_COLOR, (screen_width - 200, 0, 200, 120))

    # Render and display each line separately
    date_render = small_font.render(date_text, True, TEXT_COLOR)
    time_render = small_font.render(time_text, True, TEXT_COLOR)
    temp_render = small_font.render(weather, True, TEXT_COLOR)

    screen.blit(date_render, (screen_width - 190, 10))
    screen.blit(time_render, (screen_width - 190, 40))
    screen.blit(temp_render, (screen_width - 190, 70))
    screen.blit(cloud_icon, (screen_width - 190 + temp_render.get_width() + 10, 60))

    pygame.display.flip()



def display_text(input_text, output_lines):
    screen.fill(BG_COLOR)
    start_x, start_y = 20, 10
    line_height = 40
    max_width = screen_width - 200

    formatted_lines = []
    for line in input_text:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.render(test_line, True, TEXT_COLOR).get_width() > max_width:
                formatted_lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            formatted_lines.append(current_line)

    for i, text in enumerate(formatted_lines):
        y = start_y + i * line_height
        rendered = font.render(text, True, TEXT_COLOR)
        if y + line_height > screen.get_height():
            break
        screen.blit(rendered, (start_x, y))

    output_start_y = start_y + len(formatted_lines) * line_height + 10
    formatted_output_lines = []
    for line in output_lines:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.render(test_line, True, TEXT_COLOR).get_width() > max_width:
                formatted_output_lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:
            formatted_output_lines.append(current_line)

    for i, text in enumerate(formatted_output_lines):
        y = output_start_y + i * line_height
        rendered = font.render(text, True, TEXT_COLOR)
        if y + line_height > screen.get_height():
            break
        screen.blit(rendered, (start_x, y))

    weather = get_weather()
    display_top_right_info(weather)
    pygame.display.flip()

def listen_for_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        return r.recognize_google(audio, language="en-IN")
    except (sr.UnknownValueError, sr.RequestError):
        return ""

def get_gemini_response(prompt):
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text'].strip()
    except:
        return "Error in API response."

def main():
    while True:
        display_text(["Waiting for your voice input..."], [])

        query = ""
        while not query:
            query = listen_for_speech()
            if not query:
                display_text(["❌ Couldn't hear. Try again."], [])
                time.sleep(2)

        if "exit" in query.lower():
            break

        display_text(["🧑 You said:", query], [])

        full_response = get_gemini_response(query)
        summary_prompt = f"Summarize the following in 2-3 sentences:\n\n{full_response}"
        summarized_response = get_gemini_response(summary_prompt)

        response_lines = ["🤖 Gemini says:"] + split_into_lines(summarized_response)
        display_text(["🧑 You said:", query], response_lines)
        time.sleep(5)

    pygame.quit()

if __name__ == "__main__":
    main()
