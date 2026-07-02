# GigHub API

A REST API built with FastAPI for managing freelance gigs.

## Features

- View all gigs
- Filter gigs by category
- Filter gigs by budget
- Search gigs by title or description
- View a single gig by ID
- Create a new gig
- Update a gig
- Delete a gig

## Technologies Used

- Python 3
- FastAPI
- Uvicorn
- Pydantic

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/gighub-api.git
```

Navigate into the project:

```bash
cd gighub-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Windows

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m uvicorn main:app --reload
```

Open your browser:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

- GET `/gigs`
- GET `/gigs/search`
- GET `/gigs/{gig_id}`
- POST `/gigs`
- PUT `/gigs/{gig_id}`
- DELETE `/gigs/{gig_id}`

## Author

Peter Mutethia