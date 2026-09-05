# PlacementAI — AI Placement Preparation Assistant

[![CI](https://github.com/ANKITJOSHI1605/AI-Placement-Assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/ANKITJOSHI1605/AI-Placement-Assistant/actions/workflows/ci.yml)

A full-stack resume-analysis application that extracts text from PDF/TXT resumes, calculates a transparent ATS-style readiness score, compares skills against a job description, and recommends concrete improvements.

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

## Deployment

1. Create a Render Blueprint from the repository; `render.yaml` deploys the API.
2. Deploy `frontend` on Vercel.
3. In Vercel set `VITE_API_URL=https://YOUR-API.onrender.com/api`.
4. In Render set `CORS_ORIGINS=https://YOUR-FRONTEND.vercel.app` and redeploy.

## API

- `GET /api/health` — service health
- `POST /api/analyze` — multipart fields: `resume` and optional `job_description`

## License

Educational portfolio project by [Ankit Joshi](https://github.com/ANKITJOSHI1605).
