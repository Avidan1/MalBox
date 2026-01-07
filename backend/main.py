from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid
from redis import Redis
from rq import Queue
from sandbox_manager import run_in_sandbox

app = FastAPI()

# Setup Redis connection and Task Queue
redis_conn = Redis(host='localhost', port=6379)
task_queue = Queue('analysis_queue', connection=redis_conn)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_file(file: UploadFile = File(...)):
    # 1. Save file temporarily
    file_id = str(uuid.uuid4())
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.abspath(os.path.join(UPLOAD_DIR, filename)).replace("\\", "/")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Enqueue the task to Redis
    # The worker will pick up 'run_in_sandbox' and execute it
    job = task_queue.enqueue(run_in_sandbox, file_path)
    
    return {
        "job_id": job.get_id(),
        "status": "queued",
        "message": "File received. Analysis started in the background."
    }

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    # Retrieve job status from Redis
    job = task_queue.fetch_job(job_id)
    if not job:
        return {"error": "Job ID not found."}
    
    return {
        "job_id": job_id,
        "status": job.get_status(),
        "result": job.result # This will contain the dict returned by run_in_sandbox
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)