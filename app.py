from fastapi import FastAPI, Path, HTTPException
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

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve ",example="P001")): ## e.g "P001"
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    #return {"message": "Patient not found"}
    raise HTTPException(status_code=404, detail="Patient not found")