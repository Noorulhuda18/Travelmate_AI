# TravelMate AI 🌊

#Demo
https://travelmateai-iabxdn9owm5dw8kut4vbwy.streamlit.app/

TravelMate AI is an AI-powered tourism assistant that creates personalized travel recommendations and itineraries. It's a domain-specific chatbot — it only answers questions about travel and tourism, and politely declines anything outside that scope.

## Features

- AI-powered tourism chatbot
- Personalized itineraries
- Budget-based recommendations
- Duration-based planning
- Interest-based recommendations
- Tourism-only domain restriction
- ChatGPT-style chat interface
- API-key validation
- Streamlit frontend
- LangChain + OpenAI

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenAI
- python-dotenv

## Project Structure

```text
travelmate-ai/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variable file
├── .gitignore          # Files/folders excluded from git
└── README.md           # Project documentation
```

- **app.py** — Contains all application logic: the API key screen, the chatbot interface, the sidebar, session state management, and the domain-restricted system prompt.
- **requirements.txt** — Lists the Python packages needed to run the app.
- **.env.example** — Template showing the expected environment variable name for your OpenAI API key.
- **.gitignore** — Ensures secrets and local environment files are never committed to version control.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd travelmate-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

TravelMate AI supports two ways of providing your OpenAI API key:

1. **`.env` file** — Copy `.env.example` to `.env` and fill in your real key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   The `.env` file is listed in `.gitignore` and will never be committed.

2. **In-app entry** — On first launch, TravelMate AI shows an API key screen where you can paste your key directly. This key is only stored in the Streamlit session for the current session — it is never saved to disk or displayed on screen.

## Run

```bash
streamlit run app.py
```

## Usage

1. Open the application.
2. Enter your OpenAI API key on the first screen.
3. Click **Continue**.
4. Wait for the key to be validated.
5. Start asking travel and tourism questions.
6. Provide your destination, budget, duration, and interests (either in the chat or the sidebar) to get a personalized itinerary.

## Domain Restriction

TravelMate AI is strictly a **travel and tourism assistant**. It answers questions about destinations, itineraries, budgets, trip duration, attractions, activities, accommodation, transportation, packing, travel tips, and related topics.

Any question outside this domain (e.g. programming help, math problems, general knowledge, writing a CV) receives the following response instead of an actual answer:

> "This question is out of scope. TravelMate AI is designed specifically to help with travel and tourism-related questions."

This restriction is enforced through the system prompt sent to the model with every request.
