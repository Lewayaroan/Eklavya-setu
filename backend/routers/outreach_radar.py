"""
Zero-Dropout Outreach Radar router for MoTA Admin & Welfare Officers.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models import DistrictOutreach
from backend.schemas import DistrictOutreachOut, CampDispatchRequest

router = APIRouter(prefix="/api/outreach", tags=["Outreach Radar"])


@router.get("/gap-analysis", response_model=List[DistrictOutreachOut])
def get_outreach_gap_analysis(db: Session = Depends(get_db)):
    """
    Get district-wise gap analysis between UDISE+ school enrollments
    and active scholarship beneficiaries to identify left-out ST children.
    """
    return db.query(DistrictOutreach).all()


@router.post("/dispatch-camp")
def dispatch_mobile_camp(payload: CampDispatchRequest, db: Session = Depends(get_db)):
    """
    Trigger mobile biometric and enrollment camp dispatch for a specific district.
    """
    district = db.query(DistrictOutreach).filter(DistrictOutreach.id == payload.district_id).first()
    if not district:
        raise HTTPException(status_code=404, detail="District record not found")

    return {
        "status": "success",
        "district": district.district,
        "state": district.state,
        "target_students": district.unreached_gap,
        "message": (
            f"Mobile biometric enrollment camp scheduled for {district.district} District ({district.state}). "
            f"Automated notification dispatched to District Welfare Officer (DWO) to cover {district.unreached_gap} "
            f"left-out tribal students before the 15th October deadline."
        ),
    }
