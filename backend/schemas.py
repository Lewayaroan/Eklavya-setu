"""
Pydantic schemas for request and response serialization.
"""

from typing import Optional, List
from pydantic import BaseModel


class StudentBase(BaseModel):
    apaar_id: str
    full_name: str
    gender: str
    community: str
    is_pvtg: bool
    state: str
    district: str
    current_institute: str
    annual_family_income: float
    bank_name: str
    account_last_four: str
    aadhaar_seeded: bool


class StudentOut(StudentBase):
    id: int
    aishe_code: Optional[str] = None

    class Config:
        from_attributes = True


class SchemeOut(BaseModel):
    scheme_id: str
    name: str
    category: str
    annual_benefit: str
    income_ceiling: float
    former_portal: str
    description: str

    class Config:
        from_attributes = True


class ApplicationOut(BaseModel):
    application_id: str
    student_apaar: str
    scheme_id: str
    stage: int
    stage_name: str
    sanctioned_amount: float
    digilocker_verified: bool
    institute_verified: bool
    state_sanctioned: bool
    pfms_disbursed: bool
    soft_mismatch_resolved: bool
    soft_mismatch_detail: Optional[str] = None
    pfms_tracking_id: Optional[str] = None

    class Config:
        from_attributes = True


class SingleAvailCheckRequest(BaseModel):
    apaar_id: str
    desired_scheme_id: str


class SingleAvailCheckResponse(BaseModel):
    is_compliant: bool
    status_title: str
    message: str
    requires_transition: bool
    active_scheme: Optional[str] = None


class JagoQueryRequest(BaseModel):
    apaar_id: str
    query_text: str
    language: str = "hi"  # hi, en, sat, te


class JagoQueryResponse(BaseModel):
    language: str
    spoken_response: str
    action_type: str
    action_description: str
    confidence: float
    source: str


class DistrictOutreachOut(BaseModel):
    id: int
    district: str
    state: str
    udise_enrolled_st: int
    active_beneficiaries: int
    unreached_gap: int
    pvtg_concentration: str
    status_flag: str

    class Config:
        from_attributes = True


class CampDispatchRequest(BaseModel):
    district_id: int
    officer_contact: Optional[str] = None
