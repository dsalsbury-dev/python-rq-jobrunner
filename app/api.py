import uuid

from fastapi import FastAPI, HTTPException, Response, Header

from app.logging import configure_logging, request_id_var
from app.settings import get_settings

configure_logging()
app = FastAPI(title="python-rq-jobrunner", version="0.1.0")


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if settings.api_key is None:
        return
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.middleware("http")
async def add_request_id(request, call_next):
    rid = request.headers.get("x-request-id") or str(uuid.uuid4())
    token = request_id_var.set(rid)
    try:
        resp: Response = await call_next(request)
        resp.headers['x-request-id'] = rid
        return resp
    finally:
        request_id_var.reset(token)


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/readyz")
def readyz():
    # TODO: add DB/Redis checks later once those modules are implemented
    return {"ready": True}
