#!/usr/bin/env python3
"""
Script untuk menjalankan aplikasi FastAPI dengan mudah
"""

import subprocess
import sys
import os
import time

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ Docker tidak ditemukan. Pastikan Docker sudah terinstall.")
        return False

def start_mongodb():
    """Start MongoDB using docker-compose"""
    print("🚀 Starting MongoDB with Docker...")
    try:
        result = subprocess.run(['docker', 'compose', 'up', '-d'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MongoDB berhasil dijalankan")
            print("📊 Mongo Express: http://localhost:8081")
            return True
        else:
            print(f"❌ Error starting MongoDB: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ docker-compose tidak ditemukan.")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies berhasil diinstall")
            return True
        else:
            print(f"❌ Error installing dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def start_api():
    """Start FastAPI application"""
    print("🌟 Starting FastAPI application...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 API Base URL: http://localhost:8000")
    print("\n⏹️  Press Ctrl+C to stop the application\n")
    
    try:
        # Run uvicorn
        subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', 
                       '--host', '0.0.0.0', '--port', '8000', '--reload'])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main function"""
    print("\n🐍 Python MongoDB REST API")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ File main.py tidak ditemukan. Pastikan Anda berada di directory yang benar.")
        sys.exit(1)
    
    # Check Docker
    if not check_docker():
        print("❌ Docker tidak berjalan. Silakan start Docker terlebih dahulu.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Gagal menginstall dependencies.")
        sys.exit(1)
    
    # Start MongoDB
    if not start_mongodb():
        print("❌ Gagal menjalankan MongoDB.")
        sys.exit(1)
    
    # Wait a bit for MongoDB to be ready
    print("⏳ Waiting for MongoDB to be ready...")
    time.sleep(5)
    
    # Start API
    start_api()

if __name__ == "__main__":
    main()

