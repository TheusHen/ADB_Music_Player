import os
import subprocess
import sys
import platform
import time
from typing import List, Optional, Tuple

def is_adb_installed() -> bool:
    """Check if ADB is installed and accessible in the system path."""
    try:
        subprocess.run(
            ["adb", "version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            check=True
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def install_adb() -> bool:
    """Install ADB based on the operating system."""
    system = platform.system()
    
    print("ADB not found. Installing ADB...")
    
    if system == "Windows":
        # For Windows, we'll use a simple approach to download platform-tools
        try:
            # Create a temporary directory
            os.makedirs("temp", exist_ok=True)
            
            # Download platform-tools zip
            print("Downloading Android platform-tools...")
            subprocess.run(
                ["powershell", "-Command", 
                 "Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile 'temp\\platform-tools.zip'"],
                check=True
            )
            
            # Extract the zip
            print("Extracting platform-tools...")
            subprocess.run(
                ["powershell", "-Command", 
                 "Expand-Archive -Path 'temp\\platform-tools.zip' -DestinationPath 'temp' -Force"],
                check=True
            )
            
            # Add to PATH temporarily for this session
            platform_tools_path = os.path.abspath(os.path.join("temp", "platform-tools"))
            os.environ["PATH"] = platform_tools_path + os.pathsep + os.environ["PATH"]
            
            print(f"ADB installed successfully. Added {platform_tools_path} to PATH for this session.")
            print("For permanent installation, add this path to your system's PATH environment variable.")
            
            return True
        except Exception as e:
            print(f"Error installing ADB: {e}")
            return False
    elif system == "Linux":
        try:
            print("Installing ADB via apt...")
            subprocess.run(
                ["sudo", "apt", "update"], 
                check=True
            )
            subprocess.run(
                ["sudo", "apt", "install", "-y", "adb"], 
                check=True
            )
            return True
        except Exception as e:
            print(f"Error installing ADB: {e}")
            return False
    elif system == "Darwin":  # macOS
        try:
            print("Installing ADB via Homebrew...")
            # Check if Homebrew is installed
            try:
                subprocess.run(
                    ["brew", "--version"], 
                    stdout=subprocess.PIPE, 
                    check=True
                )
            except:
                print("Homebrew not found. Installing Homebrew...")
                subprocess.run(
                    ["/bin/bash", "-c", 
                     "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"],
                    check=True
                )
            
            # Install ADB
            subprocess.run(
                ["brew", "install", "android-platform-tools"], 
                check=True
            )
            return True
        except Exception as e:
            print(f"Error installing ADB: {e}")
            return False
    else:
        print(f"Unsupported operating system: {system}")
        print("Please install ADB manually and add it to your PATH.")
        return False

def get_connected_devices() -> List[Tuple[str, str]]:
    """
    Get a list of connected Android devices.
    
    Returns:
        List of tuples containing (device_id, device_model)
    """
    devices = []
    
    try:
        # Get list of devices
        result = subprocess.run(
            ["adb", "devices"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            check=True
        )
        
        # Parse the output
        lines = result.stdout.strip().split('\n')
        if len(lines) <= 1:
            return []
        
        # Skip the first line (header)
        for line in lines[1:]:
            if not line.strip():
                continue
                
            parts = line.split('\t')
            if len(parts) >= 2 and parts[1] == 'device':
                device_id = parts[0].strip()
                
                # Get device model
                model_result = subprocess.run(
                    ["adb", "-s", device_id, "shell", "getprop", "ro.product.model"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True
                )
                model = model_result.stdout.strip() if model_result.returncode == 0 else "Unknown"
                
                devices.append((device_id, model))
    
    except Exception as e:
        print(f"Error getting connected devices: {e}")
    
    return devices

def select_device() -> Optional[str]:
    """
    Display a list of connected devices and let the user select one.
    
    Returns:
        The selected device ID or None if no device was selected
    """
    # Get connected devices
    devices = get_connected_devices()
    
    if not devices:
        print("No devices connected. Please connect an Android device and enable USB debugging.")
        return None
    
    # Display devices
    print("\nConnected devices:")
    for i, (device_id, model) in enumerate(devices, 1):
        print(f"{i}. {model} ({device_id})")
    
    # Let user select a device
    while True:
        try:
            choice = input("\nSelect a device (number) or 'q' to quit: ")
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(devices):
                return devices[index][0]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number or 'q'.")

def execute_adb_command(device_id: str, command: List[str]) -> str:
    """Execute an ADB command for the specified device."""
    try:
        result = subprocess.run(
            ["adb", "-s", device_id] + command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.SubprocessError as e:
        print(f"Error executing ADB command: {e}")
        return ""

# Music control functions
def play_pause(device_id: str) -> None:
    """Toggle play/pause on the device."""
    execute_adb_command(device_id, ["shell", "input", "keyevent", "KEYCODE_MEDIA_PLAY_PAUSE"])

def next_track(device_id: str) -> None:
    """Skip to the next track."""
    execute_adb_command(device_id, ["shell", "input", "keyevent", "KEYCODE_MEDIA_NEXT"])

def previous_track(device_id: str) -> None:
    """Go to the previous track."""
    execute_adb_command(device_id, ["shell", "input", "keyevent", "KEYCODE_MEDIA_PREVIOUS"])

def volume_up(device_id: str) -> None:
    """Increase the volume."""
    execute_adb_command(device_id, ["shell", "input", "keyevent", "KEYCODE_VOLUME_UP"])

def volume_down(device_id: str) -> None:
    """Decrease the volume."""
    execute_adb_command(device_id, ["shell", "input", "keyevent", "KEYCODE_VOLUME_DOWN"])

def get_current_track_info(device_id: str) -> dict:
    """
    Get information about the currently playing track.
    This is a simplified implementation and may not work on all devices/players.
    """
    try:
        # This is a simplified approach and might not work on all devices
        # A more robust solution would require a specific app or service on the device
        result = {}
        
        # Try to get the current audio session info
        dumpsys_audio = execute_adb_command(device_id, ["shell", "dumpsys", "audio"])
        
        # This is very basic and might not work reliably
        # In a real implementation, you might want to use a dedicated music player app's API
        if "state=started" in dumpsys_audio.lower():
            result["playing"] = True
        else:
            result["playing"] = False
            
        return result
    except Exception as e:
        print(f"Error getting track info: {e}")
        return {"playing": False}
