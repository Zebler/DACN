import sys
import os

# Add project to path
sys.path.insert(0, os.path.abspath('.'))

from gui.tkinter_app import main

if __name__ == "__main__":
    print("Starting Personal Schedule Assistant...")
    main()