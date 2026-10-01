"""
Scholarship schemes, applications, and Single-Avail Guard router.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import Student, ScholarshipScheme, Application
from backend.schemas import (
    SchemeOut,
    StudentOut,
    ApplicationOut,
    SingleAvailCheckRequest,
    SingleAvailCheckResponse,
)

router = APIRouter(prefix="/api/scholarships", tags=["Scholarships"])


@router.get("/schemes", response_model=List[SchemeOut])
def get_all_schemes(db: Session = Depends(get_db)):
    """Fetch all 5 MoTA Central Scholarship schemes."""
    return db.query(ScholarshipScheme).all()


@router.get("/student/{apaar_id}")
def get_student_dashboard(apaar_id: str, db: Session = Depends(get_db)):
    """Fetch consolidated student dashboard data via APAAR ID."""
    student = db.query(Student).filter(Student.apaar_id == apaar_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student APAAR record not found")

    application = db.query(Application).filter(Application.student_apaar == apaar_id).first()
    active_scheme = None
    if application:
        active_scheme = db.query(ScholarshipScheme).filter(ScholarshipScheme.scheme_id == application.scheme_id).first()

    return {
        "student": StudentOut.from_orm(student),
        "application": ApplicationOut.from_orm(application) if application else None,
        "active_scheme": SchemeOut.from_orm(active_scheme) if active_scheme else None,
    }


@router.post("/check-single-avail", response_model=SingleAvailCheckResponse)
def check_single_avail(payload: SingleAvailCheckRequest, db: Session = Depends(get_db)):
    """
    Cross-Portal Single-Avail & De-Duplication Guard.
    Prevents duplicate claims across NSP, Canara Bank SFMP, and NOS.
    """
    student = db.query(Student).filter(Student.apaar_id == payload.apaar_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student record not found")

    current_app = db.query(Application).filter(Application.student_apaar == payload.apaar_id).first()

    # Scenario 1: No active application -> 100% compliant
    if not current_app:
        return SingleAvailCheckResponse(
            is_compliant=True,
            status_title="No Overlapping Claims",
            message="No existing scholarship active on NSP, SFMP, or NOS. Eligible to proceed.",
            requires_transition=False,
            active_scheme=None,
        )

    # Scenario 2: Applying for same active scheme -> Already enrolled
    if current_app.scheme_id == payload.desired_scheme_id:
        return SingleAvailCheckResponse(
            is_compliant=True,
            status_title="Active Beneficiary",
            message="You are already actively enrolled and tracked under this scheme for the current session.",
            requires_transition=False,
            active_scheme=current_app.scheme_id,
        )

    # Scenario 3: Higher Ed or Top Class Upgrade (e.g. Post-Matric -> Top Class)
    if current_app.scheme_id == "SCH-POST-MATRIC" and payload.desired_scheme_id == "SCH-TOP-CLASS":
        return SingleAvailCheckResponse(
            is_compliant=False,
            status_title="Upgrade Transition Required",
            message=(
                "You currently hold an active Post-Matric ST grant. Central MoTA policy prohibits concurrent "
                "benefits. Submitting this application will trigger an automated upgrade transition: your Post-Matric "
                "grant will auto-close upon sanction of Top Class without penalization."
            ),
            requires_transition=True,
            active_scheme=current_app.scheme_id,
        )

    # Scenario 4: Fellowship Transition
    if payload.desired_scheme_id == "SCH-NFST":
        return SingleAvailCheckResponse(
            is_compliant=True,
            status_title="Doctoral Transition Eligible",
            message=(
                "Post-Matric tenure completed. Transitioning to National Fellowship (NFST via Canara Bank) "
                "is compliant subject to valid UGC-NET JRF score verification."
            ),
            requires_transition=True,
            active_scheme=current_app.scheme_id,
        )

    return SingleAvailCheckResponse(
        is_compliant=True,
        status_title="Safe Progression",
        message="No dual-claim conflicts detected across central registries.",
        requires_transition=False,
        active_scheme=current_app.scheme_id,
    )


@router.post("/digilocker-sync/{apaar_id}")
def sync_digilocker(apaar_id: str, db: Session = Depends(get_db)):
    """Simulate cryptographic verification of documents via DigiLocker PKI."""
    student = db.query(Student).filter(Student.apaar_id == apaar_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "status": "success",
        "verified_documents": [
            {
                "doc_type": "Scheduled Tribe (ST) Certificate",
                "issuer": "Department of Revenue, Govt. of Jharkhand",
                "cert_no": "JH/ST/2022/89412",
                "verified": True,
                "encryption": "SHA-256 PKI Signed",
            },
            {
                "doc_type": "Annual Family Income Certificate",
                "issuer": "Circle Officer, SDO Ranchi",
                "annual_income": student.annual_family_income,
                "verified": True,
                "encryption": "SHA-256 PKI Signed",
            },
            {
                "doc_type": "APAAR Academic Registry",
                "apaar_id": student.apaar_id,
                "institute": student.current_institute,
                "verified": True,
                "encryption": "DigiLocker Certified",
            },
        ],
    }


@router.post("/resolve-soft-exception/{application_id}")
def resolve_soft_exception(application_id: str, db: Session = Depends(get_db)):
    """Nodal officer 1-click approval for minor name/spelling mismatches."""
    app = db.query(Application).filter(Application.application_id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.soft_mismatch_resolved = True
    app.soft_mismatch_detail = "Verified manually by college principal via Aadhaar biometric override."
    db.commit()

    return {
        "status": "success",
        "application_id": app.application_id,
        "message": "Soft exception resolved. Application unblocked and promoted to next review stage.",
    }
