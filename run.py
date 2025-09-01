#!/usr/bin/env python3
"""
Motorcycle Analysis Dashboard Runner

This script provides a convenient way to run the dashboard with proper setup.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    required_packages = ['streamlit', 'pandas', 'numpy', 'plotly', 'matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_data_files():
    """Check if data files exist or can be generated."""
    csv_file = Path("faired_bikes_ratings_india_1to10L_aug2025.csv")
    
    if not csv_file.exists():
        print("📊 Generating data file...")
        try:
            subprocess.run([sys.executable, "main.py"], check=True, capture_output=True)
            print("✅ Data file generated successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to generate data file: {e}")
            return False
    else:
        print("✅ Data file exists")
    
    return True

def run_dashboard():
    """Run the Streamlit dashboard."""
    print("🚀 Starting Motorcycle Analysis Dashboard...")
    print("📱 Dashboard will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "bike_app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Thank you for using Motorcycle Analysis Dashboard!")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

def main():
    """Main function to setup and run the dashboard."""
    print("🏍️  Motorcycle Analysis Dashboard")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("bike_app.py").exists():
        print("❌ bike_app.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check/generate data files
    if not check_data_files():
        sys.exit(1)
    
    # Run the dashboard
    run_dashboard()

if __name__ == "__main__":
    main()