from utils.ascii_text import gen_art
from utils.adb import select_device, is_adb_installed, install_adb
from helpers.soundbars import start_visualization

def main():
    """Main entry point for the ADB Music Player application."""
    # Display welcome message
    print(gen_art(text="ADB_Music", font="slant"))
    print("By: TheusHen")
    print("\nWelcome to ADB Music Player!")
    print("This application allows you to control music playback on your Android device.")

    # Check if ADB is installed
    if not is_adb_installed():
        print("\nADB is not installed. Installing...")
        if not install_adb():
            print("Failed to install ADB. Please install it manually.")
            return

    # Select a device
    print("\nLooking for connected devices...")
    device_id = select_device()

    if not device_id:
        print("No device selected. Exiting.")
        return

    # Start music visualization
    print(f"\nStarting music visualization for device: {device_id}")
    print("Please ensure music is playing on your device for the best experience.")
    print("Use keyboard controls to interact with the player.")

    # Give the user a moment to read the instructions
    import time
    time.sleep(2)

    # Start the visualization
    start_visualization(device_id)


if __name__ == "__main__":
    main()
