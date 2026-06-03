# Forecaster Grid: Multi-Agent Stock Analysis Platform

⚡ **A premium, high-fidelity quantitative stock analysis web application built with React, Vite, TypeScript, and Ant Design (antd), backed by a FastAPI server optimized for Vercel deployment.**

Designed after the ultra-sleek, deep navy aesthetic of `forecaster.biz`, this application integrates custom layout grid telemetry, responsive area and volume charts, and conversational AI stock analysis workflows driven by the Hugging Face Inference API.

---

## 🚀 Quick Start

To launch the development servers concurrently:

1. **Install Prerequisites**:
   - Python 3.8+ installed.
   - Node.js (and `pnpm` package manager) installed.

2. **Configure Environment Variables (Optional)**:
   In the root directory, create a file named `.env` and add:
   ```ini
   # Recommended for stock quote statistics and news queries
   ALPHA_VANTAGE_API_KEY="your_alpha_vantage_key_here"

   # Recommended for AI reasoning synthesis reports
   HF_API_KEY="your_hugging_face_token_here"
   ```
   *Note: If no keys are provided, the application operates in simulation mode, utilizing dynamic hash-seeded calculations on the frontend and backend.*

3. **Run the Automated Launcher**:
   This script resolves backend and frontend dependencies, then launches both uvicorn (port 8000) and Vite (port 5173):
   ```bash
   python setup_and_run.py
   ```
   Open **`http://localhost:5173`** in your browser to interact with the workspace.

---

## 🎨 Architectural Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       React Frontend                        │
│               (Vite, TSX, Ant Design, Recharts)             │
├─────────────────────────────────────────────────────────────┤
│  Market Dashboard   │   AI Agent Chat   │ Stock Positions   │
└──────────────┬───────────────────────────────┬──────────────┘
               │ (Proxy rewrites via /api)     │
               ▼                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       FastAPI Backend                       │
│                         (Python, Uvicorn)                   │
├─────────────────────────────────────────────────────────────┤
│  Stock Telemetry    │    Dynamic Fallbacks   │ Hugging Face │
└──────────────┬──────────────────────────────────────────────┘
               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Third-Party APIs                           │
├─────────────────────────────────────────────────────────────┤
│  Alpha Vantage API (Data)   │ Hugging Face Inference (AI)   │
└─────────────────────────────────────────────────────────────┘
```

The application is structured into two main layers:
1. **Frontend (`src/`)**: A highly polished, responsive dashboard built with TypeScript and Ant Design v5's custom theme algorithm. Includes:
   - **Market Dashboard**: Sleek Area (Price) and Bar (Volume) historical Recharts, featuring themeable responsive tooltip overlays.
   - **AI Agent Chat**: A multi-agent timeline reasoning visualizer showing ticker resolved, price variance, and synthesis Analyst steps.
   - **Stock Positions Manager**: Registry for managing transactions, tracking Unrealized Gain/Loss arrows, cost basis, and hold strategies.
2. **Backend (`api/`)**: A FastAPI Python application exposed through `api/index.py` that serves telemetry and handles prompt routing. Optimised for serverless function compilation on Vercel.

---

## 🛠️ Configuration & Secrets

The server reads environment variables in priority order. You can set them locally in a `.env` file or in your Vercel project dashboard.

- **`HF_API_KEY`** (or **`HF_TOKEN`**): Hugging Face Token used to run NLP reports.
- **`ALPHA_VANTAGE_API_KEY`**: Alpha Vantage key for actual market quotes.

*If either key is unconfigured or hits rate limits, the workspace automatically falls back to consistent simulations, so it is always fully functional.*

---

## 📦 Production Vercel Deployment

This repository is pre-configured with a root `vercel.json` router. To host the project for free on Vercel:

1. Import your repository into **Vercel**.
2. Set the **Framework Preset** to **Vite**.
3. Set the **Build Command** to `pnpm run build` (or `npm run build`).
4. Set the **Output Directory** to `dist`.
5. Add your environment variables (`HF_API_KEY` and `ALPHA_VANTAGE_API_KEY`) under Vercel Project Settings.
6. Click **Deploy**. Vercel will host your static frontend and route API endpoints to Python serverless functions.