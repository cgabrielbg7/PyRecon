# PyRecon

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/secure-locker.git
   cd secure-locker
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python main.py
   ```

## Usage

### Home Screen
The home screen provides access to the main functions:
- **See Demos**: View marketing demo content
- **I Have a Package**: Scan QR code to retrieve packages
- **Admin** (top-right button): Access administrative functions

### Admin Panel
Generate QR codes for locker access:
1. Select a door number
2. Set an expiry date
3. Click "Generate QR Code"
4. Share the generated QR code via:
   - Copy ID: Copies the QR code ID to clipboard
   - Email: Opens default email client with QR code details
   - Teams: Copies QR code details for Microsoft Teams

### Package Retrieval
1. Navigate to "I Have a Package"
2. Allow camera access when prompted
3. Scan the QR code
4. If valid, the appropriate locker door will open
5. If invalid or expired, an error will be displayed

## Requirements

- Python 3.7+
- Webcam for QR code scanning
- Dependencies listed in requirements.txt

## Implementation Details

### Key Components

- **AppController**: Manages screen switching and application flow
- **BaseScreen**: Parent class for all screens with common functionality
- **QRGenerator**: Utility for generating secure QR codes
- **QRScanner**: Handles camera access and QR code detection

### Security Features

- QR codes include expiry dates to limit access time
- Unique 8-character alphanumeric IDs for each QR code
- JSON-based QR code data with validation

## Development

### Adding a New Screen

1. Create a new screen class that inherits from `BaseScreen`
2. Implement the `_create_widgets` method
3. Register the screen in `app_controller.py`
4. Add any navigation methods needed

Example:
```python
from app.ui.screens.base_screen import BaseScreen

class MyNewScreen(BaseScreen):
    def _create_widgets(self):
        self.frame = ttk.Frame(self.parent)
        # Add your widgets here...
```

### Customization

The application appearance can be customized by modifying the color settings in `config.py`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# SecureLocker Python Application

A Python-based application for secure locker kiosks with QR code generation and scanning capabilities. This application is a desktop version of a web-based kiosk system implemented using Tkinter.

## Features

- Home screen with navigation options
- Admin panel for generating QR codes for locker access
- QR code generation for specific locker doors
- QR code scanning for package retrieval
- Door opening success screen
- Error handling and notifications
- Marketing demo carousel

## Project Structure

```
secure-locker/
├── main.py               # Main entry point
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── app/                  # Application package
    ├── __init__.py       # Package initialization
    ├── config.py         # Application configuration
    ├── ui/               # User interface components
    │   ├── __init__.py
    │   ├── app_controller.py  # Main app controller
    │   └── screens/           # Application screens
    │       ├── __init__.py
    │       ├── base_screen.py       # Base screen class
    │       ├── home_screen.py       # Home screen
    │       ├── admin_screen.py      # Admin screen for QR generation
    │       ├── package_screen.py    # Package retrieval with QR scanner
    │       ├── demo_screen.py       # Marketing demos
    │       ├── door_open_screen.py  # Door open success screen
    │       └── error_screen.py      # Error display screen
    └── utils/            # Utility modules
        ├── __init__.py
        ├── qr_generator.py  # QR code generation utilities
        └── qr_scanner.py    # QR code scanning utilities