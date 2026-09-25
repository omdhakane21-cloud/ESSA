from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.auth import get_current_admin
from app.models.registration import Registration
from app.schemas.registration import RegistrationCreate, RegistrationResponse, RegistrationStatus

router=APIRouter()

@router.post("/",response_model=RegistrationResponse)
def create_registration(data:RegistrationCreate,db:Session=Depends(get_db)):
    item=Registration(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.get("/",response_model=list[RegistrationResponse],dependencies=[Depends(get_current_admin)])
def list_registrations(db:Session=Depends(get_db)):
    return db.query(Registration).order_by(Registration.created_at.desc()).all()

@router.patch("/{registration_id}/status",response_model=RegistrationResponse,dependencies=[Depends(get_current_admin)])
def update_status(registration_id:int,data:RegistrationStatus,db:Session=Depends(get_db)):
    if data.status not in {"pending","approved","rejected","attended"}: raise HTTPException(400,"Invalid status")
    item=db.get(Registration,registration_id)
    if not item: raise HTTPException(404,"Registration not found")
    item.status=data.status; db.commit(); db.refresh(item); return item

@router.delete("/{registration_id}",dependencies=[Depends(get_current_admin)])
def delete_registration(registration_id:int,db:Session=Depends(get_db)):
    item=db.get(Registration,registration_id)
    if not item: raise HTTPException(404,"Registration not found")
    db.delete(item); db.commit(); return {"message":"Registration deleted"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.config.database import get_db
from app.middleware.auth import get_current_admin

from app.models.registration import Registration
from app.models.registration_control import RegistrationControl

from app.schemas.registration import (
    RegistrationCreate,
    RegistrationResponse,
    RegistrationStatus
)

router = APIRouter()


# =========================================================
# PUBLIC - GET CURRENTLY OPEN REGISTRATION
# =========================================================

@router.get("/active")
def get_active_registration(db: Session = Depends(get_db)):

    control = (
        db.query(RegistrationControl)
        .filter(RegistrationControl.is_open == True)
        .first()
    )

    if not control:
        return {
            "open": False,
            "message": "Registration is currently closed."
        }

    return {
        "open": True,
        "event_id": control.event_id,
        "requirements": control.requirements,
        "opened_at": control.opened_at
    }


# =========================================================
# PUBLIC - REGISTER MEMBER
# =========================================================

@router.post("/", response_model=RegistrationResponse)
def create_registration(
    data: RegistrationCreate,
    db: Session = Depends(get_db)
):

    if not data.event_id:
        raise HTTPException(
            status_code=400,
            detail="Please select an event."
        )

    control = (
        db.query(RegistrationControl)
        .filter(
            RegistrationControl.event_id == data.event_id,
            RegistrationControl.is_open == True
        )
        .first()
    )

    if not control:
        raise HTTPException(
            status_code=403,
            detail="Registration for this event is currently closed."
        )

    # Prevent duplicate registration
    existing = (
        db.query(Registration)
        .filter(
            Registration.event_id == data.event_id,
            Registration.email == data.email
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="This email is already registered for this event."
        )

    item = Registration(**data.model_dump())

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


# =========================================================
# ADMIN - START REGISTRATION
# =========================================================

@router.post(
    "/start/{event_id}",
    dependencies=[Depends(get_current_admin)]
)
def start_registration(
    event_id: int,
    requirements: str = "",
    db: Session = Depends(get_db)
):

    control = (
        db.query(RegistrationControl)
        .filter(RegistrationControl.event_id == event_id)
        .first()
    )

    if not control:

        control = RegistrationControl(
            event_id=event_id,
            is_open=True,
            requirements=requirements,
            opened_at=datetime.utcnow(),
            closed_at=None
        )

        db.add(control)

    else:

        control.is_open = True
        control.requirements = requirements
        control.opened_at = datetime.utcnow()
        control.closed_at = None

    db.commit()
    db.refresh(control)

    return {
        "message": "Registration started successfully.",
        "event_id": event_id,
        "open": True,
        "opened_at": control.opened_at
    }


# =========================================================
# ADMIN - STOP REGISTRATION
# =========================================================

@router.post(
    "/stop/{event_id}",
    dependencies=[Depends(get_current_admin)]
)
def stop_registration(
    event_id: int,
    db: Session = Depends(get_db)
):

    control = (
        db.query(RegistrationControl)
        .filter(RegistrationControl.event_id == event_id)
        .first()
    )

    if not control:
        raise HTTPException(
            status_code=404,
            detail="Registration control not found."
        )

    control.is_open = False
    control.closed_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Registration stopped successfully.",
        "event_id": event_id,
        "open": False
    }


# =========================================================
# ADMIN - REGISTRATION STATUS
# =========================================================

@router.get(
    "/controls",
    dependencies=[Depends(get_current_admin)]
)
def registration_controls(
    db: Session = Depends(get_db)
):

    controls = (
        db.query(RegistrationControl)
        .order_by(RegistrationControl.event_id)
        .all()
    )

    return [
        {
            "id": c.id,
            "event_id": c.event_id,
            "is_open": c.is_open,
            "requirements": c.requirements,
            "opened_at": c.opened_at,
            "closed_at": c.closed_at
        }
        for c in controls
    ]


# =========================================================
# ADMIN - VIEW ALL MEMBERS
# =========================================================

@router.get(
    "/",
    response_model=list[RegistrationResponse],
    dependencies=[Depends(get_current_admin)]
)
def list_registrations(
    db: Session = Depends(get_db)
):

    return (
        db.query(Registration)
        .order_by(Registration.created_at.desc())
        .all()
    )


# =========================================================
# ADMIN - CHANGE MEMBER STATUS
# =========================================================

@router.patch(
    "/{registration_id}/status",
    response_model=RegistrationResponse,
    dependencies=[Depends(get_current_admin)]
)
def update_status(
    registration_id: int,
    data: RegistrationStatus,
    db: Session = Depends(get_db)
):

    if data.status not in {
        "pending",
        "approved",
        "rejected",
        "attended"
    }:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    item = db.get(Registration, registration_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Registration not found"
        )

    item.status = data.status

    db.commit()
    db.refresh(item)

    return item


# =========================================================
# ADMIN - DELETE REGISTRATION
# =========================================================

@router.delete(
    "/{registration_id}",
    dependencies=[Depends(get_current_admin)]
)
def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db)
):

    item = db.get(Registration, registration_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Registration not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Registration deleted"
    }
