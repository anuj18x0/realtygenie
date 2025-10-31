import subprocess
import sys
import os
import time

def launch_ultimate_app():

    if not os.path.exists("streamlit_app.py"):
        print(" Ultimate app file not found!")
        print("Please ensure streamlit_app.py is in the current directory.")
        return False
    
    try:
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "dark"
        ]
        
        process = subprocess.Popen(cmd)
        
        time.sleep(3)
        
        process.wait()
        
    except subprocess.CalledProcessError as e:
        print(f" Failed to launch app: {e}")
        return False
    except KeyboardInterrupt:
        print("\\n👋 RealtyGenie Ultimate stopped by user")
        process.terminate()
        return True
    
    return True

if __name__ == "__main__":
    success = launch_ultimate_app()
    if not success:    
        print("\\There was an issue launching the application.")
        print("Please check the error messages above and try again.")