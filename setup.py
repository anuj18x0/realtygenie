import subprocess
import sys
import os
import platform

def check_python_version():
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Error: Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    print("\nInstalling RealtyGenie Pro dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def check_gpu_support():
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"GPU acceleration available: {gpu_name}")
            return True
        else:
            print(" GPU acceleration not available (using CPU)")
            return False
    except ImportError:
        print("PyTorch not installed yet")
        return False

def verify_core_files():
    """Verify essential files exist"""
    essential_files = [
        "streamlit_app.py",
        "image_processor.py", 
        "property_descriptions.py",
        "social_media_automation.py",
        "requirements.txt"
    ]
    
    print("\n✅ Verifying core files...")
    missing_files = []
    
    for file in essential_files:
        if os.path.exists(file):
            print(f"   Found: {file}")
        else:
            print(f"   ❌ Missing: {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Warning: Missing {len(missing_files)} essential files!")
        return False
    return True

def check_setup_complete():
    print("\nSetup verification complete!")
    print("   All core files verified")
    print("   Dependencies installed")
    print("   Ready for web-based image uploads!")
    print("   No folders needed - everything runs in-memory")

def main():
    print("RealtyGenie Pro - Setup & Installation")
    print("=" * 50)
    
    if not check_python_version():
        sys.exit(1)
    
    if not verify_core_files():
        print("\nSetup cannot continue with missing core files!")
        sys.exit(1)
    
    if not install_requirements():
        sys.exit(1)
    
    check_gpu_support()
    
    check_setup_complete()
    
    print("\nSetup Complete!")
    print("\nTo start RealtyGenie Pro:")
    print("   python launch_app.py")
    print("   or")
    print("   streamlit run streamlit_app.py")
    print("\nOpen your browser to: http://localhost:8502")
    print("Upload property images directly through the web interface!")

if __name__ == "__main__":
    main()