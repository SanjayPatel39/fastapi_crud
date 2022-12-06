from pydantic import BaseModel

# Create Employee Schema (Pydantic Model)


class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: int


# Complete Employee Schema (Pydantic Model)


class Employee(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: int

    class Config:
        orm_mode = True
