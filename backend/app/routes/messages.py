from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.auth import get_current_admin
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse

router=APIRouter()

@router.post("/",response_model=MessageResponse)
def create_message(data:MessageCreate,db:Session=Depends(get_db)):
    item=Message(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.get("/",response_model=list[MessageResponse],dependencies=[Depends(get_current_admin)])
def list_messages(db:Session=Depends(get_db)):
    return db.query(Message).order_by(Message.created_at.desc()).all()

@router.patch("/{message_id}/read",response_model=MessageResponse,dependencies=[Depends(get_current_admin)])
def mark_read(message_id:int,db:Session=Depends(get_db)):
    item=db.get(Message,message_id)
    if not item: raise HTTPException(404,"Message not found")
    item.is_read=1; db.commit(); db.refresh(item); return item

@router.patch("/{message_id}/unread",response_model=MessageResponse,dependencies=[Depends(get_current_admin)])
def mark_unread(message_id:int,db:Session=Depends(get_db)):
    item=db.get(Message,message_id)
    if not item: raise HTTPException(404,"Message not found")
    item.is_read=0; db.commit(); db.refresh(item); return item

@router.delete("/{message_id}",dependencies=[Depends(get_current_admin)])
def delete_message(message_id:int,db:Session=Depends(get_db)):
    item=db.get(Message,message_id)
    if not item: raise HTTPException(404,"Message not found")
    db.delete(item); db.commit(); return {"message":"Message deleted"}
