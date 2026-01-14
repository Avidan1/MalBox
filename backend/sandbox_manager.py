import socket
import docker
import uuid
import threading
import os
from scapy.all import sniff, wrpcap

client = docker.from_env()

def capture_traffic(job_id: str, stop_event: threading.Event):
    """
    Background thread to capture network packets using Scapy.
    """
    os.makedirs("uploads/pcap", exist_ok=True)
    job_name = job_id.replace(".py", "")
    pcap_path = f"uploads/pcap/{job_name}.pcap"
    try:
        # Sniff packets. We'll capture everything initially. 
        # In a production environment, we'd filter by the container's IP.
        packets = sniff(
            timeout=15,
            iface="eth0",
            stop_filter=lambda x: stop_event.is_set(),
            store=1
            )
    except Exception as e:
        print(f"Error capturing traffic for {job_id}: {e}")
        packets = []
    
    # Save captured traffic to a forensic PCAP file
    wrpcap(pcap_path, packets)
    print(f"--- Traffic for {job_id} saved to {pcap_path} ---")
    
# TODO: Current scope is limited to Python file analysis. Expand sandbox capabilities to support additional file types and executables.
def run_in_sandbox(host_path: str):
    """
    host_path is the absolute path on the Windows Host
    Example: C:/Users/Avidan/Documents/.../uploads/file.py
    """
    # job_id = file_id from main.py
    # Extract filename and directory from the Windows path string
    job_id = host_path.split("/")[-1]# it is ending in .py
    # Get the directory by removing the filename from the end
    host_dir = "/".join(host_path.split("/")[:-1])

    stop_sniffing = threading.Event()
    
    sniffer_thread = threading.Thread(
        target=capture_traffic, 
        args=(job_id, stop_sniffing)
    )
    sniffer_thread.start()
    
    worker_container_id = socket.gethostname()
    try:
        container = client.containers.run(
            image="python:3.13-slim",
            command=["python", f"/app/{job_id}"],
            volumes={
                host_dir: { # This is the Windows path that Docker Engine understands
                    'bind': '/app', 
                    'mode': 'ro'
                }
            },
            network_mode=f"container:{worker_container_id}",
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
        # 3. Cleanup: Stop sniffer and remove container
        stop_sniffing.set()
        sniffer_thread.join()
        try:
            container.remove(force=True)
        except:
            pass