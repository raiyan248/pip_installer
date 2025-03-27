import importlib
import subprocess

def install_missing_packages(package_list):
    """
    Installs missing packages from the provided list using pip.

    Args:
        package_list (list): A list of strings representing the package names.

    Returns:
        list: A list of successfully installed packages.
    """

    installed_packages = []
    for package in package_list:
        try:
            importlib.import_module(package)
            installed_packages.append(package)
        except ImportError:
            print(f"Installing missing package: {package}")
            subprocess.run(["sudo", "apt-get", "install", "python3-"+package])
            installed_packages.append(package)
    return installed_packages

# List of required packages
required_packages = [
    "pyttsx3",
    "speech_recognition",
    "wikipedia",
    "pygame",
    "webbrowser",
    "os",
    "requests",
    "smtplib",
    "pyautogui",
    "socket",
    "json",
    "random",
    "pyaudio",
    "numpy",
    "nltk"
]

# Install missing packages if necessary
installed_packages = install_missing_packages(required_packages)

# Import modules only after installation check (optional)
if all(package in installed_packages for package in required_packages):
    print("All required packages are installed.")
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    # ... rest of your code using the imported modules ...
else:
    print("Some packages failed to install. Please check manually.")