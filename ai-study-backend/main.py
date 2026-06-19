import asyncio
import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Study Gemini Automation Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error Keywords
ERROR_KEYWORDS = ["Quota exceeded", "429", "Limit reached", "daily limit", "Error", "cannot fulfill"]

class ProjectGenerationRequest(BaseModel):
    selected_model: str
    project_goal: str
    language: str
    include_core: str
    file_name: str

async def run_mdflow_task(req: ProjectGenerationRequest):
    cmd = [
        "md", "study.gemini.md",
        "--_yes",
        "--_no-menu",
        "--_quiet",
        "--_selected_model", req.selected_model,
        "--_project_goal", req.project_goal,
        "--_language", req.language,
        "--_include_core", req.include_core,
        "--_file_name", req.file_name
    ]
    
    # 비동기 프로세스 실행
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env={**os.environ, "TERM": "xterm-256color"}
    )
    
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        yield f"data: {line.decode('utf-8', errors='ignore').strip()}\n\n"
            
    await process.wait()

@app.post("/api/generate-project")
async def generate_project(request: ProjectGenerationRequest):
    return StreamingResponse(
        run_mdflow_task(request), 
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)