"""
Home screen for SecureLocker application
"""

import tkinter as tk
from tkinter import ttk

from app.ui.screens.base_screen import BaseScreen

class HomeScreen(BaseScreen):
    """Home screen with main options"""
    
    def _create_widgets(self):
        """Create the home screen widgets"""
        self.frame = ttk.Frame(self.parent)
        
        # Welcome title
        welcome_label = tk.Label(
            self.frame, 
            text=f"Welcome to {self.config.app_name}",
            font=("Helvetica", 24, "bold"),
            pady=30
        )
        welcome_label.pack()
        
        # Buttons container
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(expand=True)
        
        # Create the main options buttons
        self._create_option_button(
            buttons_frame, 
            "See Demos", 
            "🎬", 
            lambda: self.controller.show_screen('demo')
        )
        
        self._create_option_button(
            buttons_frame, 
            "I Have a Package", 
            "📦", 
            lambda: self.controller.show_screen('package')
        )
    
    def _create_option_button(self, parent, text, icon_text, command):
        """Create a styled option button with icon
        
        Args:
            parent (tk.Widget): Parent widget
            text (str): Button text
            icon_text (str): Icon text (emoji or symbol)
            command (callable): Button command
            
        Returns:
            ttk.Frame: Button frame
        """
        btn_frame = ttk.Frame(parent, padding=10)
        btn_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Use text as icon placeholder (in a real app, you'd use actual icons)
        icon_label = tk.Label(
            btn_frame, 
            text=icon_text,
            font=("Helvetica", 36),
            fg=self.config.primary_color
        )
        icon_label.pack(pady=(0, 10))
        
        button = tk.Button(
            btn_frame,
            text=text,
            font=("Helvetica", 14, "bold"),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=20,
            pady=15,
            bd=0,
            activebackground=self.config.secondary_color,
            activeforeground=self.config.white,
            command=command
        )
        button.pack(fill=tk.X, ipady=10)
        
        return btn_frame