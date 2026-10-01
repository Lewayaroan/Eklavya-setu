"""
Database connection and initial data seeder for Eklavya Setu.
Ministry of Tribal Affairs (MoTA) • SIH26238
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "eklavya_setu.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_initial_data(db):
    """Seed initial MoTA schemes, sample tribal students, and district gap records."""
    from backend.models import Student, ScholarshipScheme, Application, DistrictOutreach

    if db.query(ScholarshipScheme).first() is not None:
        return  # Already seeded

    # 1. Seed The 5 Central MoTA Schemes
    schemes = [
        ScholarshipScheme(
            scheme_id="SCH-PRE-MATRIC",
            name="Pre-Matric Scholarship for ST Students",
            category="School Education (Class 9 & 10)",
            annual_benefit="₹ 3,500 / Year (Day Scholar) / ₹ 7,000 / Year (Hosteller)",
            income_ceiling=250000,
            former_portal="National Scholarship Portal (NSP)",
            description="Financial support to poor ST students studying in classes 9 and 10 to minimize dropouts.",
        ),
        ScholarshipScheme(
            scheme_id="SCH-POST-MATRIC",
            name="Post-Matric Scholarship for ST Students",
            category="Higher Secondary & Graduation (Class 11 to PG)",
            annual_benefit="100% Tuition Fees + Up to ₹ 1,200 / Month Maintenance",
            income_ceiling=250000,
            former_portal="NSP / State Scholarship Portals",
            description="Comprehensive scholarship covering compulsory non-refundable fees and monthly living allowances.",
        ),
        ScholarshipScheme(
            scheme_id="SCH-TOP-CLASS",
            name="National Fellowship and Scholarship for Higher Education (Top Class ST)",
            category="Premier Institutes (IIT, IIM, NIT, AIIMS, NLUs)",
            annual_benefit="Full Tuition Fees + ₹ 86,000 Living / Book / Laptop Allowance",
            income_ceiling=600000,
            former_portal="National Scholarship Portal (NSP)",
            description="Direct funding for meritorious ST students admitted into notified world-class institutions.",
        ),
        ScholarshipScheme(
            scheme_id="SCH-NFST",
            name="National Fellowship for Higher Education of ST Students (NFST)",
            category="Doctoral Studies (M.Phil & Ph.D.)",
            annual_benefit="₹ 37,000 / Month (JRF) / ₹ 42,000 / Month (SRF) + HRA",
            income_ceiling=0,  # Merit/NET based
            former_portal="Scholarship Fellowship Management Portal / SFMP (Canara Bank)",
            description="Monthly fellowship for ST candidates pursuing regular full-time research in Indian universities.",
        ),
        ScholarshipScheme(
            scheme_id="SCH-NOS",
            name="National Overseas Scholarship (NOS) for ST Candidates",
            category="International Masters & Ph.D. (Top 500 Global Unis)",
            annual_benefit="100% Foreign Tuition + USD 15,400 / GBP 9,900 Annual Stipend",
            income_ceiling=800000,
            former_portal="Standalone NOS Portal",
            description="Prestigious overseas scholarship for ST students admitted into accredited global universities.",
        ),
    ]
    db.add_all(schemes)
    db.commit()

    # 2. Seed Sample Students
    student1 = Student(
        apaar_id="9482-1049-5821",
        full_name="Ananya Soren",
        gender="Female",
        community="Santhal (Scheduled Tribe)",
        is_pvtg=False,
        state="Jharkhand",
        district="Ranchi",
        current_institute="Birla Institute of Technology (BIT Mesra)",
        aishe_code="U-0205",
        annual_family_income=140000,
        bank_name="State Bank of India",
        account_last_four="4108",
        aadhaar_seeded=True,
    )
    student2 = Student(
        apaar_id="8120-4921-3910",
        full_name="Birsa Munda",
        gender="Male",
        community="Munda (Scheduled Tribe)",
        is_pvtg=False,
        state="Jharkhand",
        district="Khunti",
        current_institute="Govt High School Khunti",
        aishe_code="S-8910",
        annual_family_income=90000,
        bank_name="Jharkhand Rajya Gramin Bank",
        account_last_four="1092",
        aadhaar_seeded=True,
    )
    db.add_all([student1, student2])
    db.commit()

    # 3. Seed Sample Application with Live Stages
    app1 = Application(
        application_id="MOTA-JH-2026-78419",
        student_apaar="9482-1049-5821",
        scheme_id="SCH-POST-MATRIC",
        stage=3,
        stage_name="State Nodal Officer Review",
        sanctioned_amount=42000,
        digilocker_verified=True,
        institute_verified=True,
        state_sanctioned=False,
        pfms_disbursed=False,
        soft_mismatch_resolved=True,
        soft_mismatch_detail="Name variation 'Ananya Soren' vs 'Ananya S' approved by BIT Mesra nodal officer.",
        pfms_tracking_id="PFMS-2026-JH-99214",
    )
    db.add(app1)

    # 4. Seed District Outreach Data (Zero-Dropout Radar)
    districts = [
        DistrictOutreach(
            district="Khunti",
            state="Jharkhand",
            udise_enrolled_st=8420,
            active_beneficiaries=7000,
            unreached_gap=1420,
            pvtg_concentration="High",
            status_flag="Action Required",
        ),
        DistrictOutreach(
            district="Mayurbhanj",
            state="Odisha",
            udise_enrolled_st=14500,
            active_beneficiaries=12320,
            unreached_gap=2180,
            pvtg_concentration="Very High",
            status_flag="Action Required",
        ),
        DistrictOutreach(
            district="Bastar",
            state="Chhattisgarh",
            udise_enrolled_st=11800,
            active_beneficiaries=10860,
            unreached_gap=940,
            pvtg_concentration="Moderate",
            status_flag="Optimal",
        ),
        DistrictOutreach(
            district="Alirajpur",
            state="Madhya Pradesh",
            udise_enrolled_st=9200,
            active_beneficiaries=7840,
            unreached_gap=1360,
            pvtg_concentration="High",
            status_flag="Action Required",
        ),
    ]
    db.add_all(districts)
    db.commit()
