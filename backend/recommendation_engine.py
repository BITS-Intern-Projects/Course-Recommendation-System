from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import pandas as pd


#SET DEVICE
import torch
def set_device():
    print("GPU available:", torch.cuda.is_available())
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return device

#Generating complex User Query from user profile
USER_JOB = "Marketting head"
USER_SKILLS = "Marketing, Management"
SKILLS_TO_LEARN = "AI, Automation, AI in Marketing"
GOAL = "To use AI to help in marketting"
prompt = f'''My job is {USER_JOB}. I am currently skilled at {USER_SKILLS}. I wish to learn {SKILLS_TO_LEARN} to fullfil
    my goal of {GOAL}. Kindly recommend me courses for the same.'''

#Create model using HuggingFace
def similarity_search(device, query = prompt):
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    #FOR LOADING DATA

    db_courses = Chroma(
        embedding_function=hf,
        persist_directory="AgenticAivenv/course-recommender/backend/db_courses_chroma"
    )
    print(db_courses)
    print(db_courses._collection.count())
    
    #SIMILARITY SEARCH
    docs  = db_courses.similarity_search(query=query, k = 5)

    courses = pd.read_csv("AgenticAivenv/course-recommender/database/Coursera2 (1).csv")
    #Printing name, ID of courses
    recommended = []
    for i in range(5):
    # print(courses[courses["ID"] == int(docs[i].page_content.strip("\"").split()[0].strip())])
        temp = courses[courses["ID"] == int(docs[i].page_content.strip("\"").split()[0].strip())].to_dict(orient='records')
        recommended.append(temp[0])
        # print(temp)
        #recommended.append(courses[courses["ID"] == int(docs[i].page_content.strip("\"").split()[0].strip())])["Course Name"]
        # print(courses[courses["ID"] == int(docs[i].page_content.strip("\"").split()[0].strip())])
    # print(recommended)
    return recommended

if __name__ == "__main__":
    print("hi")