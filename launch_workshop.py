#!/usr/bin/env python3
"""
Qdrant Workshop Launcher
This script launches JupyterLab and opens the first notebook
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_setup():
    """Check if the workshop is properly set up"""
    print("🔍 Checking workshop setup...")
    
    # Check required files
    required_files = [
        "01_fundamentals.ipynb",
        "utils.py", 
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    # Check if .env exists and is configured
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Please run setup first.")
        print("   Run: ./setup.sh (Linux/Mac) or setup.bat (Windows)")
        return False
    
    # Check if .env has real values
    with open('.env', 'r') as f:
        content = f.read()
        if 'your-cluster.qdrant.io' in content or 'your-api-key' in content:
            print("⚠️  .env file contains placeholder values.")
            print("   Please edit .env with your Qdrant Cloud credentials.")
            return False
    
    print("✅ Workshop setup looks good!")
    return True

def launch_jupyter():
    """Launch JupyterLab"""
    print("\n🚀 Launching JupyterLab...")
    
    try:
        # Check if JupyterLab is installed
        import jupyterlab
        print("✅ JupyterLab is available")
    except ImportError:
        print("❌ JupyterLab not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "jupyterlab"])
            print("✅ JupyterLab installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install JupyterLab")
            return False
    
    # Launch JupyterLab in background
    try:
        print("🌐 Starting JupyterLab server...")
        process = subprocess.Popen([
            sys.executable, "-m", "jupyter", "lab",
            "--no-browser",
            "--port=8888"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ JupyterLab server started successfully")
            print("🌐 Opening workshop in browser...")
            
            # Open first notebook
            notebook_url = "http://localhost:8888/lab/tree/01_fundamentals.ipynb"
            webbrowser.open(notebook_url)
            
            print(f"\n🎉 Workshop launched!")
            print(f"📚 First notebook: {notebook_url}")
            print(f"🔧 JupyterLab dashboard: http://localhost:8888/lab")
            print(f"\n💡 Tips:")
            print(f"   - Work through notebooks in order (01 → 05)")
            print(f"   - Check README.md for detailed instructions")
            print(f"   - Use test_setup.py to verify your setup")
            print(f"\n🛑 To stop the server, press Ctrl+C in this terminal")
            
            # Keep the process running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping JupyterLab server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped")
            
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ JupyterLab failed to start:")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to launch JupyterLab: {e}")
        return False

def main():
    """Main launcher function"""
    print("🚀 Qdrant Vector Database Workshop Launcher")
    print("=" * 50)
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup incomplete. Please fix the issues above.")
        print("\n📋 Quick setup guide:")
        print("1. Run setup script: ./setup.sh (Linux/Mac) or setup.bat (Windows)")
        print("2. Edit .env file with your Qdrant Cloud credentials")
        print("3. Run this launcher again")
        return False
    
    # Launch workshop
    if launch_jupyter():
        return True
    else:
        print("\n❌ Failed to launch workshop.")
        print("Try running manually:")
        print("   jupyter lab")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
