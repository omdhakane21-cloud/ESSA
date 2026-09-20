# ESSA Website

Full-stack college club website for the Electronics Engineering Students Association.

## Structure
- frontend: public website + admin UI
- backend: FastAPI API + SQLAlchemy + SQLite
- database: created automatically as `essa.db`

## Start backend
Open a terminal in `backend`:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `frontend/index.html` in a browser or use VS Code Live Server.

Admin:
`frontend/admin/login.html`

Default local admin:
username: `admin`
password: `ChangeMe123!`

Change credentials in `backend/.env`.

## Replace
1. ESSA logo: `frontend/assets/logos/essa-logo.png`
2. College logo: `frontend/assets/logos/college-logo.png`
3. ESSA photos in `frontend/assets/images/`
4. College name, president, mentor and coordinator details in HTML.
5. Instagram and LinkedIn links in `frontend/index.html`.
