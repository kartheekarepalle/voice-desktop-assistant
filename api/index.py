from flask import Flask, request, jsonify, render_template_string
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
    """Homepage with API documentation"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cutie - Voice Assistant API</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .logo {
                font-size: 48px;
                margin-bottom: 10px;
            }
            h1 {
                color: #333;
                font-size: 32px;
                margin-bottom: 10px;
            }
            .status {
                display: inline-block;
                background: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            .section {
                margin: 30px 0;
                padding: 20px;
                background: #f5f5f5;
                border-radius: 10px;
            }
            h2 {
                color: #667eea;
                font-size: 20px;
                margin-bottom: 15px;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .endpoint {
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-left: 4px solid #667eea;
                border-radius: 5px;
            }
            .method {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                margin-right: 10px;
            }
            .method.get {
                background: #61affe;
                color: white;
            }
            .method.post {
                background: #49cc90;
                color: white;
            }
            .code {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 12px;
                border-radius: 5px;
                overflow-x: auto;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                margin: 10px 0;
            }
            .commands {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }
            .command {
                background: white;
                padding: 12px;
                border-radius: 5px;
                border-left: 3px solid #764ba2;
            }
            .command-name {
                font-weight: bold;
                color: #764ba2;
            }
            .command-example {
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 14px;
            }
            .btn {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 24px;
                border-radius: 5px;
                text-decoration: none;
                margin-top: 15px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #764ba2;
            }
            @media (max-width: 600px) {
                .container {
                    padding: 20px;
                }
                h1 {
                    font-size: 24px;
                }
                .commands {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎙️</div>
                <h1>Cutie Voice Assistant API</h1>
                <div class="status">🟢 Online</div>
                <p style="color: #666; margin-top: 10px;">AI-powered voice command processing</p>
            </div>

            <div class="section">
                <h2>📡 API Endpoints</h2>
                
                <div class="endpoint">
                    <span class="method get">GET</span>
                    <strong>/api/command</strong>
                    <div class="code">GET /api/command?text=what's%20the%20time</div>
                    <p style="margin-top: 10px; color: #666;">Query parameter: <code>text</code> - the voice command to process</p>
                </div>

                <div class="endpoint">
                    <span class="method post">POST</span>
                    <strong>/api/process</strong>
                    <div class="code">POST /api/process<br>Content-Type: application/json<br><br>{"command": "tell me a joke"}</div>
                    <p style="margin-top: 10px; color: #666;">JSON body: <code>{"command": "your command here"}</code></p>
                </div>
            </div>

            <div class="section">
                <h2>🎯 Supported Commands</h2>
                <div class="commands">
                    <div class="command">
                        <div class="command-name">⏰ Time</div>
                        <div class="command-example">"what's the time"</div>
                    </div>
                    <div class="command">
                        <div class="command-name">📅 Date</div>
                        <div class="command-example">"what's the date"</div>
                    </div>
                    <div class="command">
                        <div class="command-name">😂 Joke</div>
                        <div class="command-example">"tell me a joke"</div>
                    </div>
                    <div class="command">
                        <div class="command-name">🔍 Search</div>
                        <div class="command-example">"who is Elon Musk"</div>
                    </div>
                    <div class="command">
                        <div class="command-name">🎵 Music</div>
                        <div class="command-example">"play despacito"</div>
                    </div>
                    <div class="command">
                        <div class="command-name">📱 App</div>
                        <div class="command-example">"open chrome"</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>✨ Example Response</h2>
                <div class="code">{<br>  "status": "success",<br>  "command": "what's the time",<br>  "response": "It's 06:32 PM ⏰"<br>}</div>
            </div>

            <div class="section">
                <h2>📚 Documentation</h2>
                <p style="color: #666; margin-bottom: 15px;">
                    For more information and examples, visit the project repository:
                </p>
                <a href="https://github.com/kartheekarepalle/voice-desktop-assistant" target="_blank" class="btn">
                    View on GitHub 🔗
                </a>
            </div>

            <div class="footer">
                <p>Cutie Voice Assistant API v1.0</p>
                <p style="margin-top: 5px; color: #999;">Built with Flask & Deployed on Vercel</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

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
