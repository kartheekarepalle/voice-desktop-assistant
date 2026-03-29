# Cutie - Voice Assistant API 🎙️

A deployed AI-powered voice assistant API built with Flask and deployable on Vercel.

## Features

✅ **Voice Command Processing** – Send text commands and get intelligent responses  
✅ **Music Playback** – Play songs on YouTube  
✅ **Time & Date** – Get current time and date  
✅ **Web Search** – Search Wikipedia for information  
✅ **Jokes** – Tell jokes on demand  
✅ **App Launcher** – Open applications  
✅ **REST API** – Call via HTTP requests  
✅ **Serverless Deployment** – Deploy on Vercel  

## Tech Stack

- **Backend:** Flask (Python)
- **Deployment:** Vercel
- **Libraries:** SpeechRecognition, pyttsx3, pywhatkit, wikipedia, pyjokes

## API Endpoints

### 1. Health Check
```
GET /
```
Returns API status.

### 2. Process Command (POST)
```
POST /api/process
Content-Type: application/json

{
  "command": "play despacito"
}
```

**Example Response:**
```json
{
  "status": "success",
  "command": "play despacito",
  "response": "Playing despacito on YouTube 🎶"
}
```

### 3. Process Command (GET)
```
GET /api/command?text=what%27s%20the%20time
```

**Example Response:**
```json
{
  "status": "success",
  "command": "what's the time",
  "response": "It's 03:45 PM ⏰"
}
```

## Supported Commands

| Command | Example | Response |
|---------|---------|----------|
| Play Music | "play despacito" | Plays on YouTube |
| Get Time | "what's the time" | Returns current time |
| Get Date | "what's the date" | Returns current date |
| Tell Joke | "tell me a joke" | Returns a random joke |
| Search | "who is Elon Musk" | Wikipedia summary |
| Open App | "open chrome" | Launches application |

## Local Setup

1. **Clone Repository**
```bash
git clone https://github.com/kartheekarepalle/voice-desktop-assistant.git
cd voice-desktop-assistant
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Mac/Linux
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Locally**
```bash
python -m flask --app api.index run
```

5. **Test API**
```bash
# GET request
curl "http://localhost:5000/api/command?text=what%27s%20the%20time"

# POST request
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{"command": "tell me a joke"}'
```

## Deploy to Vercel

1. **Prerequisites**
   - Vercel account (vercel.com)
   - GitHub account with repo pushed

2. **Deploy**
   ```bash
   npm i -g vercel
   vercel
   ```

3. **Access Your API**
   ```
   https://your-project.vercel.app/api/command?text=hello
   ```

## Environment Variables

Create a `.env` file (for local development):
```
FLASK_ENV=development
FLASK_DEBUG=True
```

For Vercel, set via dashboard or:
```bash
vercel env add FLASK_ENV production
```

## Error Handling

All errors return consistent JSON responses:
```json
{
  "status": "error",
  "message": "Description of error"
}
```

## Project Structure

```
voice-desktop-assistant/
├── api/
│   └── index.py              # Flask app
├── voice-desktop-assistant/
│   └── assistant.py          # Original desktop app
├── vercel.json               # Vercel config
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .gitignore
```

## Future Enhancements

- 🎤 Add speech-to-text API endpoint
- 📝 Add response logging/analytics
- 🔐 Add authentication
- 🗣️ Support multiple languages
- 🎯 Add sentiment analysis
- 📊 Add usage dashboard

## License

MIT License

## Author

Karthik Repalle – [GitHub](https://github.com/kartheekarepalle)

---

**Live API:** [Vercel Deployment URL - Coming Soon]
