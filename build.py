#!/usr/bin/env python3
"""
Cross-platform build script
Package invoiceprint as standalone executable
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def get_platform_info():
    """Get platform information"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "darwin":
        platform_name = "macos"
    elif system == "windows":
        platform_name = "windows"
    elif system == "linux":
        platform_name = "linux"
    else:
        platform_name = system
    
    # Architecture
    if machine in ("x86_64", "amd64"):
        arch = "x64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = machine
    
    return platform_name, arch


def clean_build():
    """Clean build directories"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"Cleaning directory: {dir_path}")
            shutil.rmtree(dir_path)
    
    for pattern in files_to_clean:
        for file_path in Path(".").glob(pattern):
            print(f"Cleaning file: {file_path}")
            file_path.unlink()


def build_executable():
    """Build executable"""
    platform_name, arch = get_platform_info()
    
    print(f"Platform: {platform_name}")
    print(f"Architecture: {arch}")
    print("-" * 40)
    
    # Output filename
    if platform_name == "windows":
        exe_name = "invoiceprint.exe"
    else:
        exe_name = "invoiceprint"
    
    output_name = f"invoiceprint-{platform_name}-{arch}"
    
    # PyInstaller arguments
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # Package as single file
        "--clean",             # Clean temp files
        "--noconfirm",         # No confirmation for overwrite
        "--name", output_name, # Output filename
        "main.py"              # Entry file
    ]
    
    # Windows specific: hide console window (uncomment if needed)
    # if platform_name == "windows":
    #     pyinstaller_args.insert(-1, "--noconsole")
    
    print("Building...")
    print(f"Command: {' '.join(pyinstaller_args)}")
    print("-" * 40)
    
    # Execute build
    result = subprocess.run(pyinstaller_args)
    
    if result.returncode != 0:
        print("Build failed!")
        return False
    
    # Check output file
    if platform_name == "windows":
        output_file = Path("dist") / f"{output_name}.exe"
    else:
        output_file = Path("dist") / output_name
    
    if output_file.exists():
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        print("-" * 40)
        print(f"Build successful!")
        print(f"Output file: {output_file}")
        print(f"File size: {file_size:.2f} MB")
        return True
    else:
        print("Build failed: output file not found")
        return False


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cross-platform build script")
    parser.add_argument(
        "--clean", "-c",
        action="store_true",
        help="Only clean build directories"
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Don't clean before build"
    )
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    if args.clean:
        clean_build()
        print("Clean completed!")
        return 0
    
    if not args.no_clean:
        clean_build()
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("Error: PyInstaller not installed")
        print("Run: uv pip install pyinstaller")
        print("Or: uv sync --extra dev")
        return 1
    
    success = build_executable()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
