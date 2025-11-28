import sys
import os

# Set up paths
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, application_path)

# Import and run GUI
from gui.tkinter_app import main

if __name__ == "__main__":
    main()