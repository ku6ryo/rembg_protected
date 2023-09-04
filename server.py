from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO

app = FastAPI()

@app.get("/")
def read_root():
    return { "status": "Working" }

@app.post("/remove")
async def removeBg(request: Request, file: UploadFile = File(...)):
    if request.headers["X-API-KEY"] != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    b = file.file.read()
    if len(b) > 1024 * 1024 * 1:
        raise HTTPException(status_code=400, detail="File size should be less than 5MB")
    result = remove(b)
    return StreamingResponse(content=BytesIO(result), media_type="application/octet-stream")