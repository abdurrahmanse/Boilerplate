from sqlalchemy import Column, Integer, String
from app.database import Base

class Page(Base):
    __tablename__ = "page"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
