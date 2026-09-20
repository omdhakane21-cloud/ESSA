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
