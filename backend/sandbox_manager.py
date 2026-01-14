import docker
import uuid

client = docker.from_env()
# BASE START SCAN ONLY PYTHON FILES
def run_in_sandbox(host_path: str):
    """
    host_path is the absolute path on the Windows Host
    Example: C:/Users/Avidan/Documents/.../uploads/file.py
    """
    container_name = f"analysis_{uuid.uuid4().hex[:8]}"
    
    # Extract filename and directory from the Windows path string
    file_name = host_path.split("/")[-1]
    # Get the directory by removing the filename from the end
    host_dir = "/".join(host_path.split("/")[:-1])

    try:
        container = client.containers.run(
            image="python:3.13-slim",
            command=["python", f"/app/{file_name}"],
            volumes={
                host_dir: { # This is the Windows path that Docker Engine understands
                    'bind': '/app', 
                    'mode': 'ro'
                }
            },
            working_dir="/app",
            detach=True,
            mem_limit="128m",
            nano_cpus=500000000,
        )

        result = container.wait(timeout=10)
        logs = container.logs().decode("utf-8")
        
        return {
            "exit_code": result["StatusCode"],
            "logs": logs,
            "status": "completed"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        try:
            container.remove(force=True)
        except:
            pass