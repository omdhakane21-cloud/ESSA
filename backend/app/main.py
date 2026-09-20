from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config.database import Base, engine
from app.routes import auth, events, team, gallery, registrations, messages

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
for folder in ["events", "gallery", "team"]:
    (UPLOAD_DIR / folder).mkdir(parents=True, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ESSA Website API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(team.router, prefix="/api/team", tags=["Team"])
app.include_router(gallery.router, prefix="/api/gallery", tags=["Gallery"])
app.include_router(registrations.router, prefix="/api/registrations", tags=["Registrations"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])

@app.get("/")
def root():
    return {"message": "ESSA API is running"}

@app.get("/api/health")
def health():
    return {"status": "ok"}
