# Dropship Automator

## Overview
The Dropship Automator is a production-ready application designed to streamline the process of dropshipping products from AliExpress to eBay. It features a clean, user-friendly interface built with Tkinter, and securely manages API keys and user credentials through an encrypted configuration system.

## Features
- **Nested Configuration Schema**: Organizes settings for both sandbox and production environments.
- **Encrypted Storage**: Safely stores sensitive information such as API keys and tokens.
- **First-Run Configuration Wizard**: Guides users through the initial setup process to input their credentials.
- **API Integration**: Interacts with AliExpress and eBay APIs for product management and order synchronization.
- **Unit Testing**: Comprehensive test suite to ensure reliability and functionality.

## Project Structure
```
dropship-automator
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   └── storage.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── aliexpress.py
│   │   └── ebay.py
│   ├── gui
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── wizard.py
│   ├── helpers
│   │   ├── __init__.py
│   │   └── import_credentials.py
│   ├── db
│   │   ├── __init__.py
│   │   └── models.py
│   └── utils
│       ├── __init__.py
│       └── encryption.py
├── tests
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_ebay_api.py
│   ├── test_aliexpress_api.py
│   ├── test_encryption.py
│   └── test_gui.py
├── build
│   └── pyinstaller.spec
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dropship-automator.git
   ```
2. Navigate to the project directory:
   ```
   cd dropship-automator
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/main.py
   ```
2. Follow the prompts in the configuration wizard to set up your API keys and preferences.

## Testing
To run the unit tests, execute:
```
pytest
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License - see the LICENSE file for details.