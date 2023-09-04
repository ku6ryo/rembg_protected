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
    result = remove(file.file.read())
    return StreamingResponse(content=BytesIO(result), media_type="application/octet-stream")