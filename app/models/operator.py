from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Operator(Base):
    __tablename__ = "operators"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Operator name

    flares = relationship("Flare", back_populates="operator")