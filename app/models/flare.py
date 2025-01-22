from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Flare(Base):
    __tablename__ = "flares"

    id = Column(Integer, primary_key=True, index=True)
    exception_number = Column(String, nullable=True)  # Add this column
    submittal_date = Column(DateTime, nullable=True)  # Add this column
    filing_number = Column(String, nullable=True)  # Add this column
    status = Column(String, nullable=True)  # Add this column
    filing_type = Column(String, nullable=True)  # Add this column
    operator_number = Column(String, nullable=True)  # Add this column
    operator_name = Column(String, nullable=True)  # Add this column
    property = Column(String, nullable=True)  # Add this column
    effective_date = Column(DateTime, nullable=True)  # Add this column
    expiration_date = Column(DateTime, nullable=True)  # Add this column
    fv_district = Column(String, nullable=True)  # Add this column
    location_id = Column(Integer, ForeignKey("locations.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"))

    location = relationship("Location", back_populates="flares")
    operator = relationship("Operator", back_populates="flares")