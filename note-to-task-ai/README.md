# Note-to-Task AI

A full-featured Streamlit app that converts natural language notes into structured, categorized to-do tasks using NLP and AI.

## Features
- Sentence splitting (spaCy)
- Date/due detection (dateparser)
- Priority, category, and deadline suggestion
- Analytics dashboard (progress, priority, category)
- Editable/deletable tasks
- Download as .txt or .pdf
- Task highlighting (overdue, due today)
- User authentication (stub)
- Google Calendar sync (stub)
- Recurring tasks & dependencies (stub)
- Voice input (stub)

## Setup
1. Install requirements:
   ```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
   ```
2. Run the app:
   ```
streamlit run app.py
   ```

## File Structure
- `app.py` — Main Streamlit app
- `utils.py` — NLP and task parsing utilities
- `dashboard.py` — Analytics dashboard
- `requirements.txt` — Dependencies
- `README.md` — This file
