"""
utils.py - Utility functions for Note-to-Task AI
"""
import spacy
import dateparser
from typing import List, Dict, Any
from fpdf import FPDF

nlp = spacy.load('en_core_web_sm')

PRIORITY_KEYWORDS = {
    'high': ['urgent', 'asap', 'immediately', 'important'],
    'medium': ['soon', 'next', 'upcoming'],
    'low': ['later', 'someday', 'eventually']
}

CATEGORIES = ['Work', 'Personal', 'Academic', 'Health', 'Other']


def split_sentences(text: str) -> List[str]:
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]


def extract_date(sentence: str):
    date = dateparser.parse(sentence, settings={'PREFER_DATES_FROM': 'future'})
    return date


def detect_priority(sentence: str) -> str:
    s = sentence.lower()
    for level, keywords in PRIORITY_KEYWORDS.items():
        if any(k in s for k in keywords):
            return level.capitalize()
    return 'Medium'


def categorize_task(sentence: str) -> str:
    s = sentence.lower()
    if any(w in s for w in ['project', 'meeting', 'client', 'email']):
        return 'Work'
    if any(w in s for w in ['doctor', 'exercise', 'meditate', 'health']):
        return 'Health'
    if any(w in s for w in ['assignment', 'study', 'exam', 'class']):
        return 'Academic'
    if any(w in s for w in ['family', 'call mom', 'birthday', 'home']):
        return 'Personal'
    return 'Other'


def suggest_deadline(sentence: str) -> str:
    # Simple heuristic: if no date, suggest tomorrow for high, 3 days for medium, 7 for low
    priority = detect_priority(sentence)
    from datetime import datetime, timedelta
    if priority == 'High':
        return (datetime.now() + timedelta(days=1)).date()
    elif priority == 'Medium':
        return (datetime.now() + timedelta(days=3)).date()
    else:
        return (datetime.now() + timedelta(days=7)).date()


def parse_tasks(text: str) -> List[Dict[str, Any]]:
    sentences = split_sentences(text)
    tasks = []
    for sent in sentences:
        if len(sent) < 5:
            continue
        date = extract_date(sent)
        priority = detect_priority(sent)
        category = categorize_task(sent)
        if not date:
            date = suggest_deadline(sent)
        tasks.append({
            'task': sent,
            'due': date,
            'priority': priority,
            'category': category,
            'done': False
        })
    return tasks


def tasks_to_pdf(tasks, filename="tasks.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Note-to-Task AI - Task List", ln=True, align='C')
    pdf.ln(10)
    for i, task in enumerate(tasks, 1):
        line = f"{i}. {task['task']}\n   Due: {task['due']} | Priority: {task['priority']} | Category: {task['category']} | Status: {'Done' if task['done'] else 'Pending'}"
        pdf.multi_cell(0, 10, line)
        pdf.ln(2)
    return pdf.output(dest='S').encode('latin1')
