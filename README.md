# Job Portal Login System

A FastAPI application with Jinja2 templates for user authentication and job role/skills selection.

## Features

- Login page with userid, password, and phone number fields
- Sign in and Sign up buttons
- Job roles page with skills dropdown
- Dependency injection using protocols
- Minimal JavaScript for interactivity
- Clear button to reset selections

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Open your browser and go to `http://localhost:8000`

## Usage

1. Enter credentials on the login page
2. Click "Login" to proceed to job roles page
3. Select a job role to see available skills
4. Click on skills to add them to your selection
5. Use the "Clear" button to reset all selections

## Project Structure

- `main.py` - FastAPI application with dependency injection
- `templates/` - Jinja2 HTML templates
- `static/` - CSS and JavaScript files
- `requirements.txt` - Python dependencies