#!/usr/bin/env python3
"""
Setup and Run Script for the React + FastAPI Stock Analysis System

This script automates the installation and run process for the new architecture:
1. Installs backend dependencies from api/requirements.txt.
2. Performs Node package installation via pnpm install.
3. Launches the FastAPI uvicorn backend on port 8000.
4. Launches the Vite React frontend via pnpm dev on port 5173.
"""

import sys
import os
import subprocess
import time
import importlib.util
from pathlib import Path

def check_package_installed(package_name: str) -> bool:
    """Checks if a specific Python package is installed."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_python_requirements() -> bool:
    """Installs all backend requirements from api/requirements.txt."""
    req_file = Path(__file__).parent / "api" / "requirements.txt"
    if not req_file.exists():
        print("❌ Error: api/requirements.txt not found.")
        return False
    
    print("📦 Installing python backend packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(req_file)
        ])
        print("✅ Python packages installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Python packages: {e}")
        return False

def check_dependencies() -> bool:
    required = ['fastapi', 'uvicorn', 'requests', 'pandas', 'dotenv']
    missing = [pkg for pkg in required if not check_package_installed(pkg)]
    if missing:
        print(f"⚠️ Missing packages: {', '.join(missing)}")
        return False
    return True

def install_pnpm_packages() -> bool:
    """Checks if node_modules exists, otherwise installs pnpm dependencies."""
    node_modules = Path(__file__).parent / "node_modules"
    if node_modules.exists():
        print("✅ node_modules found. Skipping package installation.")
        return True
    
    print("📦 Installing frontend dependencies using pnpm...")
    try:
        # Run pnpm install
        subprocess.check_call("pnpm install", shell=True)
        print("✅ Frontend packages installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing frontend packages via pnpm: {e}")
        return False

def run_development_servers():
    """Runs FastAPI and Vite dev servers concurrently."""
    print("\n🚀 Launching Development Environment...")
    print("   FastAPI backend will run on: http://localhost:8000")
    print("   Vite React frontend will run on: http://localhost:5173")
    print("   Press Ctrl+C to stop both servers.")
    print("="*60 + "\n")
    
    processes = []
    try:
        # Start FastAPI
        backend_cmd = [sys.executable, "-m", "uvicorn", "api.index:app", "--port", "8000", "--reload"]
        backend_process = subprocess.Popen(
            backend_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(backend_process)
        print("🔥 Starting FastAPI backend (Uvicorn)...")
        time.sleep(1.5)
        
        # Start Frontend using pnpm dev
        frontend_process = subprocess.Popen(
            "pnpm dev",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(frontend_process)
        print("🔥 Starting React frontend (Vite via pnpm dev)...")
        
        # Wait and read logs from processes
        print("\n💡 Servers running. Logs will stream below:\n")
        
        # Non-blocking log printer for active console checking
        while True:
            # Check backend output
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly.")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend dev server stopped unexpectedly.")
                break
                
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping development servers...")
    except Exception as e:
        print(f"❌ Execution error: {e}")
    finally:
        # Terminate all launched processes
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=3)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        print("✅ Clean shutdown complete.")

def main():
    print("🤖 AI Stock Analysis System - Modern Migration Setup")
    print("="*60)
    
    # 1. Install/Check Python backend requirements
    if not check_dependencies():
        if not install_python_requirements():
            print("❌ Failed to resolve python backend requirements.")
            return
            
    # 2. Check Node packages
    if not install_pnpm_packages():
        print("❌ Failed to resolve frontend packages. Make sure 'pnpm' is installed and path-accessible.")
        return
        
    # 3. Run development servers concurrently
    run_development_servers()

if __name__ == "__main__":
    main()