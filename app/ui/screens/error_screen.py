"""
Error screen for SecureLocker application
"""

import tkinter as tk
from tkinter import ttk

from app.ui.screens.base_screen import BaseScreen

class ErrorScreen(BaseScreen):
    """Error screen"""
    
    def _create_widgets(self):
        """Create the error screen widgets"""
        self.frame = ttk.Frame(self.parent)
        
        # Center content
        content_frame = ttk.Frame(self.frame)
        
        # Error icon - using emoji as placeholder
        # In a real app, use a proper error icon
        self.icon_label = tk.Label(
            content_frame, 
            text="⚠️",  
            font=("Helvetica", 72), 
            fg="red"
        )
        self.icon_label.pack(pady=(0, 20))
        
        # Error title
        self.title_label = tk.Label(
            content_frame, 
            text="Invalid QR Code",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=(0, 10))
        
        # Error message
        self.error_label = tk.Label(
            content_frame, 
            text="An error occurred",
            font=("Helvetica", 16)
        )
        self.error_label.pack(pady=(0, 20))
        
        # Try again button
        retry_button = tk.Button(
            content_frame,
            text="Try Again",
            font=("Helvetica", 14),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=20,
            pady=10,
            bd=0,
            activebackground=self.config.secondary_color,
            activeforeground=self.config.white,
            command=lambda: self.controller.show_screen('package')
        )
        retry_button.pack()
        
        # Place content frame in center
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def show(self, error_message=None, *args, **kwargs):
        """Show the error screen
        
        Args:
            error_message (str, optional): Error message to display. Defaults to None.
        """
        super().show(*args, **kwargs)
        
        # Update error message if provided
        if error_message:
            self.error_label.config(text=error_message)