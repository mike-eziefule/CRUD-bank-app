import csv
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    id: int
    name: str
    age: int
    
# CRUD Operations
# Create - POST
@app.post("/person/")
async def create_person(person: Person):
    with open("new.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([person.id, person.name, person.age])
    return {"message": "Person created successfully", "data": person}

# Read - GET
@app.get("/person/{id}")
async def get_person(id: int):
    with open("new.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if int(row[0]) == id:
                return Person(id=int(row[0]), name=row[1], age=int(row[2]))
    return {"message": "Person not found"}
