#!/usr/bin/env python3
"""
SecureLocker Application
Main entry point for the application
"""

import tkinter as tk
from app.config import AppConfig
from app.ui.app_controller import AppController

def main():
    """Main function to start the application"""
    # Create the root window
    root = tk.Tk()
    root.title("SecureLocker")
    root.geometry("800x600")
    root.minsize(800, 600)
    
    # Create app config
    config = AppConfig()
    
    # Initialize the app controller
    app = AppController(root, config)
    
    # Start the app
    root.mainloop()

if __name__ == "__main__":
    main()