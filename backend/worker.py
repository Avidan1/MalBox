import os
from redis import Redis
from rq import Worker, Queue

# Define the queue name to listen to
listen = ['analysis_queue']

# Fetch Redis host from environment variables (default to localhost)
# When using docker-compose, this will be 'redis'
redis_host = os.getenv('REDIS_HOST', 'localhost')
conn = Redis(host=redis_host, port=6379)

if __name__ == '__main__':
    # Initialize the queue with the connection
    queue = Queue('analysis_queue', connection=conn)
    
    # Initialize the worker with the connection and the specific queue
    # This approach is more robust and avoids 'Connection' import issues
    worker = Worker([queue], connection=conn)
    
    print(f"--- Malware Sandbox Worker is Running (Host: {redis_host}) ---")
    worker.work()