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
            print(f"Package {package} is already installed.")
            installed_packages.append(package)
        except ImportError:
            print(f"Installing missing package: {package}")
            try:
                subprocess.run(["pip", "install", package], check=True)
                print(f"Successfully installed {package}")
                installed_packages.append(package)
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}. Please try installing it manually.")
    return installed_packages

# Get package names from user input
print("Enter the package name(s) you want to install (separate multiple packages with spaces):")
user_input = input("> ")
required_packages = user_input.split()  # Split input by spaces into a list

# Install missing packages if necessary
if required_packages:
    installed_packages = install_missing_packages(required_packages)
    
    # Verify installation
    if installed_packages:
        print("\nInstallation Summary:")
        for package in installed_packages:
            print(f"- {package}: Installed successfully")
        if len(installed_packages) < len(required_packages):
            print("\nSome packages failed to install. Missing:")
            for package in required_packages:
                if package not in installed_packages:
                    print(f"- {package}")
    else:
        print("No packages were installed successfully.")
else:
    print("No packages specified for installation.")