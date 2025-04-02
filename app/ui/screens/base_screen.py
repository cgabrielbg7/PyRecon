"""
Base screen class for SecureLocker application
All screens should inherit from this class
"""

import tkinter as tk
from tkinter import ttk

class BaseScreen:
    """Base class for all application screens"""
    
    def __init__(self, parent, controller):
        """Initialize the base screen
        
        Args:
            parent (tk.Widget): Parent widget for this screen
            controller (AppController): Main application controller
        """
        self.parent = parent
        self.controller = controller
        self.config = controller.config
        self.frame = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the screen widgets - to be implemented by subclasses"""
        self.frame = ttk.Frame(self.parent)
        # Subclasses should override this method to create their specific widgets
        pass
    
    def show(self, *args, **kwargs):
        """Show this screen
        
        Can be extended by subclasses to initialize or refresh content
        """
        if self.frame:
            self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Hide this screen"""
        if self.frame:
            self.frame.pack_forget()
    
    def _create_header_with_back(self, title, back_command=None):
        """Create a header with title and back button
        
        Args:
            title (str): Title to display in header
            back_command (callable, optional): Command for back button. 
                          Defaults to returning to home screen.
        
        Returns:
            ttk.Frame: The header frame
        """
        if back_command is None:
            back_command = lambda: self.controller.show_screen('home')
        
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, 
            text=title,
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        back_button = tk.Button(
            header_frame,
            text="Back",
            font=("Helvetica", 10),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=10,
            pady=5,
            bd=0,
            activebackground=self.config.secondary_color,
            activeforeground=self.config.white,
            command=back_command
        )
        back_button.pack(side=tk.RIGHT)
        
        return header_frame