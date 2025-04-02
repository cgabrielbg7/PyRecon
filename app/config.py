"""
Configuration module for SecureLocker application
"""

class AppConfig:
    """Configuration class containing app settings"""
    
    def __init__(self):
        """Initialize configuration with default values"""
        # App colors - matching the original HTML theme
        self.primary_color = "#5D5CDE"
        self.secondary_color = "#4B4AC6"
        self.white = "#FFFFFF"
        self.dark = "#181818"
        self.light_gray = "#F3F4F6"
        self.gray = "#6B7280"
        self.green = "#10B981"
        self.blue = "#3B82F6"
        self.purple = "#8B5CF6"
        self.red = "#EF4444"
        
        # Check for dark mode preference
        # This is a simplified approach - in real application you'd check system preferences
        self.dark_mode = False
        
        # App name and version
        self.app_name = "SecureLocker"
        self.version = "1.0.0"
        
        # Default QR code settings
        self.default_expiry_days = 7
        
        # Security settings
        self.qr_code_length = 8  # Length of generated QR code IDs