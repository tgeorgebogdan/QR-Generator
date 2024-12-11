# QR Code Generator Batch Script and Python Script

## Overview
This guide details the usage of a batch script and accompanying Python script (`qr.py`) to generate QR codes and organize them into SVG files. The batch script automates the installation of required dependencies, ensures the system environment is set up, and executes the Python script. The Python script (`qr.py`) handles the logic for generating QR codes, custom IDs, and SVG output.

## Batch Script Features
- Verifies if Python is installed.
- Checks and installs `pip` if necessary.
- Upgrades `pip` to the latest version.
- Installs or updates required Python packages: `qrcode[pil]` and `svgwrite`.
- Downloads the latest version of the `qr.py` script from GitHub.
- Provides an option to restart the script after execution.

## Python Script (`qr.py`) Features
- Generates custom IDs based on user-specified parameters (e.g., area, producer code, year, etc.).
- Generates QR codes for the custom IDs.
- Saves QR codes in base64-encoded PNG format.
- Organizes QR codes and IDs into SVG files with specified dimensions and layout.
- Maintains a record of generated IDs in a CSV file to avoid duplicates.

## Prerequisites
- Python must be installed and accessible in the system's PATH.
- Internet connection for downloading dependencies and the script from GitHub.
- `curl` installed on the system for downloading the Python script.

## Script Workflow
### Batch Script
1. **Python Check**: Ensures Python is installed; prompts the user to install it if missing.
2. **Pip Check and Installation**: Ensures `pip` is available; attempts installation if not found.
3. **Pip Upgrade**: Updates `pip` to the latest version.
4. **Dependency Installation**: Installs `qrcode[pil]` and `svgwrite` using `pip`.
5. **GitHub Update**: Downloads the latest version of `qr.py` from a GitHub repository.
6. **Script Execution**: Executes the `qr.py` script.
7. **Restart or Exit Option**: Allows the user to restart the script or exit upon completion.

### Python Script (`qr.py`)
1. **Directory Management**: Ensures the output directory exists.
2. **Custom ID Generation**: Generates unique IDs based on user input.
3. **QR Code Creation**: Creates QR codes for each generated ID.
4. **SVG File Creation**: Organizes QR codes and IDs into SVG files based on a predefined template.
5. **ID Tracking**: Saves generated IDs to a CSV file to prevent duplication.

## Usage
### Batch Script
1. Clone or download the batch script.
2. Place the script in the desired working directory.
3. Execute the script by double-clicking the `.bat` file or running it in a command prompt.

### Python Script (`qr.py`)
1. The Python script is automatically executed by the batch script. Ensure it is present in the same directory.
2. If running independently, ensure required dependencies are installed.

## Configuration
### Batch Script
- Update the `SCRIPT_URL` variable with the actual URL of your `qr.py` script in the GitHub repository.

### Python Script (`qr.py`)
- Modify the `rect_dimensions` array to change the SVG template layout.
- Configure the `generate_custom_code` function to customize ID encoding logic.

## Example
### Batch Script
```bat
set SCRIPT_URL=https://raw.githubusercontent.com/your-username/your-repo/main/qr.py
```
Replace `your-username` and `your-repo` with your GitHub username and repository name.

### Python Script Configuration
```python
config = {
    'area': 1,  # e.g., 1 for Energy
    'producer_code': '24',
    'year': 2024,
    'model_code': 'D0'
}
```

## Notes
- Ensure the Python script is compatible with the dependencies specified in this script.
- If the GitHub download fails, the batch script uses the local version of `qr.py` if available.
- Remove redirections like `>nul 2>&1` in the batch script for debugging.

## Troubleshooting
### Batch Script
- **Python not found**: Install Python from [python.org](https://www.python.org/).
- **Pip installation fails**: Ensure Python is correctly installed and `ensurepip` is available.
- **Dependency installation issues**: Check your internet connection and ensure `pip` is updated.
- **GitHub download issues**: Verify the `SCRIPT_URL` and your internet connection.

### Python Script
- **File Not Found**: Ensure `USED_IDS_FILE` and `OUTPUT_DIR` paths are correctly set.
- **ID Overlap**: Check the `used_ids.csv` file for previously generated IDs.

## License
This script and the Python script are provided as-is under the MIT License. Modify and distribute them as needed.

