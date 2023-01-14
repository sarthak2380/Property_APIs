from fastapi import Body, FastAPI, HTTPException
app = FastAPI()
import mysql.connector
connection = mysql.connector.connect(host='localhost',database='properties',user='root',password='')
cursor = connection.cursor()
@app.get("/")
def root():
    return {"message":"Hello"}
properties = []
@app.post("/create_new_property/")
async def create_new_property(payload: dict = Body(...)):
    property = {
        'name': payload['property_name'],
        'address': payload['address'],
        'city': payload['city'],
        'state': payload['state']
    }
    try:
        connection = mysql.connector.connect(host='localhost',database='properties',user='root',password='')
        cursor = connection.cursor()
        query = "CREATE TABLE IF NOT EXISTS PROPERTY(property_id int primary key, property_name varchar(50), address varchar(70), city varchar(30), state varchar(30));"
        cursor.execute(query)
        connection.commit()
    except:
        raise HTTPException(status_code=404,detail="Nooo")
    if True:
        query = "SELECT * FROM PROPERTY"
        cursor.execute(query)
        ll = list(cursor.fetchall())
        a = len(ll)
        b = payload['property_name']
        c = payload['address']
        d = payload['city']
        e = payload['state']
        query = "INSERT INTO PROPERTY (property_id,property_name,address,city,state) VALUES ("+str(f"{a},'{b}','{c}','{d}','{e}')")
        print(query)
        cursor.execute(query)
        properties.append(property)
        connection.commit()
        #raise HTTPException(status_code=404)
    return {"properties": properties}
@app.get("/fetch_property_details/{city}")
async def fetch_property_details(city: str):
    query = "SELECT * FROM PROPERTY WHERE city = " + f"'{city}'"
    cursor.execute(query)
    result = list(cursor.fetchall())
    if not result:
        raise HTTPException(status_code=404, detail="City not found")
    return {"properties": result}
@app.put("/update_property_details/{property_id}")
async def update_property_details(payload: dict = Body(...)):
    a = payload['property_id']
    b = payload['property_name']
    c = payload['address']
    d = payload['city']
    e = payload['state']
    query = f"UPDATE PROPERTY SET property_name = '{b}', address = '{c}', city = '{d}', state = '{e}' WHERE property_id = {a}"
    cursor.execute(query)
    query = "SELECT * FROM PROPERTY"
    cursor.execute(query)
    properties = list(cursor.fetchall())
    return {"properties": properties}
@app.get("/find_cities_by_state/{state}")
async def find_cities_by_state(state: str):
    query = "SELECT city FROM PROPERTY WHERE state = " + f"'{state}'"
    cursor.execute(query)
    result = list(cursor.fetchall())
    print(result)
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
# len(result) == 1 statement.

@app.get("/find_similar_properties/{property_id}")
async def find_similar_properties(property_id: int):
    req_city = ""
    query = "SELECT city FROM PROPERTY WHERE property_id = " + f"{property_id}"
    cursor.execute(query)
    ll = list(cursor.fetchall())
    print(ll)
    req_city = ll[0]
    if len(req_city) == 0:
         raise HTTPException(status_code=404, detail="Property_ID not found")
    else:
        query = "SELECT * FROM PROPERTY WHERE city = " + f"'{req_city[0]}'"
        print(req_city[0])
        cursor.execute(query)
        result = list(cursor.fetchall())
        if len(result) == 1:
            raise HTTPException(status_code=404, detail= "No similar property found in the city")
        return {"properties":result}
