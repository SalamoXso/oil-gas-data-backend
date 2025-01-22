from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Location name
    coordinates = Column(String)  # Latitude and longitude

    flares = relationship("Flare", back_populates="location")