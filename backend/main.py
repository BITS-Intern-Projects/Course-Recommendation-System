from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
db = client.course_recommender

# Load course data
courses_df = pd.read_csv("../archive (2)/Coursera.csv")

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

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

# Helper function to get embeddings
def get_embedding(text: str) -> np.ndarray:
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

# Precompute course embeddings
course_embeddings = []
for _, row in courses_df.iterrows():
    desc = str(row["Course Description"])
    embedding = get_embedding(desc)
    course_embeddings.append(embedding[0])
course_embeddings = np.array(course_embeddings)

@app.post("/submit-query")
async def submit_query(query: Query):
    query_doc = {
        "query": query.query,
        "timestamp": datetime.utcnow()
    }
    await db.queries.insert_one(query_doc)
    return {"message": "Query submitted successfully"}

@app.get("/recommendations", response_model=List[Course])
async def get_recommendations():
    # Get the latest query
    latest_query = await db.queries.find_one(sort=[("timestamp", -1)])
    if not latest_query:
        raise HTTPException(status_code=404, detail="No queries found")
    
    # Get embedding for the query
    query_embedding = get_embedding(latest_query["query"])
    
    # Calculate similarities
    similarities = cosine_similarity(query_embedding, course_embeddings)[0]
    
    # Get top 5 recommendations
    top_indices = np.argsort(similarities)[-5:][::-1]
    
    recommendations = []
    for idx in top_indices:
        course = courses_df.iloc[idx]
        recommendations.append(Course(
            id=str(course["Course ID"]),
            name=course["Course Name"],
            description=course["Course Description"],
            url=course["Course URL"]
        ))
    
    return recommendations

@app.post("/track-click")
async def track_click(click: ClickEvent):
    click_doc = {
        "course_id": click.courseId,
        "timestamp": datetime.utcnow()
    }
    await db.clicks.insert_one(click_doc)
    return {"message": "Click tracked successfully"}

@app.post("/bookmark")
async def bookmark_course(course: Course):
    bookmark_doc = {
        "course_id": course.id,
        "name": course.name,
        "description": course.description,
        "url": course.url,
        "timestamp": datetime.utcnow()
    }
    await db.bookmarks.insert_one(bookmark_doc)
    return {"message": "Course bookmarked successfully"}

@app.get("/bookmarks", response_model=List[Course])
async def get_bookmarks():
    cursor = db.bookmarks.find()
    bookmarks = []
    async for doc in cursor:
        bookmarks.append(Course(
            id=doc["course_id"],
            name=doc["name"],
            description=doc["description"],
            url=doc["url"]
        ))
    return bookmarks

@app.delete("/bookmark/{course_id}")
async def remove_bookmark(course_id: str):
    result = await db.bookmarks.delete_one({"course_id": course_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"message": "Bookmark removed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 