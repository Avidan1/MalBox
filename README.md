# MalBox: High-Performance Automated Malware Analysis Pipeline

A high-performance, asynchronous sandbox environment designed to analyze potentially malicious files in isolated containers. This project demonstrates full-stack engineering, distributed systems, and cybersecurity principles.

## 🏗 Architecture & Technologies

The system is built with a **decoupled, microservices-oriented architecture** to ensure scalability and security:

- **API Layer:** FastAPI (Python) - Provides a high-performance interface for file submission and status polling.
- **Task Queue:** Redis & RQ - Manages asynchronous execution to prevent blocking the API during long analysis tasks.
- **Worker Engine:** Docker-out-of-Docker (DooD) - A specialized Linux-based worker that manages the lifecycle of analysis containers.
- **Isolation:** Docker Containers - Each sample is executed in a strictly constrained environment (CPU/RAM limits) to prevent host compromise.
- **Networking (Upcoming):** Scapy-based packet sniffing for real-time network behavior analysis.

## 🚀 Key Engineering Features

- **Asynchronous Processing:** Utilizes a Producer-Consumer pattern to handle multiple analysis requests simultaneously.
- **Resource Hardening:** Implements Docker Cgroup limits (Memory/CPU) to mitigate Denial-of-Service (DoS) attempts by malware.
- **Cross-Platform Compatibility:** Engineered to work seamlessly on Windows (via WSL2/Docker Desktop) and Linux.
- **Deterministic Cleanup:** Automated container lifecycle management ensures no "zombie" processes or containers leak resources.

## 🛠 Getting Started

### Prerequisites
- Docker Desktop (with WSL2 backend on Windows)
- Python 3.9+
- Redis (Handled via Docker Compose)

### Installation & Running
1. **Clone the repository:**
   ```
   git clone [https://github.com/Avidan1/MalBox.git](https://github.com/Avidan1/MalBox.git)
   cd malbox
   ```

2. **Set up the backend:**
    ```
    cd backend
    python -m venv venv
    source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
3. **Launch Infrastructure:** Using Docker Compose to spin up Redis and the Worker:
    ```
    docker-compose up --build
    ```
4. **Start the API:**
    ```
    python main.py
    ```

## 🗺 Roadmap & Future Development

- [x] **Phase 1: Core MVP** - Synchronous container execution.
- [x] **Phase 2: Scalable Infrastructure** - Redis integration and Async Workers.
- [ ] **Phase 3: Network Analysis & Forensics** - Real-time traffic sniffing and PCAP generation using Scapy.
- [ ] **Phase 4: Security Hardening** - Implementing advanced network isolation (no internet access for samples).
- [ ] **Phase 5: Web Dashboard** - A React-based frontend to visualize analysis reports and network graphs.

## 👨‍💻 Interview Discussion Points

- **Why Redis?** To decouple the long-running analysis from the user-facing API.
- **Why DooD?** To enable a Linux-native worker to control the host's Docker engine, bypassing Windows compatibility issues with process forking.
- **Isolation Strategy:** Using read-only volumes and resource constraints to maintain host integrity.