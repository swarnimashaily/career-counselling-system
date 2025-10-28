# Career Counselling GenAI Platform

This project provides a lightweight GenAI-inspired platform that guides students who are unsure about their next steps. It combines a structured questionnaire with a narrative recommendation engine to produce actionable career guidance.

## Features

- **Interactive questionnaire** that captures motivations, strengths, and preferred environments.
- **Rule-based generative engine** that synthesizes answers into tailored career stories.
- **FastAPI service** exposing endpoints to fetch questions and receive guidance.
- **Practical recommendations** including starter projects and curated learning resources.

## Getting Started

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the API server

```bash
uvicorn app:app --reload
```

The server will start at `http://127.0.0.1:8000`. Use the interactive docs at `/docs` to try the endpoints.

### 3. Example usage

1. Fetch the questionnaire:
   ```bash
   curl http://127.0.0.1:8000/questionnaire
   ```
2. Submit responses:
   ```bash
   curl -X POST http://127.0.0.1:8000/evaluate \
        -H "Content-Type: application/json" \
        -d '{
              "learner_name": "Avery",
              "responses": {
                  "strength": "analytical",
                  "values": "innovation",
                  "environment": "independent",
                  "learning": "courses"
              }
            }'
   ```
3. Receive a narrative report with recommended career directions, project ideas, and reflection prompts.

## Project Structure

```
career_counselling/
├── __init__.py                # Package entry point
├── engine.py                  # Core evaluation logic and recommendation data
├── genai.py                   # Narrative report generation helpers
└── questionnaire.py           # Questionnaire definition and validation
app.py                         # FastAPI application
requirements.txt               # Python dependencies
```

## Extending the Platform

- Add more questions or traits by updating `questionnaire.py`.
- Append new career paths or resources inside `_build_career_library()` in `engine.py`.
- Customize the narrative format in `genai.py` to match your branding or tone.

Feel free to build a front-end, integrate with your preferred LLM provider, or connect the evaluation to student information systems.
