from flask import Flask, request, jsonify
import datetime
import os
import sys
import json

app = Flask(__name__)

# Configure Flask to properly handle UTF-8 and emojis
app.json.ensure_ascii = False
app.config['JSON_AS_ASCII'] = False

# Lazy load heavy dependencies to avoid import errors
try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
except:
    engine = None

# Import optional modules
try:
    import wikipedia
except:
    wikipedia = None

try:
    import pyjokes
except:
    pyjokes = None

def talk(text):
    """Convert text to speech"""
    try:
        if engine:
            engine.say(text)
            engine.runAndWait()
    except:
        pass  # Silently fail for serverless environment
    return text

def process_command(command):
    """Process voice commands and return response"""
    if not command:
        return {"status": "error", "message": "No command provided"}
    
    command = command.lower().strip()
    response = ""
    
    try:
        if "play" in command:
            song = command.replace("play", "").strip()
            response = f"Playing {song} on YouTube 🎶"
            # pywhatkit removed due to PIL dependencies
        
        elif "what" in command and "time" in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            response = f"It's {time} ⏰"
        
        elif "date" in command:
            date = datetime.datetime.now().strftime('%B %d, %Y')
            response = f"Today is {date} 📅"
        
        elif "joke" in command:
            if pyjokes:
                response = pyjokes.get_joke()
            else:
                response = "Why did the Python go to the doctor? Because it had a snake bite! 🐍"
        
        elif "search" in command or "who is" in command:
            query = command.replace("search", "").replace("who is", "").strip()
            if wikipedia:
                try:
                    result = wikipedia.summary(query, sentences=2)
                    response = f"According to Wikipedia: {result}"
                except:
                    response = f"Could not find information about {query}"
            else:
                response = f"Search for '{query}' - feature requires wikipedia module"
        
        elif "open" in command:
            app_name = command.replace("open", "").strip()
            response = f"Opening {app_name}..."
            try:
                os.startfile(app_name) if sys.platform == "win32" else os.system(f"open {app_name}")
            except:
                response = f"Could not open {app_name}"
        
        else:
            response = "I didn't understand that command. Try: play [song], what's the time, tell me a joke, or search [topic]"
    
    except Exception as e:
        response = f"Error processing command: {str(e)}"
    
    return {"status": "success", "command": command, "response": response}

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    response = jsonify({"status": "Cutie Voice Assistant API is running 🎙️", "version": "1.0"})
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/api/process', methods=['POST'])
def api_process():
    """Process voice commands via API"""
    data = request.get_json()
    command = data.get('command', '').strip() if data else ''
    
    if not command:
        response = jsonify({"status": "error", "message": "Command is required"})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    result = process_command(command)
    response = jsonify(result)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/api/command', methods=['GET'])
def api_command_get():
    """Process command via GET request"""
    command = request.args.get('text', '').strip()
    
    if not command:
        response = jsonify({"status": "error", "message": "text parameter is required"})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    
    result = process_command(command)
    response = jsonify(result)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.errorhandler(404)
def not_found(error):
    response = jsonify({"status": "error", "message": "Endpoint not found"})
    response.status_code = 404
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.errorhandler(500)
def internal_error(error):
    response = jsonify({"status": "error", "message": "Internal server error"})
    response.status_code = 500
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
