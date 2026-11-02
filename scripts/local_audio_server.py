import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title="HörLabor Local Audio Range Server")

# 启用全局 CORS 允许前端本地 Vite 访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_ROOT = r"D:\GermanCorpus\processed\tracks"
RAW_ROOT = r"D:\GermanCorpus\raw"

@app.get("/")
def index():
    return {"status": "ok", "service": "HoerLabor Audio Server", "audio_root": AUDIO_ROOT}

@app.get("/audio/tracks/{filename}")
async def get_track_audio(filename: str, request: Request):
    """
    提供支持 HTTP 206 Partial Content (Byte-Range) 的音频流服务，
    确保在 Chrome/Safari 及移动端拖动时间轴和单句 Seek 畅通无阻。
    """
    file_path = os.path.join(AUDIO_ROOT, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename,
        headers={"Accept-Ranges": "bytes", "Cache-Control": "public, max-age=86400"}
    )

if __name__ == "__main__":
    print(f"[STARTING SERVER] Mounting {AUDIO_ROOT} on port 8080...")
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
