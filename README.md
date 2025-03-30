 # Python Package Installer Script
 This repository contains a Python script designed to dynamically install missing Python packages based on user input. The script checks if specified packages are installed, attempts to install them using pip if they’re missing, and provides a summary of the installation process.  
 ## Key Features
 - User Input: Allows users to specify one or more package names to install.
 - Dynamic Installation: Uses pip to install missing packages instead of relying on a hardcoded list.
 - Error Handling: Includes try/except blocks to manage installation failures gracefully.
 - Installation Summary: Provides feedback on which packages were successfully installed and which failed.  
 ## Changes from Previous Version
 The original script was modified to enhance usability and flexibility. Below are the key updates:
 1. Removed Hardcoded Package List
    - Original: The script had a predefined list of packages (required_packages) such as pyttsx3, speech_recognition, etc.
    - Change: Replaced with an interactive prompt where users input package names (e.g., "numpy pandas") separated by spaces.
    - Reason: Makes the script reusable for any package, not just a specific set.
 2. User Input Handling
    - Addition: Added print("Enter the package name(s)...") and input("> ") to collect package names.
    - Processing: Uses split() to convert the input string into a list of package names.
    - Reason: Enables dynamic package specification at runtime.
 3. Switched from apt-get to pip
    - Original: Used subprocess.run(["sudo", "apt-get", "install", "python3-"+package]).
    - Change: Now uses subprocess.run(["pip", "install", package], check=True).
    - Reason: pip is the standard Python package manager, more appropriate and widely compatible than apt-get (which is system-specific and requires sudo).
 4. Enhanced Error Handling
    - Addition: Wrapped the subprocess.run call in a try/except block to catch subprocess.CalledProcessError.
    - Feedback: Prints success or failure messages for each package (e.g., "Successfully installed numpy" or "Failed to install numpy").
    - Reason: Prevents the script from crashing on installation errors and informs the user of specific failures.
 5. Improved Feedback with Installation Summary
    - Addition: After installation, the script displays a summary listing successfully installed packages and notes any that failed.
    - Example Output:
      Installation Summary:
      - numpy: Installed successfully
      - pandas: Installed successfully
    - Reason: Provides clear visibility into the script’s results, especially useful when installing multiple packages.
 6. Conditional Execution
    - Addition: Checks if required_packages is empty and prints "No packages specified for installation" if no input is provided.
    - Reason: Prevents unnecessary execution and improves user experience.  
 ## Usage
 1. Clone the repository:
    git clone <repository-url>
 2. Navigate to the directory:
    cd <repository-name>
 3. Run the script:
    python installer_script.py
 4. When prompted, enter the package names separated by spaces:
    Enter the package name(s) you want to install (separate multiple packages with spaces):
    > numpy pandas
 Note: Ensure you have pip installed and appropriate permissions. You may need to run with sudo or in a virtual environment depending on your system setup.  
 ## Requirements
 - Python 3.x
 - pip (Python package manager)
 - Modules used in the script:
   - importlib (built-in)
   - subprocess (built-in)  
 ## Future Improvements
 - Add support for specifying package versions (e.g., "numpy==1.21.0").
 - Include an option to use alternative package managers (e.g., conda).
 - Add logging to save installation results to a file.  

