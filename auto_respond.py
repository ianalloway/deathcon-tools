#!/usr/bin/env python3
"""
Auto-Responder - Answers common questions about Ian
"""
import sys

# Knowledge base
QA = {
    "who are you": """I'm Ian's AI assistant. He built me to help with his data science and AI projects.

He runs Alloway LLC, is getting his MS in AI at USF, and has built multiple production ML systems.""",
    
    "what do you do": """I handle:
- Job search automation (scanning HN, applying)
- Daily briefings
- Project management
- Code reviews
- System monitoring

Ian focuses on building. I handle the busywork.""",
    
    "what projects": """Key projects:
- sports-betting-ml: NBA prediction model (68% accuracy)
- ai-advantage: Sports betting platform
- Money-maker-bot: forked from OpenClaw
- job-fit-analyzer: Resume matcher
- deathcon-bot: that's me!

Total: 40+ repos on GitHub.""",
    
    "stack": """Tech stack:
- Python, FastAPI, React, TypeScript
- XGBoost, YOLOv8, NLP
- AWS, Docker, PostgreSQL
- Claude API, local models

Focus: production ML systems.""",
    
    "experience": """Background:
- MS AI candidate at USF
- BS Information Science, Data Science
- Built production ML for sports betting, NLP, computer vision
- Full-stack dev experience
- 40+ GitHub repos""",
    
    "contact": """Ian Alloway
- Email: ian@allowayllc.com
- GitHub: github.com/ianalloway
- Blog: allowayai.substack.com
- Portfolio: ianalloway.xyz""",
    
    "education": """- MS Artificial Intelligence, USF (2024-Present)
- BS Information Science, Data Science Analytics, USF
- Various certifications: Deep Learning (Ng), ML Engineering (Google), AWS Cloud""",
    
    "skills": """Core skills:
Python, FastAPI, React, TypeScript
XGBoost, YOLOv8, NLP, Computer Vision
AWS, Docker, PostgreSQL, Redis
Claude API, local models (Ollama)
Data analysis, ML pipelines""",
}

def get_answer(question):
    q = question.lower().strip()
    
    # Direct match
    if q in QA:
        return QA[q]
    
    # Partial match
    for key in QA:
        if key in q or q in key:
            return QA[key]
    
    return "I don't have info on that. Check ianalloway.xyz or ask Ian directly."


def main():
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(get_answer(question))
    else:
        print("Auto-Responder - Ask about Ian\n")
        print("Usage: python3 auto_respond.py <question>")
        print("\nExample questions:")
        for q in QA.keys():
            print(f"  - {q}")


if __name__ == "__main__":
    main()
