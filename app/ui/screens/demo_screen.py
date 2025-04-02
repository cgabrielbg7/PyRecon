"""
Demo/marketing screen for SecureLocker application
"""

import tkinter as tk
from tkinter import ttk

from app.ui.screens.base_screen import BaseScreen

class DemoScreen(BaseScreen):
    """Demo screen with marketing content"""
    
    def _create_widgets(self):
        """Create the demo screen widgets"""
        self.frame = ttk.Frame(self.parent)
        
        # Header with back button
        self._create_header_with_back("Marketing Demos")
        
        # Marketing content carousel
        carousel_frame = ttk.Frame(self.frame, padding=10)
        carousel_frame.pack(fill=tk.BOTH, expand=True)
        
        # We'll simulate the carousel with a notebook with tabs
        self.carousel = ttk.Notebook(carousel_frame)
        self.carousel.pack(fill=tk.BOTH, expand=True)
        
        # Create demo slides with different colors
        slide_info = [
            {
                "bg": self.config.blue, 
                "title": "Secure Package Delivery", 
                "text": "High-security lockers for all your delivery needs"
            },
            {
                "bg": self.config.green, 
                "title": "Easy Access System", 
                "text": "Simple QR code scanning for quick package retrieval"
            },
            {
                "bg": self.config.purple, 
                "title": "24/7 Availability", 
                "text": "Access your secure items anytime you need them"
            }
        ]
        
        for idx, info in enumerate(slide_info):
            self._create_slide(idx, info)
    
    def _create_slide(self, idx, info):
        """Create a slide for the carousel
        
        Args:
            idx (int): Slide index
            info (dict): Slide information including bg, title and text
        """
        slide = ttk.Frame(self.carousel)
        
        # Make the slide colored
        slide_content = tk.Frame(slide, bg=info["bg"], padx=40, pady=40)
        slide_content.pack(fill=tk.BOTH, expand=True)
        
        # Add content to slide
        title = tk.Label(
            slide_content, 
            text=info["title"],
            font=("Helvetica", 24, "bold"),
            fg=self.config.white,
            bg=info["bg"]
        )
        title.pack(pady=(0, 20))
        
        description = tk.Label(
            slide_content, 
            text=info["text"],
            font=("Helvetica", 16),
            fg=self.config.white,
            bg=info["bg"]
        )
        description.pack()
        
        self.carousel.add(slide, text=f"Slide {idx+1}")
    
    def show(self, *args, **kwargs):
        """Show the demo screen and start carousel rotation"""
        super().show(*args, **kwargs)
        self._rotate_carousel()
    
    def hide(self):
        """Hide the demo screen and stop carousel rotation"""
        # Cancel scheduled rotation if it exists
        if hasattr(self, '_rotation_id'):
            self.frame.after_cancel(self._rotation_id)
            delattr(self, '_rotation_id')
        super().hide()
    
    def _rotate_carousel(self):
        """Automatically rotate the carousel tabs"""
        if hasattr(self, 'carousel'):
            current = self.carousel.index(self.carousel.select())
            next_tab = (current + 1) % self.carousel.index('end')
            self.carousel.select(next_tab)
            
            # Schedule next rotation
            self._rotation_id = self.frame.after(5000, self._rotate_carousel)