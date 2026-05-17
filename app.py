from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()

## Utility function to load the data from the json file and return it as a dictionary.
def load_data():
    """
    The `load_data` function reads and returns data from a JSON file named "patients.json".
    :return: The function `load_data()` is returning the data loaded from the "patients.json" file.
    """
    with open("patients.json", "r") as f:
        data = json.load(f)
    
    return data

@app.get("/")
def hello():
    """
    The function returns a message indicating that the Patient Management System API is running.
    :return: The function `hello()` is returning a dictionary with the key "message" and the value
    "Patient Management System API is running!".
    """
    return {"message":"Patient Management System API is running!"}

@app.get("/view")
#def view_patients():
#    """
#    The function `view_patients` loads and returns patient data.
#    :return: The function `view_patients()` is returning the data loaded from the `load_data()`
#    function.
#    """
#    data = load_data()
#    return data

## Added the Query parameters to the sort the patients data retrieved.
def view_patients(sort_by: str = Query(default = 'bmi', description="The field to sort the patients by height,weight or bmi.", example="bmi"),
                  order: str = Query(default = 'asc', description="The order to sort the patients in asc or dsc order.", example="asc")):
    """
    This Python function retrieves and sorts patient data based on specified criteria such as height,
    weight, or BMI.
    
    :param sort_by: The `sort_by` parameter in the `view_patients` function is used to specify the field
    by which the patients should be sorted. The valid options for sorting are 'height', 'weight', or
    'bmi'. The default value is 'bmi', but it can be changed by providing
    :type sort_by: str
    :param order: The `order` parameter in the `view_patients` function is used to specify the order in
    which the patients should be sorted. It can have two possible values:
    :type order: str
    :return: The function `view_patients` is returning a sorted list of patient data based on the
    specified field (`sort_by`) and order (`order`). The data is sorted in either ascending or
    descending order based on the specified parameters.
    """
    
    valid_fields = ['height', 'weight', 'bmi'] ## fields to sort the data
    ## validate the query parameters
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {valid_fields}")#400 Bad Request
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'")#400 Bad Request
    
    data = load_data() ## load the data
    
    sort_order = True if order == 'desc' else False ## determine the sort order based on the query parameter
    sorted_data = sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order) ## sort the data based on the specified field and order
    
    return sorted_data
    

## Added the path parameter to retrieve the specific patient data based on the patient id provided in the path.
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve ",example="P001")): ## e.g "P001"
    """
    The function `view_patient` retrieves patient data based on the provided ID and returns a 404 error
    if the patient is not found.
    
    :param patient_id: The `patient_id` parameter is a string that represents the ID of the patient to
    retrieve. It is a required parameter and is expected to be provided in the path when making a
    request. The example value provided is "P001"
    :type patient_id: str
    :return: If the patient with the specified `patient_id` is found in the data, the function will
    return the data associated with that patient. If the patient is not found, an HTTPException with a
    status code of 404 and a detail message of "Patient not found" will be raised.
    """
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    #return {"message": "Patient not found"}  ## normal json response if not found
    raise HTTPException(status_code=404, detail="Patient not found") ## improved the response by adding status codes and details.