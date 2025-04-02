"""
Door open success screen for SecureLocker application
"""

import tkinter as tk
from tkinter import ttk

from app.ui.screens.base_screen import BaseScreen

class DoorOpenScreen(BaseScreen):
    """Door open success screen"""
    
    def _create_widgets(self):
        """Create the door open screen widgets"""
        self.frame = ttk.Frame(self.parent)
        
        # Center content
        content_frame = ttk.Frame(self.frame)
        
        # Success icon - using emoji as placeholder
        # In a real app, use a proper check mark icon
        self.icon_label = tk.Label(
            content_frame, 
            text="✅",  
            font=("Helvetica", 72), 
            fg="green"
        )
        self.icon_label.pack(pady=(0, 20))
        
        # Success message
        self.message_label = tk.Label(
            content_frame, 
            text="Door is Open!",
            font=("Helvetica", 24, "bold")
        )
        self.message_label.pack(pady=(0, 10))
        
        # Instruction
        instruction_label = tk.Label(
            content_frame, 
            text="Please collect your package",
            font=("Helvetica", 16)
        )
        instruction_label.pack(pady=(0, 20))
        
        # Done button
        done_button = tk.Button(
            content_frame,
            text="Done",
            font=("Helvetica", 14),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=20,
            pady=10,
            bd=0,
            activebackground=self.config.secondary_color,
            activeforeground=self.config.white,
            command=lambda: self.controller.show_screen('home')
        )
        done_button.pack()
        
        # Place content frame in center
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def show(self, door_id=None, *args, **kwargs):
        """Show the door open screen
        
        Args:
            door_id (str, optional): Door ID to display. Defaults to None.
        """
        super().show(*args, **kwargs)
        
        # Update message with door ID if provided
        if door_id:
            self.message_label.config(text=f"Door {door_id} is Open!")