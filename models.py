from sqlalchemy import Column, Integer, String, UniqueConstraint
from database import Base

# Define Employee class inheriting from Base


class Employee(Base):
    __tablename__ = 'Employee'
    __table_args__ = (UniqueConstraint('First Name', 'Last Name', 'Email', name='unique_employee'),)
    id = Column(Integer, primary_key=True)
    first_name = Column('First Name', String(45))
    last_name = Column('Last Name', String(45))
    email = Column('Email', String(100))
    phone = Column('Phone', Integer)
