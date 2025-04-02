"""
QR code scanner utilities for SecureLocker application
"""

import cv2
from pyzbar.pyzbar import decode
import numpy as np

class QRScanner:
    """Class for handling QR code scanning functionality"""
    
    def __init__(self, on_qr_detected=None, on_error=None, camera_id=0):
        """Initialize the QR scanner
        
        Args:
            on_qr_detected (callable, optional): Callback for detected QR code.
            on_error (callable, optional): Callback for scanner errors.
            camera_id (int, optional): Camera device ID. Defaults to 0.
        """
        self.camera_id = camera_id
        self.on_qr_detected = on_qr_detected
        self.on_error = on_error
        self.cap = None
        self.running = False
        self.last_frame = None
    
    def start(self):
        """Start the camera capture
        
        Returns:
            bool: True if camera started successfully, False otherwise
        """
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                if self.on_error:
                    self.on_error("Could not open camera")
                return False
            
            self.running = True
            return True
            
        except Exception as e:
            if self.on_error:
                self.on_error(str(e))
            return False
    
    def stop(self):
        """Stop the camera capture"""
        self.running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def get_frame(self):
        """Get the current frame from camera and scan for QR codes
        
        Returns:
            numpy.ndarray: Current frame (or None if error)
        """
        if not self.running or self.cap is None:
            return None
        
        try:
            ret, frame = self.cap.read()
            if not ret:
                if self.on_error:
                    self.on_error("Failed to read from camera")
                return None
            
            # Convert to RGB for display (Tkinter requires RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Save as last frame
            self.last_frame = rgb_frame
            
            # Scan for QR codes
            self._scan_qr_codes(rgb_frame)
            
            return rgb_frame
            
        except Exception as e:
            if self.on_error:
                self.on_error(f"Camera error: {str(e)}")
            return None
    
    def _scan_qr_codes(self, frame):
        """Scan frame for QR codes
        
        Args:
            frame (numpy.ndarray): Frame to scan
        """
        if not self.running:
            return
        
        try:
            # Scan for QR codes
            decoded_objects = decode(frame)
            
            for obj in decoded_objects:
                # Draw rectangle around QR code
                points = obj.polygon
                if len(points) > 4:
                    hull = cv2.convexHull(np.array([point for point in points]))
                    cv2.polylines(frame, [hull], True, (0, 255, 0), 3)
                else:
                    pts = np.array([point for point in points], np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
                
                # Get data
                qr_data = obj.data.decode('utf-8')
                
                # Stop scanning and call callback
                if self.on_qr_detected:
                    self.on_qr_detected(qr_data)
                    break
                    
        except Exception as e:
            # Don't call error handler here to avoid excessive error messages
            # during scanning. Just skip this frame.
            pass