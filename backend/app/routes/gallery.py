from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.middleware.auth import get_current_admin
from app.models.gallery import GalleryImage
from app.schemas.gallery import GalleryResponse
from app.utils.file_upload import save_upload

router=APIRouter()
UPLOAD_DIR=Path(__file__).resolve().parents[1]/"uploads"/"gallery"

@router.get("/",response_model=list[GalleryResponse])
def list_gallery(db:Session=Depends(get_db)):
    return db.query(GalleryImage).order_by(GalleryImage.created_at.desc()).all()

@router.post("/",response_model=GalleryResponse,dependencies=[Depends(get_current_admin)])
async def add_gallery(title:str="",description:str="",file:UploadFile=File(...),db:Session=Depends(get_db)):
    item=GalleryImage(title=title or None,description=description or None,image=await save_upload(file,UPLOAD_DIR))
    db.add(item); db.commit(); db.refresh(item); return item

@router.delete("/{image_id}",dependencies=[Depends(get_current_admin)])
def delete_gallery(image_id:int,db:Session=Depends(get_db)):
    item=db.get(GalleryImage,image_id)
    if not item: raise HTTPException(404,"Gallery image not found")
    db.delete(item); db.commit(); return {"message":"Gallery image deleted"}
