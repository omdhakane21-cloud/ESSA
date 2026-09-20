# ESSA Website Backend

## Run
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs

Change ADMIN_PASSWORD and SECRET_KEY in `.env` before deployment.
