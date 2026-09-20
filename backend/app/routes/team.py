from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.auth import get_current_admin
from app.models.team import TeamMember
from app.schemas.team import TeamCreate, TeamResponse
from app.utils.file_upload import save_upload

router=APIRouter()
UPLOAD_DIR=Path(__file__).resolve().parents[1]/"uploads"/"team"

@router.get("/",response_model=list[TeamResponse])
def list_team(db:Session=Depends(get_db)):
    return db.query(TeamMember).filter(TeamMember.active==1).order_by(TeamMember.display_order,TeamMember.id).all()

@router.get("/{member_id}",response_model=TeamResponse)
def get_member(member_id:int,db:Session=Depends(get_db)):
    item=db.get(TeamMember,member_id)
    if not item: raise HTTPException(404,"Team member not found")
    return item

@router.post("/",response_model=TeamResponse,dependencies=[Depends(get_current_admin)])
def create_member(data:TeamCreate,db:Session=Depends(get_db)):
    item=TeamMember(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.put("/{member_id}",response_model=TeamResponse,dependencies=[Depends(get_current_admin)])
def update_member(member_id:int,data:TeamCreate,db:Session=Depends(get_db)):
    item=db.get(TeamMember,member_id)
    if not item: raise HTTPException(404,"Team member not found")
    for k,v in data.model_dump().items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

@router.delete("/{member_id}",dependencies=[Depends(get_current_admin)])
def delete_member(member_id:int,db:Session=Depends(get_db)):
    item=db.get(TeamMember,member_id)
    if not item: raise HTTPException(404,"Team member not found")
    db.delete(item); db.commit(); return {"message":"Team member deleted"}

@router.post("/{member_id}/photo",response_model=TeamResponse,dependencies=[Depends(get_current_admin)])
async def upload_team_photo(member_id:int,file:UploadFile=File(...),db:Session=Depends(get_db)):
    item=db.get(TeamMember,member_id)
    if not item: raise HTTPException(404,"Team member not found")
    item.photo=await save_upload(file,UPLOAD_DIR)
    db.commit(); db.refresh(item); return item
