"""
Main controller for the SecureLocker application.
Manages screens and user interface flow.
"""

import tkinter as tk
from tkinter import ttk

from app.ui.screens.home_screen import HomeScreen
from app.ui.screens.admin_screen import AdminScreen
from app.ui.screens.package_screen import PackageScreen
from app.ui.screens.demo_screen import DemoScreen
from app.ui.screens.door_open_screen import DoorOpenScreen
from app.ui.screens.error_screen import ErrorScreen

class AppController:
    """Main application controller class"""
    
    def __init__(self, root, config):
        """Initialize the application controller
        
        Args:
            root (tk.Tk): The root Tkinter window
            config (AppConfig): Application configuration
        """
        self.root = root
        self.config = config
        self.current_screen = None
        
        # Create styles for the application
        self._setup_styles()
        
        # Create the application structure
        self._create_app_structure()
        
        # Initialize screens
        self.screens = {
            'home': HomeScreen(self.content_container, self),
            'admin': AdminScreen(self.content_container, self),
            'package': PackageScreen(self.content_container, self),
            'demo': DemoScreen(self.content_container, self),
            'door_open': DoorOpenScreen(self.content_container, self),
            'error': ErrorScreen(self.content_container, self)
        }
        
        # Start with home screen
        self.show_screen('home')
    
    def _setup_styles(self):
        """Set up TTK styles for the application"""
        self.style = ttk.Style()
        
        # Configure frame style
        self.style.configure(
            "TFrame", 
            background=self.config.white if not self.config.dark_mode else self.config.dark
        )
        
        # Configure button styles
        self.style.configure(
            "Primary.TButton", 
            background=self.config.primary_color, 
            foreground=self.config.white, 
            padding=10, 
            font=("Helvetica", 12, "bold")
        )
        
        self.style.map(
            "Primary.TButton",
            background=[("active", self.config.secondary_color)],
            foreground=[("active", self.config.white)]
        )
    
    def _create_app_structure(self):
        """Create the main application structure"""
        # Create header
        self._create_header()
        
        # Create container for content frames
        self.content_container = ttk.Frame(self.root)
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create footer
        self._create_footer()
    
    def _create_header(self):
        """Create the header with logo and admin button"""
        header_frame = tk.Frame(
            self.root, 
            bg=self.config.primary_color, 
            padx=15, 
            pady=10
        )
        header_frame.pack(fill=tk.X)
        
        # Logo/Title
        logo_label = tk.Label(
            header_frame, 
            text=self.config.app_name, 
            font=("Helvetica", 18, "bold"), 
            fg=self.config.white, 
            bg=self.config.primary_color
        )
        logo_label.pack(side=tk.LEFT)
        
        # Admin button
        admin_btn = tk.Button(
            header_frame, 
            text="Admin", 
            font=("Helvetica", 10), 
            bg=self.config.primary_color, 
            fg=self.config.white,
            bd=1,
            padx=10, 
            pady=5,
            activebackground=self.config.secondary_color,
            activeforeground=self.config.white,
            command=lambda: self.show_screen('admin')
        )
        admin_btn.pack(side=tk.RIGHT)
    
    def _create_footer(self):
        """Create the footer with copyright information"""
        bg_color = self.config.light_gray if not self.config.dark_mode else "#1F2937"
        
        footer_frame = tk.Frame(
            self.root, 
            bg=bg_color, 
            padx=15, 
            pady=10
        )
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        copyright_label = tk.Label(
            footer_frame, 
            text=f"© 2023 {self.config.app_name}. All rights reserved.", 
            font=("Helvetica", 10), 
            fg=self.config.gray, 
            bg=bg_color
        )
        copyright_label.pack()
    
    def show_screen(self, screen_name, *args, **kwargs):
        """Show a specific screen
        
        Args:
            screen_name (str): Name of the screen to show
            *args, **kwargs: Arguments to pass to the screen's setup method
        """
        # Hide current screen if exists
        if self.current_screen:
            self.current_screen.hide()
        
        # Show the new screen
        if screen_name in self.screens:
            self.screens[screen_name].show(*args, **kwargs)
            self.current_screen = self.screens[screen_name]
        else:
            raise ValueError(f"Screen '{screen_name}' does not exist")