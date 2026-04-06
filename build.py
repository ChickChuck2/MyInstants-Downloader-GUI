import subprocess
import sys
import os
import shutil

def build():
    print("====================================")
    print("  Building Standalone Executable    ")
    print("====================================")
    
    # Ensure pyinstaller is installed
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # PyInstaller arguments
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",         # No black command prompt window
        "--onefile",           # Compress to a single .exe
        "--icon=assets/main.ico",
        "--add-data=assets;assets", # Bundle the entire assets folder
        "--name", "MyInstants_Downloader",
        "main.py"
    ]
    
    print("\nRunning PyInstaller...")
    try:
        subprocess.run(cmd, check=True)
        print("\n[SUCCESS] Build complete! Your standalone executable is located in the 'dist' folder.")
    except subprocess.CalledProcessError:
        print("\n[ERROR] Build failed.")
        sys.exit(1)

if __name__ == "__main__":
    build()
