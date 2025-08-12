import unittest
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the test modules
from test_music_player import (
    TestAsciiText,
    TestADB,
    TestSoundbars,
    TestKeyboardControls,
    TestIntegration
)

if __name__ == '__main__':
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases to the suite
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestAsciiText))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestADB))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestSoundbars))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestKeyboardControls))
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestIntegration))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\nTest Summary:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Exit with appropriate code
    sys.exit(len(result.failures) + len(result.errors))