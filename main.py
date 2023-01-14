from fastapi import Body, FastAPI, HTTPException
app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello"}
properties = []
@app.post("/create_new_property/")
async def create_new_property(payload: dict = Body(...)):
    property = {
        'property_id': len(properties) + 1,
        'name': payload['property_name'],
        'address': payload['address'],
        'city': payload['city'],
        'state': payload['state']
    }
    properties.append(property)
    return {"properties": properties}
@app.get("/fetch_property_details/{city}")
async def fetch_property_details(city: str):
    result = [property for property in properties if property['city'] == city]
    if not result:
        raise HTTPException(status_code=404, detail="City not found")
    return {"properties": result}
@app.put("/update_property_details/{property_id}")
async def update_property_details(payload: dict = Body(...)):
    for i in range(len(properties)):
        if properties[i]['property_id'] == payload['property_id']:
            properties[i]['name'] = payload['property_name']
            properties[i]['address'] = payload['address']
            properties[i]['city'] = payload['city']
            properties[i]['state'] = payload['state']
            break
    else:
        raise HTTPException(status_code=404, detail="property_id not found")
    return {"properties": properties}
@app.get("/find_cities_by_state/{state}")
async def find_cities_by_state(state: str):
    result = [property["city"] for property in properties if property['state'] == state]
    result = list(sorted(list(set(result))))
    if not result:
        raise HTTPException(status_code=404, detail="State not found")
    return {"properties": result}
# The below function does not give the the property having the given property_id as an output.
# It looks for other properties in the cities, and if there is no other property present in the city
# other than the property having the property_id mentioned in the function, then it raises an error
# saying that no similar properties can be found. If the user mentions an incorrect property, 
# it raises an error saying that no property having the corresponding property_ID can be found.
# If you want the output to show the property having the given property_id also, comment out the
# len(result) == 0 statement.

@app.get("/find_similar_properties/{property_id}")
async def find_similar_properties(property_id: int):
    req_city = ""
    for property in properties:
        if property['property_id'] == property_id:
            req_city = property['city']
            break
    if req_city == "":
         raise HTTPException(status_code=404, detail="Property_ID not found")
    else:
        result = [property for property in properties if property['city'] == req_city and property['property_id']!=property_id] 
        if len(result) == 0:
            raise HTTPException(status_code=404, detail= "No similar property found in the city")
        return {"properties":result}
