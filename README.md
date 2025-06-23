# Course Recommendation Engine

A full-stack web application that provides personalized course recommendations based on user queries. Built with React, FastAPI, and MongoDB.

## Features

- Search for courses using natural language queries
- Get personalized course recommendations
- Bookmark favorite courses
- Track course interactions
- Modern, responsive UI with Tailwind CSS

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- MongoDB (v4.4 or higher)
- Coursera dataset in `archive (2)/Coursera.csv`

## Setup

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:
   ```bash
   python main.py
   ```

The backend API will be available at http://localhost:8000

### MongoDB Setup

1. Install MongoDB if you haven't already
2. Start the MongoDB service
3. The application will automatically create the necessary collections

## Project Structure

```
course-recommender/
├── frontend/           # React frontend
│   ├── src/
│   │   ├── pages/     # Page components
│   │   └── App.tsx    # Main application component
│   └── package.json   # Frontend dependencies
├── backend/           # FastAPI backend
│   ├── main.py       # Main application file
│   └── requirements.txt # Backend dependencies
└── README.md         # This file
```

## API Endpoints

- POST `/submit-query` - Submit a search query
- GET `/recommendations` - Get course recommendations
- POST `/track-click` - Track course URL clicks
- POST `/bookmark` - Bookmark a course
- GET `/bookmarks` - Get all bookmarked courses
- DELETE `/bookmark/{course_id}` - Remove a bookmark

## Technologies Used

- Frontend:
  - React
  - TypeScript
  - Tailwind CSS
  - Axios

- Backend:
  - FastAPI
  - MongoDB
  - Pandas
  - Transformers (Hugging Face)
  - scikit-learn

## License

MIT 