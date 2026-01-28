🌍 QuakeWatch — Global Earthquake Monitoring Dashboard

QuakeWatch is a full-stack web application that provides a real-time view of global earthquake activity using authoritative data from the USGS Earthquake Hazards Program.

Beyond the UI, this project was intentionally built to demonstrate production-grade QA automation, including Selenium UI testing, resilient test design for live data, and CI-ready reporting.

🎯 Project Goals

Present live, worldwide earthquake data in a clear, government-style dashboard

Support filtering by time window, minimum magnitude, and result limits

Demonstrate real-world UI automation against a React application with dynamic data

Build a QA suite that is stable, maintainable, and CI-ready, not demo-only

🧱 System Architecture
[ React + Vite UI ]
          ↓
[ FastAPI Backend ]
          ↓
[ USGS Earthquake API ]


QA Automation:

Selenium (UI)
  ├─ Page Object Model (POM)
  ├─ Explicit waits (loading / empty / error states)
  ├─ React re-render & stale-element handling
  ├─ HTML reports + screenshots
  └─ CI-ready (headless execution)

🖥️ Frontend

Tech

React

TypeScript

Vite

CSS Modules

Features

Full-page, public-sector-style dashboard

Filter controls (time window, min magnitude, limit)

Empty state handling (no results)

Modal detail view for each earthquake

Stable data-testid attributes for automation

⚙️ Backend

Tech

FastAPI

Python

Axios (frontend client)

Responsibilities

Acts as a validation layer between UI and USGS

Normalizes earthquake data

Handles query parameters (window, minMag, limit)

Enables CORS for browser-based clients

🧪 QA Automation (Key Focus)

This project intentionally goes beyond “basic Selenium scripts”.

Tools

Selenium WebDriver

Pytest

Pytest-HTML

Chrome (headless & headed modes)

Design Patterns

Page Object Model (POM)

Explicit waits only (no implicit waits)

Resilient selectors (data-testid)

Safe handling of:

Loading states

Empty result states

React re-renders (stale elements)

Live / non-deterministic data

Test Coverage

Smoke Test

Application loads

Data table renders

Modal opens and closes correctly

Regression Test

Minimum magnitude filter enforced

Supports valid empty results (real-world data behavior)

Reporting

Self-contained HTML test reports

Automatic screenshots on failure

CI artifact-ready output
