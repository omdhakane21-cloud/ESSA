from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.auth import get_current_admin
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse
from app.utils.file_upload import save_upload

router = APIRouter()
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "uploads" / "events"

@router.get("/", response_model=list[EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.date.asc(), Event.id.desc()).all()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id:int, db:Session=Depends(get_db)):
    event=db.get(Event,event_id)
    if not event: raise HTTPException(404,"Event not found")
    return event

@router.post("/", response_model=EventResponse, dependencies=[Depends(get_current_admin)])
def create_event(data:EventCreate, db:Session=Depends(get_db)):
    item=Event(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

@router.put("/{event_id}", response_model=EventResponse, dependencies=[Depends(get_current_admin)])
def update_event(event_id:int,data:EventCreate,db:Session=Depends(get_db)):
    item=db.get(Event,event_id)
    if not item: raise HTTPException(404,"Event not found")
    for k,v in data.model_dump().items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item

@router.delete("/{event_id}", dependencies=[Depends(get_current_admin)])
def delete_event(event_id:int,db:Session=Depends(get_db)):
    item=db.get(Event,event_id)
    if not item: raise HTTPException(404,"Event not found")
    db.delete(item); db.commit(); return {"message":"Event deleted"}

@router.post("/{event_id}/image", response_model=EventResponse, dependencies=[Depends(get_current_admin)])
async def upload_event_image(event_id:int,file:UploadFile=File(...),db:Session=Depends(get_db)):
    item=db.get(Event,event_id)
    if not item: raise HTTPException(404,"Event not found")
    item.image=await save_upload(file,UPLOAD_DIR)
    db.commit(); db.refresh(item); return item
