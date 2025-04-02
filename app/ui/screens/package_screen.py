"""
Package retrieval screen with QR scanner for SecureLocker application
"""

import tkinter as tk
from tkinter import ttk
import threading
import json
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime

from app.ui.screens.base_screen import BaseScreen
from app.utils.qr_scanner import QRScanner

class PackageScreen(BaseScreen):
    """Package screen with QR scanning functionality"""
    
    def _create_widgets(self):
        """Create the package screen widgets"""
        self.frame = ttk.Frame(self.parent)
        
        # Header with back button
        self._create_header_with_back("Package Retrieval")
        
        # QR Scanner area
        scanner_frame = ttk.Frame(self.frame, padding=10)
        scanner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Video feed frame with border for better visibility
        video_container = tk.Frame(
            scanner_frame, 
            bd=2, 
            relief=tk.GROOVE,
            bg=self.config.dark
        )
        video_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Video feed label
        self.video_frame = tk.Label(video_container, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scanning indicator (animated line)
        self.scanning_line = tk.Frame(video_container, bg=self.config.primary_color, height=3)
        
        # Scanner message
        self.scan_message = tk.Label(
            scanner_frame, 
            text="Please scan your QR code to retrieve your package",
            font=("Helvetica", 14)
        )
        self.scan_message.pack(pady=10)
        
        # Initialize scanner variables
        self.camera_active = False
        self.scanner = None
        
    def show(self, *args, **kwargs):
        """Show the package screen and start QR scanner"""
        super().show(*args, **kwargs)
        self._start_scanner()
        
    def hide(self):
        """Hide the package screen and stop QR scanner"""
        self._stop_scanner()
        super().hide()
    
    def _start_scanner(self):
        """Start the QR code scanner"""
        if not self.camera_active:
            self.camera_active = True
            
            # Initialize QR scanner
            self.scanner = QRScanner(
                on_qr_detected=self._on_qr_detected,
                on_error=self._on_scanner_error
            )
            
            # Start scanner in a separate thread
            self.scanner_thread = threading.Thread(target=self._scanner_loop)
            self.scanner_thread.daemon = True
            self.scanner_thread.start()
            
            # Start scanning line animation
            self._animate_scanning_line()
    
    def _stop_scanner(self):
        """Stop the QR code scanner"""
        if self.camera_active:
            self.camera_active = False
            if self.scanner:
                self.scanner.stop()
                self.scanner = None
            
            # Stop scanning line animation
            if hasattr(self, '_animation_id'):
                self.frame.after_cancel(self._animation_id)
    
    def _scanner_loop(self):
        """Camera processing loop to update UI with camera feed"""
        if not self.scanner.start():
            return
        
        while self.camera_active:
            # Get the current frame from scanner
            frame = self.scanner.get_frame()
            if frame is None:
                continue
            
            # Convert to PhotoImage for display
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update the video feed if it still exists
            # Since this runs in a thread, we need to check if video_frame still exists
            if hasattr(self, 'video_frame') and self.video_frame.winfo_exists():
                self.video_frame.imgtk = imgtk  # Keep a reference
                self.video_frame.configure(image=imgtk)
                
                # Process tkinter events
                try:
                    self.video_frame.update()
                except:
                    # If update fails, the window may have been closed
                    break
    
    def _animate_scanning_line(self):
        """Animate the scanning line to provide visual feedback"""
        if not hasattr(self, 'video_frame') or not self.video_frame.winfo_exists():
            return
            
        # Get video frame dimensions
        width = self.video_frame.winfo_width()
        height = self.video_frame.winfo_height()
        
        if width > 1 and height > 1:  # Make sure widget is visible
            # Position the scanning line
            if not self.scanning_line.winfo_ismapped():
                self.scanning_line.place(x=0, y=0, width=width)
            
            # Get current y position or start at top
            y = self.scanning_line.winfo_y()
            if y >= height:
                y = 0
            else:
                y += 2  # Move line down by 2 pixels
            
            # Update position
            self.scanning_line.place(x=0, y=y, width=width)
        
        # Schedule next animation frame
        self._animation_id = self.frame.after(30, self._animate_scanning_line)
    
    def _on_qr_detected(self, qr_data):
        """Handle detected QR code
        
        Args:
            qr_data (str): QR code data
        """
        # Stop scanner
        self._stop_scanner()
        
        try:
            # Parse QR code data
            qr_content = json.loads(qr_data)
            
            # Validate QR code
            if self._validate_qr_code(qr_content):
                # Show door open screen
                self.controller.show_screen('door_open', qr_content['doorId'])
            else:
                # Show error screen
                self.controller.show_screen('error', "QR code has expired or is invalid")
        except json.JSONDecodeError:
            # Invalid QR code format
            self.controller.show_screen('error', "Invalid QR code format")
        except Exception as e:
            # Other errors
            self.controller.show_screen('error', f"Error processing QR code: {str(e)}")
    
    def _validate_qr_code(self, qr_data):
        """Validate if QR code is valid and not expired
        
        Args:
            qr_data (dict): QR code data
            
        Returns:
            bool: True if QR code is valid
        """
        # Check if QR code has required fields
        if not all(key in qr_data for key in ['id', 'doorId', 'expiryDate']):
            return False
        
        # Check if QR code has expired
        try:
            expiry_date = datetime.fromisoformat(qr_data['expiryDate'].replace('Z', '+00:00'))
            now = datetime.now()
            return expiry_date > now
        except ValueError:
            return False
    
    def _on_scanner_error(self, error_message):
        """Handle scanner errors
        
        Args:
            error_message (str): Error message
        """
        self.camera_active = False
        self.scan_message.configure(
            text=f"Camera error: {error_message}. Please check your permissions.",
            fg=self.config.red
        )
        
        # Add a retry button
        retry_btn = tk.Button(
            self.frame,
            text="Retry",
            font=("Helvetica", 12),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=10,
            pady=5,
            bd=0,
            command=self._start_scanner
        )
        retry_btn.pack(pady=10)