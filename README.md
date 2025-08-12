# ADB_Music_Player
Simple ASCII music player for Android

## Description
ADB_Music_Player is a Python application that allows you to control music playback on your Android device from your computer. It displays a colorful ASCII visualization of the music that's playing and provides keyboard controls for basic playback functions.

## Features
- Automatic ADB installation if not already installed
- Device selection from connected Android devices
- Colorful ASCII visualization of music playback
- Keyboard controls for:
  - Play/Pause (Space)
  - Next track (Right arrow)
  - Previous track (Left arrow)
  - Volume up (Up arrow)
  - Volume down (Down arrow)
  - Quit (Q)

## Requirements
- Python 3.6 or higher
- Android device with USB debugging enabled
- USB connection to your Android device

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/TheusHen/ADB_Music_Player.git
   cd ADB_Music_Player
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Connect your Android device to your computer via USB
2. Enable USB debugging on your device
3. Run the application:
   ```
   python main.py
   ```
4. Select your device from the list
5. Use the keyboard controls to interact with the music player

## Notes
- If ADB is not installed, the application will attempt to install it automatically
- For the best experience, start playing music on your device before running the application
- The visualization is based on random values and does not actually analyze the audio

## Testing
The application includes a comprehensive test suite that tests all the main functionality using mocked data. This allows the tests to run without requiring an actual Android device connection.

### Running the Tests
To run the tests, you can use the provided script:
```
python tests/run_tests.py
```

Or you can use pytest directly:
```
pytest tests/test_music_player.py -v
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.