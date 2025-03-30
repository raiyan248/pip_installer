import os
import subprocess
import sys
from datetime import datetime
from typing import List, Optional
from enum import Enum
import glob
import logging
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from threading import Thread

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class OSType(Enum):
    LINUX = "1"
    WINDOWS = "2"
    MAC = "3"

class PackageInfo:
    def __init__(self, name: str, install_time: float, version: Optional[str] = None):
        self.name = name
        self.install_time = install_time
        self.version = version

class PackageManager:
    def __init__(self):
        self.os_handlers = {
            OSType.LINUX: {
                'list': self.get_apt_package_times,
                'search': self._apt_search,
                'install': lambda pkg: self._run_system(f"sudo apt-get install {pkg} -y"),
                'uninstall': lambda pkg: self._run_system(f"sudo apt-get remove {pkg} -y")
            },
            OSType.WINDOWS: {
                'list': self.get_pip_package_times,
                'search': self._pip_search,
                'install': lambda pkg: self._run_system(f"pip install {pkg}"),
                'uninstall': lambda pkg: self._run_system(f"pip uninstall {pkg} -y")
            },
            OSType.MAC: {
                'list': self.get_brew_package_times,
                'search': self._brew_search,
                'install': lambda pkg: self._run_system(f"brew install {pkg}"),
                'uninstall': lambda pkg: self._run_system(f"brew uninstall {pkg}")
            }
        }

    @staticmethod
    def _run_subprocess(command: List[str]) -> Optional[str]:
        try:
            return subprocess.check_output(command, text=True, stderr=subprocess.DEVNULL)
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            logger.error(f"Command failed: {e}")
            return None

    @staticmethod
    def _run_system(command: str) -> bool:
        try:
            return os.system(command) == 0
        except Exception as e:
            logger.error(f"System command failed: {e}")
            return False

    def get_pip_package_times(self) -> List[PackageInfo]:
        result = self._run_subprocess([sys.executable, "-m", "pip", "list", "--format=freeze"])
        if not result:
            return []
        packages = []
        for line in result.splitlines():
            if not line.strip():
                continue
            name, version = line.split('==', 1)
            info = self._run_subprocess([sys.executable, "-m", "pip", "show", name])
            install_time = 0
            if info:
                for line in info.splitlines():
                    if line.startswith('Location:'):
                        location = line.split(':', 1)[1].strip()
                        pkg_path = os.path.join(location, f"{name.lower().replace('-', '_')}*.dist-info")
                        if dist_info := glob.glob(pkg_path):
                            install_time = os.path.getctime(dist_info[0])
                        break
            packages.append(PackageInfo(name, install_time, version))
        return packages

    def get_apt_package_times(self) -> List[PackageInfo]:
        result = self._run_subprocess(["dpkg", "-l"])
        if not result:
            return []
        packages = []
        for line in result.splitlines():
            if not line.strip() or 'python3-' not in line.lower() or not line.startswith('ii'):
                continue
            fields = line.split()
            name, version = fields[1], fields[2]
            info = self._run_subprocess(["dpkg-query", "-s", name])
            install_time = float(next((l.split(':', 1)[1].strip() for l in info.splitlines() 
                                    if l.startswith('Installed-Time:')), 0)) if info else 0
            packages.append(PackageInfo(name, install_time, version))
        return packages

    def get_brew_package_times(self) -> List[PackageInfo]:
        result = self._run_subprocess(["brew", "list", "--versions"])
        if not result:
            return []
        packages = []
        for line in result.splitlines():
            if not line.strip() or 'python' not in line.lower():
                continue
            name, version = line.split(maxsplit=1)
            try:
                install_time = os.path.getctime(f"/usr/local/Cellar/{name}")
            except OSError:
                install_time = 0
            packages.append(PackageInfo(name, install_time, version))
        return packages

    def _apt_search(self, term: str) -> List[str]:
        result = self._run_subprocess(["apt-cache", "search", term])
        return [line.split()[0] for line in result.splitlines() 
                if line.strip() and line.split()[0].startswith('python3-')] if result else []

    def _pip_search(self, term: str) -> List[str]:
        result = self._run_subprocess([sys.executable, "-m", "pip", "list", "--format=freeze"])
        return [line.split('==')[0] for line in result.splitlines() 
                if term.lower() in line.lower()] if result else []

    def _brew_search(self, term: str) -> List[str]:
        result = self._run_subprocess(["brew", "search", term])
        return [line.strip() for line in result.splitlines() 
                if line.strip() and 'python' in line.lower()] if result else []

    def execute_operation(self, os_type: OSType, operation: str, package: str = "") -> bool:
        handler = self.os_handlers[os_type]
        if operation == 'list':
            return handler[operation]()
        return handler[operation](package)

class PackageManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Package Manager")
        self.root.geometry("800x600")
        self.manager = PackageManager()
        self.os_type = None
        self.packages = []
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=5)
        style.configure("TLabel", padding=3)

        # Main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # OS Selection
        ttk.Label(self.main_frame, text="Select Operating System:").grid(row=0, column=0, sticky="w")
        self.os_var = tk.StringVar()
        os_options = ttk.Combobox(self.main_frame, textvariable=self.os_var, 
                                values=["Linux", "Windows", "Mac"], state="readonly")
        os_options.grid(row=0, column=1, sticky="w")
        os_options.bind("<<ComboboxSelected>>", self.on_os_select)
        
        # Package list frame
        self.list_frame = ttk.LabelFrame(self.main_frame, text="Installed Packages", padding="5")
        self.list_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")
        
        self.tree = ttk.Treeview(self.list_frame, columns=("Name", "Version", "Installed"), 
                               show="headings", height=10)
        self.tree.heading("Name", text="Package Name", command=lambda: self.sort_column("Name"))
        self.tree.heading("Version", text="Version", command=lambda: self.sort_column("Version"))
        self.tree.heading("Installed", text="Installed Time", command=lambda: self.sort_column("Installed"))
        self.tree.column("Name", width=200)
        self.tree.column("Version", width=100)
        self.tree.column("Installed", width=200)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=5)
        
        ttk.Button(btn_frame, text="Refresh List", command=self.refresh_list).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Install Package", command=self.show_install_dialog).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Uninstall Selected", command=self.uninstall_package).grid(row=0, column=2, padx=5)
        
        # Search results frame
        self.search_frame = ttk.LabelFrame(self.main_frame, text="Search Results", padding="5")
        self.search_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")
        self.search_results = ttk.Treeview(self.search_frame, columns=("Name",), show="headings", height=5)
        self.search_results.heading("Name", text="Package Name")
        self.search_results.column("Name", width=300)
        self.search_results.grid(row=0, column=0, sticky="nsew")
        
        search_scroll = ttk.Scrollbar(self.search_frame, orient="vertical", command=self.search_results.yview)
        search_scroll.grid(row=0, column=1, sticky="ns")
        self.search_results.configure(yscrollcommand=search_scroll.set)
        
        # Log output
        self.log_frame = ttk.LabelFrame(self.main_frame, text="Operation Log", padding="5")
        self.log_frame.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")
        self.log_text = scrolledtext.ScrolledText(self.log_frame, height=5)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.log_frame.grid_columnconfigure(0, weight=1)

    def on_os_select(self, event=None):
        os_map = {"Linux": OSType.LINUX, "Windows": OSType.WINDOWS, "Mac": OSType.MAC}
        self.os_type = os_map.get(self.os_var.get())
        self.refresh_list()

    def refresh_list(self):
        if not self.os_type:
            messagebox.showwarning("Warning", "Please select an operating system first")
            return
        
        self.tree.delete(*self.tree.get_children())
        self.packages = self.manager.execute_operation(self.os_type, 'list')
        for pkg in self.packages:
            time_str = (datetime.fromtimestamp(pkg.install_time).strftime('%Y-%m-%d %H:%M:%S') 
                       if pkg.install_time else "Unknown")
            self.tree.insert("", "end", values=(pkg.name, pkg.version or "N/A", time_str))
        self.log_text.insert(tk.END, f"Package list refreshed for {self.os_var.get()}\n")

    def sort_column(self, col):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort()
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

    def show_install_dialog(self):
        if not self.os_type:
            messagebox.showwarning("Warning", "Please select an operating system first")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Install Package")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Enter search term:").pack(pady=5)
        search_entry = ttk.Entry(dialog)
        search_entry.pack(pady=5)
        
        result_list = ttk.Treeview(dialog, columns=("Name",), show="headings")
        result_list.heading("Name", text="Package Name")
        result_list.column("Name", width=300)
        result_list.pack(fill="both", expand=True, pady=5)
        
        def search_packages():
            term = search_entry.get()
            results = self.manager.execute_operation(self.os_type, 'search', term)
            result_list.delete(*result_list.get_children())
            for pkg in results:
                result_list.insert("", "end", values=(pkg,))
        
        ttk.Button(dialog, text="Search", command=search_packages).pack(pady=5)
        
        def install_selected():
            selected = result_list.selection()
            if selected:
                pkg = result_list.item(selected[0])['values'][0]
                Thread(target=self.install_package, args=(pkg,)).start()
                dialog.destroy()
        
        ttk.Button(dialog, text="Install Selected", command=install_selected).pack(pady=5)

    def install_package(self, package):
        success = self.manager.execute_operation(self.os_type, 'install', package)
        self.log_text.insert(tk.END, f"Installing {package}: {'Success' if success else 'Failed'}\n")
        if success:
            self.refresh_list()

    def uninstall_package(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a package to uninstall")
            return
        
        pkg_name = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", f"Uninstall {pkg_name}?"):
            Thread(target=self._uninstall_thread, args=(pkg_name,)).start()

    def _uninstall_thread(self, package):
        success = self.manager.execute_operation(self.os_type, 'uninstall', package)
        self.log_text.insert(tk.END, f"Uninstalling {package}: {'Success' if success else 'Failed'}\n")
        if success:
            self.refresh_list()

def main():
    root = tk.Tk()
    app = PackageManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()