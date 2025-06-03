from sqlalchemy import Column, Integer, String, Float
from database import Base

class Crack(Base):
    __tablename__ = "cracks"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    length = Column(Float)
    depth = Column(Float)
    status = Column(String)
