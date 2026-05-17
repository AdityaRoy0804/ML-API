from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    
    return data

@app.get("/")
def hello():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"message":"Patient Management System API is running!"}

@app.get("/view")
#def view_patients():
#    data = load_data()
#    return data
def view_patients(sort_by: str = Query(default = 'bmi', description="The field to sort the patients by height,weight or bmi.", example="bmi"),
                  order: str = Query(default = 'asc', description="The order to sort the patients in asc or dsc order.", example="asc")):
    
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_fields}")#400 Bad Request
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'")#400 Bad Request
    
    data = load_data()
    
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order)
    
    return sorted_data
    

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve ",example="P001")): ## e.g "P001"
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    #return {"message": "Patient not found"} 
    raise HTTPException(status_code=404, detail="Patient not found")