# PlacementAI — AI Placement Preparation Assistant

[![CI](https://github.com/ANKITJOSHI1605/AI-Placement-Assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/ANKITJOSHI1605/AI-Placement-Assistant/actions/workflows/ci.yml)
[![Live Demo](https://img.shields.io/badge/Live-Demo-43e6b1)](https://ai-placement-assistant-beryl.vercel.app)

A full-stack resume-analysis application that extracts text from PDF/TXT resumes, calculates a transparent ATS-style readiness score, compares skills against a job description, and recommends concrete improvements.

**Live application:** https://ai-placement-assistant-beryl.vercel.app  
**API:** https://ai-placement-assistant-a6uq.onrender.com  
**API documentation:** https://ai-placement-assistant-a6uq.onrender.com/docs

## Features

- PDF and TXT resume parsing (5 MB limit)
- Explainable 0–100 ATS readiness score
- Job-description skill matching
- Missing-skill and resume-structure recommendations
- Responsive React dashboard
- Privacy-focused in-memory processing; files are not stored
- FastAPI documentation at `/docs`
- Automated backend tests and CI

> The score is a rule-based preparation aid and does not reproduce any employer's proprietary ATS.

## Stack

React, Vite, FastAPI, Python, pypdf, Docker, Render and Vercel.

## Local setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

## Tests

```bash
cd backend && pytest
cd ../frontend && npm run build
```

## Production configuration

- Vercel: `VITE_API_URL=https://ai-placement-assistant-a6uq.onrender.com/api`
- Render: `CORS_ORIGINS=https://ai-placement-assistant-beryl.vercel.app`
- Render health check: `/api/health`

## API

- `GET /api/health` — service health
- `POST /api/analyze` — multipart fields: `resume` and optional `job_description`

## License

Educational portfolio project by [Ankit Joshi](https://github.com/ANKITJOSHI1605).
