import unittest
from unittest.mock import patch, MagicMock, call
import sys
import os
import random

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ascii_text import gen_art
from utils.adb import (
    is_adb_installed, install_adb, get_connected_devices, select_device,
    execute_adb_command, play_pause, next_track, previous_track,
    volume_up, volume_down, get_current_track_info
)
from helpers.soundbars import (
    clear_screen, generate_random_bars, draw_bars, draw_controls,
    visualize_music, start_visualization
)


class TestAsciiText(unittest.TestCase):
    """Test the ASCII text generation functionality."""
    
    @patch('pyfiglet.figlet_format')
    def test_gen_art(self, mock_figlet_format):
        """Test that gen_art calls pyfiglet.figlet_format with the correct arguments."""
        mock_figlet_format.return_value = "ASCII ART"
        
        result = gen_art("Test Text", "slant")
        
        mock_figlet_format.assert_called_once_with("Test Text", font="slant")
        self.assertEqual(result, "ASCII ART")


class TestADB(unittest.TestCase):
    """Test the ADB functionality."""
    
    @patch('subprocess.run')
    def test_is_adb_installed_true(self, mock_run):
        """Test is_adb_installed when ADB is installed."""
        mock_run.return_value = MagicMock(returncode=0)
        
        result = is_adb_installed()
        
        self.assertTrue(result)
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_is_adb_installed_false(self, mock_run):
        """Test is_adb_installed when ADB is not installed."""
        mock_run.side_effect = FileNotFoundError()
        
        result = is_adb_installed()
        
        self.assertFalse(result)
    
    @patch('utils.adb.execute_adb_command')
    def test_play_pause(self, mock_execute):
        """Test play_pause function."""
        play_pause("device123")
        
        mock_execute.assert_called_once_with(
            "device123", ["shell", "input", "keyevent", "KEYCODE_MEDIA_PLAY_PAUSE"]
        )
    
    @patch('utils.adb.execute_adb_command')
    def test_next_track(self, mock_execute):
        """Test next_track function."""
        next_track("device123")
        
        mock_execute.assert_called_once_with(
            "device123", ["shell", "input", "keyevent", "KEYCODE_MEDIA_NEXT"]
        )
    
    @patch('utils.adb.execute_adb_command')
    def test_previous_track(self, mock_execute):
        """Test previous_track function."""
        previous_track("device123")
        
        mock_execute.assert_called_once_with(
            "device123", ["shell", "input", "keyevent", "KEYCODE_MEDIA_PREVIOUS"]
        )
    
    @patch('utils.adb.execute_adb_command')
    def test_volume_up(self, mock_execute):
        """Test volume_up function."""
        volume_up("device123")
        
        mock_execute.assert_called_once_with(
            "device123", ["shell", "input", "keyevent", "KEYCODE_VOLUME_UP"]
        )
    
    @patch('utils.adb.execute_adb_command')
    def test_volume_down(self, mock_execute):
        """Test volume_down function."""
        volume_down("device123")
        
        mock_execute.assert_called_once_with(
            "device123", ["shell", "input", "keyevent", "KEYCODE_VOLUME_DOWN"]
        )
    
    @patch('utils.adb.execute_adb_command')
    def test_get_current_track_info_playing(self, mock_execute):
        """Test get_current_track_info when music is playing."""
        mock_execute.return_value = "state=started"
        
        result = get_current_track_info("device123")
        
        self.assertEqual(result, {"playing": True})
        mock_execute.assert_called_once()
    
    @patch('utils.adb.execute_adb_command')
    def test_get_current_track_info_not_playing(self, mock_execute):
        """Test get_current_track_info when music is not playing."""
        mock_execute.return_value = "state=stopped"
        
        result = get_current_track_info("device123")
        
        self.assertEqual(result, {"playing": False})
        mock_execute.assert_called_once()


