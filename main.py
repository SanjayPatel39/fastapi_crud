from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "Employee"


@app.post("/employee", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, session: Session = Depends(get_session)):
    # create an instance of the Employee database model
    employee_db = models.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        phone=employee.phone
    )

    try:
        # add it to the session and commit it
        session.add(employee_db)
        session.commit()
        session.refresh(employee_db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=422, detail="employee already exists") from e
    else:
        # return the employee_db object
        return employee_db


@app.get("/employee/{id}", response_model=schemas.Employee)
def get_employee(id: int, session: Session = Depends(get_session)):

    # get the employee with the given id
    employee = session.query(models.Employee).get(id)

    # check if employee with given id exists. If not, raise exception and return 404 not found response
    if not employee:
        raise HTTPException(status_code=404, detail=f"employee with id {id} not found")

    return employee


@app.put("/employee/{id}", response_model=schemas.Employee)
def update_employee(id: int, first_name: str, last_name: str, email: str, phone: int, session: Session = Depends(get_session)):

    # get the employee with the given id
    employee = session.query(models.Employee).get(id)

    # update employee with the given task (if an item with the given id was found)
    if employee:
        employee.first_name = first_name
        employee.last_name = last_name
        employee.email = email
        employee.phone = phone

        session.commit()

    # check if employee with given id exists. If not, raise exception and return 404 not found response
    if not employee:
        raise HTTPException(status_code=404, detail=f"employee with id {id} not found")

    return employee


@app.delete("/employee/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, session: Session = Depends(get_session)):

    # get the employee with the given id
    employee = session.query(models.Employee).get(id)

    # if employee with given id exists, delete it from the database. Otherwise raise 404 error
    if not employee:
        raise HTTPException(status_code=404, detail=f"employee with id {id} not found")

    session.delete(employee)
    session.commit()
    return None


@app.get("/employee", response_model=List[schemas.Employee])
def employee_list(session: Session = Depends(get_session)):

    # get all employees
    return session.query(models.Employee).all()
