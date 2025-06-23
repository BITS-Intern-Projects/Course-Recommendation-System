from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, UTC
from typing import List
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# import torch
from recommendation_engine import set_device, similarity_search



app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for testing
queries = []
bookmarks = []
clicks = []

# Load course data
try:
    courses_df = pd.read_csv("D:/Akshit/VS/AgenticAivenv/archive (2)/Coursera.csv")
    print(f"Loaded {len(courses_df)} courses")
except FileNotFoundError:
    # Create sample data if file not found
    courses_df = pd.DataFrame({
        'Course ID': [1, 2, 3, 4, 5],
        'Course Name': [
            'Introduction to Data Science',
            'Machine Learning Fundamentals',
            'Python Programming',
            'Web Development',
            'Database Management'
        ],
        'Course Description': [
            'Learn the basics of data science and analytics',
            'Master machine learning algorithms and techniques',
            'Learn Python programming from scratch',
            'Build modern web applications',
            'Understand database design and management'
        ],
        'Course URL': [
            'https://example.com/data-science',
            'https://example.com/machine-learning',
            'https://example.com/python',
            'https://example.com/web-dev',
            'https://example.com/database'
        ]
    })
    print("Using sample course data")

# Simple text similarity function
def simple_similarity(query: str, description: str) -> float:
    query_words = set(query.lower().split())
    desc_words = set(description.lower().split())
    intersection = query_words.intersection(desc_words)
    union = query_words.union(desc_words)
    return len(intersection) / len(union) if union else 0


# Pydantic models
class Query(BaseModel):
    query: str

class Course(BaseModel):
    id: str
    name: str
    description: str
    url: str

class ClickEvent(BaseModel):
    courseId: str

@app.get("/")
async def root():
    return {"message": "Course Recommender API is running!"}

@app.post("/submit-query")
async def submit_query(query: Query):
    queries.append({
        "query": query.query,
        "timestamp": datetime.now(UTC).isoformat()
    })
    return {"message": "Query submitted successfully"}

# @app.get("/recommendations", response_model=List[Course])
# async def get_recommendations():
#     if not queries:
#         raise HTTPException(status_code=404, detail="No queries found")
    
#     latest_query = queries[-1]["query"]
    
#     # Calculate similarities
#     similarities = []
#     for _, row in courses_df.iterrows():
#         similarity = simple_similarity(latest_query, str(row["Course Description"]))
#         similarities.append(similarity)
    
#     # Get top 5 recommendations
#     top_indices = np.argsort(similarities)[-5:][::-1]
    
#     recommendations = []
#     for idx in top_indices:
#         course = courses_df.iloc[idx]

        # recommendations.append(Course(
        #     id=str(course["Course ID"]),
        #     name=course["Course Name"],
        #     description=course["Course Description"],
        #     url=course["Course URL"]
        # ))
    
#     return recommendations

@app.get("/recommendations", response_model=List[Course])
async def get_recommendations():
    if not queries:
        raise HTTPException(status_code=404, detail="No queries found")
    
    latest_query = queries[-1]["query"]
    # courses = pd.read_csv("AgenticAivenv/course-recommender/database/Coursera2 (1).csv")
    device = set_device()
    # db_courses = create_model(device)
    # load_data()
    courses = similarity_search(device, latest_query)
    # print(courses)
    recommendations = []
    for i in courses:
        # print(i)
        # print(str(i["ID"])),
        # print(i["Course Name"])
        # print(i["Course Description"],)
        # print(i["Course URL"])
        # i1 = i[0]
        recommendations.append(Course(
            id=str(i["ID"]),
            name=str(i["Course Name"]),
            description=str(i["Course Description"]),
            url=str(i["Course URL"])
        ))
    return recommendations


@app.post("/track-click")
async def track_click(click: ClickEvent):
    clicks.append({
        "course_id": click.courseId,
        "timestamp": datetime.now(UTC).isoformat()
    })
    return {"message": "Click tracked successfully"}

@app.post("/bookmark")
async def bookmark_course(course: Course):
    bookmark = {
        "course_id": course.id,
        "name": course.name,
        "description": course.description,
        "url": course.url,
        "timestamp": datetime.now(UTC).isoformat()
    }
    bookmarks.append(bookmark)
    return {"message": "Course bookmarked successfully"}

@app.get("/bookmarks", response_model=List[Course])
async def get_bookmarks():
    return [
        Course(
            id=bookmark["course_id"],
            name=bookmark["name"],
            description=bookmark["description"],
            url=bookmark["url"]
        )
        for bookmark in bookmarks
    ]

@app.delete("/bookmark/{course_id}")
async def remove_bookmark(course_id: str):
    global bookmarks
    original_length = len(bookmarks)
    bookmarks = [b for b in bookmarks if b["course_id"] != course_id]
    
    if len(bookmarks) == original_length:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    return {"message": "Bookmark removed successfully"}

if __name__ == "__main__":
    import uvicorn
    print("Starting Course Recommender API...")
    print(f"Available courses: {len(courses_df)}")
    uvicorn.run(app, host="0.0.0.0", port=8000) 