class TestSoundbars(unittest.TestCase):
    """Test the soundbars visualization functionality."""
    
    @patch('random.randint')
    def test_generate_random_bars(self, mock_randint):
        """Test generate_random_bars function."""
        mock_randint.side_effect = [5, 3, 7, 2, 8]
        
        result = generate_random_bars(num_bars=5, max_height=10)
        
        self.assertEqual(result, [5, 3, 7, 2, 8])
        self.assertEqual(mock_randint.call_count, 5)
    
    @patch('builtins.print')
    def test_draw_bars(self, mock_print):
        """Test draw_bars function."""
        heights = [3, 1, 4, 2]
        
        draw_bars(heights, width=2)
        
        # Check that print was called the expected number of times
        # (max_height + 1 for the base line)
        self.assertEqual(mock_print.call_count, 5)
    
    @patch('builtins.print')
    def test_draw_controls(self, mock_print):
        """Test draw_controls function."""
        draw_controls()
        
        # Check that print was called to display controls
        self.assertEqual(mock_print.call_count, 4)
    
    @patch('helpers.soundbars.clear_screen')
    @patch('helpers.soundbars.get_current_track_info')
    @patch('helpers.soundbars.generate_random_bars')
    @patch('builtins.print')
    @patch('time.sleep')
    @patch('keyboard.on_press')
    @patch('keyboard.unhook_all')
    def test_visualize_music_playing(self, mock_unhook, mock_on_press, mock_sleep, 
                                    mock_print, mock_generate_bars, mock_get_track, mock_clear):
        """Test visualize_music when music is playing."""
        # Setup mocks
        mock_get_track.return_value = {"playing": True}
        mock_generate_bars.return_value = [5, 3, 7, 2, 8]
        
        # Make visualize_music run only once
        mock_sleep.side_effect = KeyboardInterrupt()
        
        # Call the function
        visualize_music("device123")
        
        # Verify the function behavior
        mock_clear.assert_called_once()
        mock_get_track.assert_called_once_with("device123")
        mock_generate_bars.assert_called_once()
        mock_on_press.assert_called_once()
        mock_unhook.assert_called_once()
    
    @patch('helpers.soundbars.clear_screen')
    @patch('helpers.soundbars.get_current_track_info')
    @patch('random.randint')
    @patch('builtins.print')
    @patch('time.sleep')
    @patch('keyboard.on_press')
    @patch('keyboard.unhook_all')
    def test_visualize_music_not_playing(self, mock_unhook, mock_on_press, mock_sleep, 
                                        mock_print, mock_randint, mock_get_track, mock_clear):
        """Test visualize_music when music is not playing."""
        # Setup mocks
        mock_get_track.return_value = {"playing": False}
        mock_randint.return_value = 2
        
        # Make visualize_music run only once
        mock_sleep.side_effect = KeyboardInterrupt()
        
        # Call the function
        visualize_music("device123")
        
        # Verify the function behavior
        mock_clear.assert_called_once()
        mock_get_track.assert_called_once_with("device123")
        self.assertTrue(mock_randint.called)
        mock_on_press.assert_called_once()
        mock_unhook.assert_called_once()


class TestKeyboardControls(unittest.TestCase):
    """Test the keyboard controls functionality."""
    
    @patch('helpers.soundbars.play_pause')
    def test_on_key_press_space(self, mock_play_pause):
        """Test on_key_press with space key."""
        # Extract the on_key_press function from visualize_music
        with patch('keyboard.on_press') as mock_on_press:
            # Start visualize_music but interrupt it immediately
            with patch('time.sleep', side_effect=KeyboardInterrupt()):
                try:
                    visualize_music("device123")
                except KeyboardInterrupt:
                    pass
            
            # Get the callback function registered with keyboard.on_press
            on_key_press = mock_on_press.call_args[0][0]
            
            # Create a mock event
            mock_event = MagicMock()
            mock_event.name = "space"
            
            # Call the callback with the mock event
            on_key_press(mock_event)
            
            # Verify play_pause was called
            mock_play_pause.assert_called_once_with("device123")
    
    @patch('helpers.soundbars.next_track')
    def test_on_key_press_right(self, mock_next_track):
        """Test on_key_press with right arrow key."""
        # Extract the on_key_press function from visualize_music
        with patch('keyboard.on_press') as mock_on_press:
            # Start visualize_music but interrupt it immediately
            with patch('time.sleep', side_effect=KeyboardInterrupt()):
                try:
                    visualize_music("device123")
                except KeyboardInterrupt:
                    pass
            
            # Get the callback function registered with keyboard.on_press
            on_key_press = mock_on_press.call_args[0][0]
            
            # Create a mock event
            mock_event = MagicMock()
            mock_event.name = "right"
            
            # Call the callback with the mock event
            on_key_press(mock_event)
            
            # Verify next_track was called
            mock_next_track.assert_called_once_with("device123")


class TestIntegration(unittest.TestCase):
    """Integration tests for the music player."""
    
    @patch('utils.adb.is_adb_installed', return_value=True)
    @patch('utils.adb.get_connected_devices')
    @patch('builtins.input', return_value='1')
    @patch('helpers.soundbars.visualize_music')
    def test_main_flow(self, mock_visualize, mock_input, mock_get_devices, mock_is_installed):
        """Test the main flow of the application."""
        from main import main
        
        # Setup mocks
        mock_get_devices.return_value = [("device123", "Test Phone")]
        
        # Run the main function
        main()
        
        # Verify the expected flow
        mock_is_installed.assert_called_once()
        mock_get_devices.assert_called_once()
        mock_visualize.assert_called_once_with("device123")


if __name__ == '__main__':
    unittest.main()