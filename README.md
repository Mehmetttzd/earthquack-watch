# 🌍 QuakeWatch — Global Earthquake Monitoring Dashboard

**QuakeWatch** is a full-stack web application that provides a real-time view of worldwide earthquake activity using authoritative data from the **USGS Earthquake Hazards Program**.

Beyond the UI, this project was intentionally built to demonstrate **production-grade QA automation**, including Selenium UI testing, resilient test design for live data, and CI-ready reporting.

---

## 🎯 Project Goals

- Present **live, global earthquake data** in a clear, government-style dashboard  
- Support filtering by **time window**, **minimum magnitude**, and **result limits**  
- Demonstrate **real-world UI automation** against a React application with dynamic data  
- Build a QA suite that is **stable, maintainable, and CI-ready** — not demo-only  

---

## 🧱 System Architecture

[ React + Vite UI ]
↓
[ FastAPI Backend ]
↓
[ USGS Earthquake API ]


### QA Automation Flow

Selenium (UI)
├─ Page Object Model (POM)
├─ Explicit waits (loading / empty / error states)
├─ React re-render & stale-element handling
├─ HTML reports + screenshots
└─ CI-ready (headless execution)


---

## 🖥️ Frontend

### Tech Stack
- React  
- TypeScript  
- Vite  
- CSS Modules  

### Features
- Full-page, public-sector-style dashboard  
- Filter controls (time window, min magnitude, limit)  
- Empty state handling (no results)  
- Modal detail view for each earthquake  
- Stable `data-testid` attributes for automation  

---

## ⚙️ Backend

### Tech Stack
- FastAPI  
- Python  
- Axios (frontend client)  

### Responsibilities
- Acts as a validation layer between UI and USGS  
- Normalizes earthquake data  
- Handles query parameters (`window`, `minMag`, `limit`)  
- Enables CORS for browser-based clients  

---

## 🧪 QA Automation (Key Focus)

This project intentionally goes **beyond basic Selenium scripts**.

### Tools
- Selenium WebDriver  
- Pytest  
- Pytest-HTML  
- Chrome (headless & headed modes)  

### Design Patterns & Practices
- Page Object Model (POM)  
- Explicit waits only (no implicit waits)  
- Resilient selectors using `data-testid`  
- Safe handling of:
  - Loading states  
  - Empty result states  
  - React re-renders (stale elements)  
  - Live / non-deterministic data  

---

## ✅ Test Coverage

### Smoke Tests
- Application loads successfully  
- Data table renders  
- Modal opens and closes correctly  

### Regression Tests
- Minimum magnitude filter enforced  
- Supports valid empty results (real-world data behavior)  

---

## 📊 Reporting

- Self-contained HTML test reports  
- Automatic screenshots on failure  
- CI artifact-ready output  

---

## ▶️ Running the Project Locally

### Backend
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8000
Frontend
cd apps/web
npm install
npm run dev
📍 Frontend runs at:
http://localhost:5173

🧪 Running UI Tests
cd quakewatch
python -m pytest -q --html=artifacts/report.html --self-contained-html
Artifacts Generated
artifacts/report.html

artifacts/screenshots/ (on failure)

🚀 CI / Automation
The project is CI-ready and designed to run Selenium in headless mode using GitHub Actions:

Starts backend and frontend services

Executes Selenium UI tests

Uploads HTML reports and logs as artifacts

📁 Workflow location:
.github/workflows/

📌 Why This Project Matters
QuakeWatch demonstrates:

Full-stack understanding (frontend + backend)

Real-world QA automation (not toy examples)

Testing against live, changing data

Thoughtful handling of UI edge cases

Production-minded engineering practices

This is not a tutorial project — it reflects how modern teams build and test real systems.

👤 Author
Mehmet Yazdkhasti
Software Engineer / QA Automation
Focused on building reliable systems with strong testing foundations


---
