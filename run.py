import os
import subprocess
import sys

def search_pip_package(search_term):
    try:
        # Search PyPI using pip
        result = subprocess.check_output([sys.executable, "-m", "pip", "search", search_term], text=True)
        packages = []
        for line in result.split('\n'):
            if line.strip() and '(' in line:
                package_name = line.split()[0]
                packages.append(package_name)
        return packages[:5]  # Return top 5 results
    except:
        return []

def search_apt_package(search_term):
    try:
        # Search apt packages
        result = subprocess.check_output(["apt-cache", "search", search_term], text=True)
        packages = []
        for line in result.split('\n'):
            if line.strip():
                package_name = line.split()[0]
                if package_name.startswith('python3-'):
                    packages.append(package_name)
        return packages[:5]  # Return top 5 results
    except:
        return []

def search_brew_package(search_term):
    try:
        # Search Homebrew packages
        result = subprocess.check_output(["brew", "search", search_term], text=True)
        packages = []
        for line in result.split('\n'):
            if line.strip() and 'python' in line.lower():
                packages.append(line.strip())
        return packages[:5]  # Return top 5 results
    except:
        return []

def install_linux(package):
    os.system(f"sudo apt-get install {package} -y")

def install_windows(package):
    os.system(f"pip install {package}")

def install_mac(package):
    os.system(f"brew install {package}")

def display_search_results(packages, os_type):
    if not packages:
        print(f"No {os_type} packages found.")
        return None
    
    print(f"\nFound {os_type} packages:")
    for i, pkg in enumerate(packages, 1):
        print(f"{i}. {pkg}")
    
    choice = input("Enter the number of the package to install (or 0 to skip): ")
    if choice == "0":
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(packages):
            return packages[idx]
        else:
            print("Invalid selection.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

def main():
    while True:
        print("\nSelect your operating system:")
        print("1. Linux")
        print("2. Windows")
        print("3. Mac")
        print("4. Exit")
        choice = input("Enter the number corresponding to your OS: ")
        
        if choice == "4":
            print("Goodbye!")
            break
            
        search_term = input("Enter what you want to search for: ")
        
        if choice == "1":
            packages = search_apt_package(search_term)
            selected_package = display_search_results(packages, "Linux")
            if selected_package:
                install_linux(selected_package)
                
        elif choice == "2":
            packages = search_pip_package(search_term)
            selected_package = display_search_results(packages, "Windows")
            if selected_package:
                install_windows(selected_package)
                
        elif choice == "3":
            packages = search_brew_package(search_term)
            selected_package = display_search_results(packages, "Mac")
            if selected_package:
                install_mac(selected_package)
                
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
