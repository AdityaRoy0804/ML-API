from fastapi import FastAPI
import json


app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    
    return data


@app.get("/")
def hello():
    return {"message":"Patient Management System API is running!"}

@app.get("/view")
def view_patients():
    data = load_data()
    return data