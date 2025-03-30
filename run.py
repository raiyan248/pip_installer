import os

def install_linux(package):
    os.system(f"sudo apt-get install python3-{package} -y")

def install_windows(package):
    os.system(f"pip install {package}")

def install_mac(package):
    os.system(f"brew install {package}")

def main():
    print("Select your operating system:")
    print("1. Linux")
    print("2. Windows")
    print("3. Mac")
    choice = input("Enter the number corresponding to your OS: ")
    package = input("Enter the package name: ")
    
    if choice == "1":
        install_linux(package)
    elif choice == "2":
        install_windows(package)
    elif choice == "3":
        install_mac(package)
    else:
        print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
