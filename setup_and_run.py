#!/usr/bin/env python3
"""
Setup and Run Script for the Multi-Agent Stock Analysis System

This script automates the setup process for the stock analysis application.
It performs the following checks and actions:
1. Verifies Python version compatibility.
2. Checks for and installs required Python packages from requirements.txt.
3. Validates the .env file for API key configuration, creating it from .env.example if needed.
4. Launches the main Streamlit application (unified_stock_analysis_app.py).

Designed to provide a smooth startup experience for users.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path



def check_package_installed(package_name: str) -> bool:
    """Checks if a specific Python package is installed in the current environment."""
    spec = importlib.util.find_spec(package_name)
    return spec is not None

def install_requirements() -> bool:
    """Installs all packages listed in the requirements.txt file."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found.")
        return False
    
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Packages installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_env_file() -> bool:
    """Validates the .env file for Alpha Vantage API key configuration.
    If .env is missing, it attempts to create it from .env.example.
    Returns True if configured, False otherwise.
    """
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("⚠️  Warning: .env file not found.")
        print("   Creating .env file from template...")
        
        env_example = Path(__file__).parent / ".env.example"
        if env_example.exists():
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                content = src.read()
                dst.write(content)
            print("✅ .env file created from template.")
            print("⚠️  Please edit .env file and add your Alpha Vantage API key.")
            return False
        else:
            print("❌ Error: .env.example template not found.")
            return False
    
    # Check if API key is configured
    with open(env_file, 'r') as f:
        content = f.read()
        if "your_api_key_here" in content or "ALPHA_VANTAGE_API_KEY=" not in content:
            print("⚠️  Warning: Alpha Vantage API key not configured in .env file.")
            print("   Please edit .env file and add your API key.")
            print("   Get free API key at: https://www.alphavantage.co/support/#api-key")
            return False
    
    print("✅ Environment configuration found.")
    return True

def check_dependencies() -> bool:
    """Verifies that all core dependencies for the application are installed."""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'requests',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        if not check_package_installed(package):
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed.")
    return True

def run_application() -> bool:
    """Launches the main Streamlit application (unified_stock_analysis_app.py).
    Handles user interruption (Ctrl+C) gracefully.
    """
    app_file = Path(__file__).parent / "unified_stock_analysis_app.py"
    
    if not app_file.exists():
        print("❌ Error: unified_stock_analysis_app.py not found.")
        return False
    
    print("🚀 Launching Multi-Agent Stock Analysis System...")
    print("   The application will open in your default web browser.")
    print("   Press Ctrl+C to stop the application.")
    print("\n" + "="*60)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", str(app_file)
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user.")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False
    
    return True

def main():
    """Orchestrates the setup checks and application launch sequence."""
    print("🤖 Multi-Agent Stock Analysis System - Setup & Run")
    print("="*60)
    
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_requirements():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            return
    
    # Check environment configuration
    if not check_env_file():
        print("\n⚠️  Please configure your .env file before running the application.")
        print("\nSteps to configure:")
        print("1. Get free API key: https://www.alphavantage.co/support/#api-key")
        print("2. Edit .env file and replace 'your_api_key_here' with your actual API key")
        print("3. Run this script again")
        return
    
    print("\n✅ All checks passed! Ready to launch application.")
    print("\nFeatures available:")
    print("• 💬 Natural Language Stock Queries")
    print("• 📊 Interactive Stock Visualizations")
    print("• 📰 Real-time News Analysis")
    print("• 🤖 Multi-Agent Architecture")
    
    input("\nPress Enter to launch the application...")
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main()