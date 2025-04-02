"""
QR code generator utilities for SecureLocker application
"""

import json
import qrcode
import string
import random
import tempfile
import os
from datetime import datetime
from PIL import Image

class QRGenerator:
    """Class for generating QR codes for package lockers"""
    
    def __init__(self):
        """Initialize the QR code generator"""
        # Character set for generating unique IDs
        self.chars = string.ascii_uppercase + string.digits
        
        # Default QR code settings
        self.qr_code_length = 8  # Length of generated QR code IDs
    
    def generate_unique_id(self, length=None):
        """Generate a unique ID for QR codes
        
        Args:
            length (int, optional): Length of the ID. Defaults to self.qr_code_length.
            
        Returns:
            str: Generated unique ID
        """
        if length is None:
            length = self.qr_code_length
            
        return ''.join(random.choices(self.chars, k=length))
    
    def generate_qr_data(self, door_id, expiry_date):
        """Generate QR code data
        
        Args:
            door_id (str): Door ID for the locker
            expiry_date (str): Expiry date in YYYY-MM-DD format
            
        Returns:
            dict: QR code data
        """
        # Generate a unique ID
        qr_id = self.generate_unique_id()
        
        # Create QR data
        qr_data = {
            'id': qr_id,
            'doorId': door_id,
            'expiryDate': expiry_date,
            'created': datetime.now().isoformat()
        }
        
        return qr_data
    
    def generate_qr_image(self, qr_data, box_size=10, border=4):
        """Generate QR code image from data
        
        Args:
            qr_data (dict): QR code data
            box_size (int, optional): Size of each box in QR code. Defaults to 10.
            border (int, optional): Border size. Defaults to 4.
            
        Returns:
            Image: PIL Image object with QR code
        """
        # Convert data to JSON
        qr_json = json.dumps(qr_data)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        qr.add_data(qr_json)
        qr.make(fit=True)
        
        # Create image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        return qr_image
    
    def save_qr_image(self, qr_data, filename=None):
        """Generate and save QR code image to file
        
        Args:
            qr_data (dict): QR code data
            filename (str, optional): Filename to save QR code. 
                                    If None, a temp file will be created.
            
        Returns:
            str: Path to saved QR code image
        """
        qr_image = self.generate_qr_image(qr_data)
        
        # Create filename if not provided
        if filename is None:
            qr_id = qr_data['id']
            # Create a temporary file
            fd, filename = tempfile.mkstemp(suffix='.png', prefix=f'qr_{qr_id}_')
            os.close(fd)  # Close the file descriptor
        
        # Save image
        qr_image.save(filename)
        
        return filename