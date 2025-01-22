from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Flare(Base):
    __tablename__ = "flares"

    id = Column(Integer, primary_key=True, index=True)
    exception_number = Column(String, nullable=True)
    submittal_date = Column(DateTime, nullable=True)
    filing_number = Column(String, nullable=True)
    status = Column(String, nullable=True)
    filing_type = Column(String, nullable=True)
    operator_number = Column(String, nullable=True)
    operator_name = Column(String, nullable=True)
    property = Column(String, nullable=True)
    effective_date = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
    fv_district = Column(String, nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"))
    volume = Column(Float, nullable=True)  # Ensure this column exists
    duration = Column(Float, nullable=True)  # Ensure this column exists
    h2s = Column(Float, nullable=True)  # Ensure this column exists
    date = Column(DateTime, nullable=True)  # Ensure this column exists

    location = relationship("Location", back_populates="flares")
    operator = relationship("Operator", back_populates="flares")