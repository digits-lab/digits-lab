# MiniDoc - Smart Digital Health Assistant

MiniDoc is a responsive, user-friendly healthcare web application that connects patients, doctors, and hospitals.

## Features

- **Doctor & Surgeon Directory:** Search for doctors by specialty, illness, and hospital.
- **Appointment Booking System:** Book appointments with doctors, with an option for urgent cases.
- **AI Medical Assistant:** Get a preliminary diagnosis based on your symptoms (powered by OpenAI).
- **Hospital Capacity Tracker:** View real-time hospital bed availability and cost indexes.
- **Patient Portal:** View your appointments and prescriptions.

## Tech Stack

- **Frontend:** HTML, CSS (Tailwind), JavaScript
- **Backend:** Python (Flask), SQLite
- **AI:** OpenAI API

## Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd minidoc-project
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   - The database is created automatically. To seed it with sample data, run:
   ```bash
   python minidoc/seed.py
   ```

4. **Set your OpenAI API Key:**
   - Open `minidoc/routes.py` and replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI API key.

### Running the Application

1. **Start the Flask server:**
   ```bash
   python minidoc/app.py
   ```

2. **Open your browser:**
   - Navigate to `http://127.0.0.1:5000`

## Project Structure

```
minidoc/
├── database/
│   └── minidoc.db      # SQLite database
├── frontend/
│   ├── static/
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   └── patient_portal.js
│   └── templates/
│       ├── index.html
│       └── patient_portal.html
├── __init__.py
├── app.py              # Main Flask application
├── create_db.py        # Script to create the database
├── models.py           # Database models
├── routes.py           # API routes
└── seed.py             # Script to seed the database
```