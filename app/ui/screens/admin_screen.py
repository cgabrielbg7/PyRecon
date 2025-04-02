"""
Admin screen for SecureLocker application
Allows generation of QR codes
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import qrcode
import string
import random
import pyperclip
import webbrowser
from datetime import datetime, timedelta
from PIL import Image, ImageTk

from app.ui.screens.base_screen import BaseScreen
from app.utils.qr_generator import QRGenerator

class AdminScreen(BaseScreen):
    """Admin screen for QR code generation"""
    
    def _create_widgets(self):
        """Create the admin screen widgets"""
        self.frame = ttk.Frame(self.parent)
        
        # Header with back button
        self._create_header_with_back("Admin Panel")
        
        # Two column layout
        columns_frame = ttk.Frame(self.frame)
        columns_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # QR Generation Form (left column)
        self._create_form_panel(columns_frame)
        
        # QR Code Display (right column)
        self._create_display_panel(columns_frame)
        
        # Store QR data
        self.current_qr_data = None
        self.qr_generator = QRGenerator()
    
    def _create_form_panel(self, parent):
        """Create the QR code generation form panel
        
        Args:
            parent (tk.Widget): Parent widget
        """
        form_frame = ttk.Frame(parent, padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        form_card = tk.Frame(form_frame, bd=1, relief=tk.SOLID)
        form_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        form_title = tk.Label(
            form_card, 
            text="Generate QR Code",
            font=("Helvetica", 16, "bold"),
            pady=10
        )
        form_title.pack()
        
        # Form fields
        form_fields = ttk.Frame(form_card, padding=20)
        form_fields.pack(fill=tk.BOTH, expand=True)
        
        # Door selection
        door_label = tk.Label(
            form_fields, 
            text="Select Door",
            font=("Helvetica", 12)
        )
        door_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.door_var = tk.StringVar()
        door_select = ttk.Combobox(
            form_fields, 
            textvariable=self.door_var,
            state="readonly",
            values=["1", "2", "3", "4"]
        )
        door_select.pack(fill=tk.X, pady=(0, 15))
        
        # Expiry date
        expiry_label = tk.Label(
            form_fields, 
            text="Expiry Date",
            font=("Helvetica", 12)
        )
        expiry_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Set default expiry date to 7 days from now
        self.expiry_var = tk.StringVar()
        default_expiry = (datetime.now() + timedelta(days=self.config.default_expiry_days)).strftime('%Y-%m-%d')
        self.expiry_var.set(default_expiry)
        
        expiry_entry = ttk.Entry(form_fields, textvariable=self.expiry_var)
        expiry_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Help text
        help_text = tk.Label(
            form_fields, 
            text="Format: YYYY-MM-DD (e.g. 2023-12-31)",
            font=("Helvetica", 9),
            fg=self.config.gray
        )
        help_text.pack(anchor=tk.W, pady=(0, 15))
        
        # Generate button
        generate_btn = tk.Button(
            form_fields,
            text="Generate QR Code",
            font=("Helvetica", 12),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=10,
            pady=8,
            bd=0,
            activebackground=self.config.secondary_color,
            activeforeground=self.config.white,
            command=self._generate_qr_code
        )
        generate_btn.pack(fill=tk.X, pady=(10, 0))
    
    def _create_display_panel(self, parent):
        """Create the QR code display panel
        
        Args:
            parent (tk.Widget): Parent widget
        """
        display_frame = ttk.Frame(parent, padding=10)
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        display_card = tk.Frame(display_frame, bd=1, relief=tk.SOLID)
        display_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        display_title = tk.Label(
            display_card, 
            text="QR Code",
            font=("Helvetica", 16, "bold"),
            pady=10
        )
        display_title.pack()
        
        # QR code display container
        qr_container = ttk.Frame(display_card, padding=20)
        qr_container.pack(fill=tk.BOTH, expand=True)
        
        # QR code image label
        self.qr_display = tk.Label(
            qr_container, 
            text="QR code will appear here",
            font=("Helvetica", 12),
            fg=self.config.gray,
            width=300, 
            height=300
        )
        self.qr_display.pack(pady=(0, 10))
        
        # QR code ID display
        self.qr_id_label = tk.Label(
            qr_container, 
            text="",
            font=("Helvetica", 12, "bold")
        )
        self.qr_id_label.pack(pady=(0, 15))
        
        # Action buttons frame
        action_buttons = ttk.Frame(qr_container)
        action_buttons.pack()
        
        # Copy ID button
        self.copy_btn = tk.Button(
            action_buttons,
            text="Copy ID",
            font=("Helvetica", 10),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=10,
            pady=5,
            bd=0,
            state=tk.DISABLED,
            command=self._copy_qr_id
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Email button
        self.email_btn = tk.Button(
            action_buttons,
            text="Email",
            font=("Helvetica", 10),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=10,
            pady=5,
            bd=0,
            state=tk.DISABLED,
            command=self._email_qr
        )
        self.email_btn.pack(side=tk.LEFT, padx=5)
        
        # Teams button
        self.teams_btn = tk.Button(
            action_buttons,
            text="Teams",
            font=("Helvetica", 10),
            bg=self.config.primary_color,
            fg=self.config.white,
            padx=10,
            pady=5,
            bd=0,
            state=tk.DISABLED,
            command=self._teams_qr
        )
        self.teams_btn.pack(side=tk.LEFT, padx=5)
    
    def _generate_qr_code(self):
        """Generate QR code from form data"""
        door_id = self.door_var.get()
        expiry_date = self.expiry_var.get()
        
        if not door_id or not expiry_date:
            messagebox.showerror("Error", "Please fill out all fields")
            return
        
        try:
            # Validate date format
            datetime.strptime(expiry_date, '%Y-%m-%d')
            
            # Generate QR code using QRGenerator
            self.current_qr_data = self.qr_generator.generate_qr_data(door_id, expiry_date)
            qr_id = self.current_qr_data['id']
            
            # Generate QR code image
            qr_image = self.qr_generator.generate_qr_image(self.current_qr_data)
            
            # Resize for display
            qr_image = qr_image.resize((250, 250))
            self.qr_photoimage = ImageTk.PhotoImage(qr_image)
            
            # Update QR display
            self.qr_display.configure(image=self.qr_photoimage, text="")
            self.qr_id_label.configure(text=f"ID: {qr_id}")
            
            # Enable buttons
            self.copy_btn.configure(state=tk.NORMAL)
            self.email_btn.configure(state=tk.NORMAL)
            self.teams_btn.configure(state=tk.NORMAL)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def _copy_qr_id(self):
        """Copy QR ID to clipboard"""
        if self.current_qr_data:
            pyperclip.copy(self.current_qr_data['id'])
            self._show_copy_success(self.copy_btn)
    
    def _email_qr(self):
        """Open email client with QR code info"""
        if self.current_qr_data:
            qr_id = self.current_qr_data['id']
            door_id = self.current_qr_data['doorId']
            expiry_date = datetime.strptime(
                self.current_qr_data['expiryDate'], 
                '%Y-%m-%d'
            ).strftime('%m/%d/%Y')
            
            email_subject = f"Your {self.config.app_name} Package QR Code"
            email_body = (
                f"Your {self.config.app_name} QR code ID is: {qr_id}\n\n"
                f"Door: {door_id}\n"
                f"Expires: {expiry_date}\n\n"
                f"Please use this code at our {self.config.app_name} kiosk to retrieve your package."
            )
            
            # Open default email client
            url = f"mailto:?subject={email_subject}&body={email_body}"
            webbrowser.open(url)
    
    def _teams_qr(self):
        """Copy QR details for Teams message"""
        if self.current_qr_data:
            qr_id = self.current_qr_data['id']
            door_id = self.current_qr_data['doorId']
            expiry_date = datetime.strptime(
                self.current_qr_data['expiryDate'], 
                '%Y-%m-%d'
            ).strftime('%m/%d/%Y')
            
            # Create a message for Teams
            message = (
                f"Your {self.config.app_name} QR code ID is: {qr_id}\n\n"
                f"Door: {door_id}\n"
                f"Expires: {expiry_date}\n\n"
                f"Please use this code at our {self.config.app_name} kiosk to retrieve your package."
            )
            
            # Copy to clipboard
            pyperclip.copy(message)
            self._show_copy_success(self.teams_btn, "Copied for Teams!")
    
    def _show_copy_success(self, button, message="Copied!"):
        """Show a temporary success message on button
        
        Args:
            button (tk.Button): Button to show message on
            message (str): Message to display
        """
        original_text = button.cget("text")
        button.config(text=message)
        
        # Reset after 2 seconds
        self.frame.after(2000, lambda: button.config(text=original_text))