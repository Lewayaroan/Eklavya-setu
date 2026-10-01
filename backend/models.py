"""
SQLAlchemy ORM models for Eklavya Setu.
"""

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from backend.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    apaar_id = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=False)
    community = Column(String(100), nullable=False)
    is_pvtg = Column(Boolean, default=False)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    current_institute = Column(String(200), nullable=False)
    aishe_code = Column(String(50), nullable=True)
    annual_family_income = Column(Float, nullable=False)
    bank_name = Column(String(100), nullable=False)
    account_last_four = Column(String(10), nullable=False)
    aadhaar_seeded = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ScholarshipScheme(Base):
    __tablename__ = "scholarship_schemes"

    id = Column(Integer, primary_key=True, index=True)
    scheme_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    annual_benefit = Column(String(100), nullable=False)
    income_ceiling = Column(Float, default=0.0)
    former_portal = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String(50), unique=True, index=True, nullable=False)
    student_apaar = Column(String(50), ForeignKey("students.apaar_id"), nullable=False)
    scheme_id = Column(String(50), ForeignKey("scholarship_schemes.scheme_id"), nullable=False)
    stage = Column(Integer, default=1)  # 1: DigiLocker, 2: Institute, 3: State/MoTA, 4: PFMS DBT
    stage_name = Column(String(100), default="Application Submitted")
    sanctioned_amount = Column(Float, default=0.0)
    digilocker_verified = Column(Boolean, default=False)
    institute_verified = Column(Boolean, default=False)
    state_sanctioned = Column(Boolean, default=False)
    pfms_disbursed = Column(Boolean, default=False)
    soft_mismatch_resolved = Column(Boolean, default=True)
    soft_mismatch_detail = Column(Text, nullable=True)
    pfms_tracking_id = Column(String(100), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DistrictOutreach(Base):
    __tablename__ = "district_outreach"

    id = Column(Integer, primary_key=True, index=True)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    udise_enrolled_st = Column(Integer, nullable=False)
    active_beneficiaries = Column(Integer, nullable=False)
    unreached_gap = Column(Integer, nullable=False)
    pvtg_concentration = Column(String(50), default="Moderate")
    status_flag = Column(String(50), default="Action Required")
