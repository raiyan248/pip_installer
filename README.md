<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Package Installer Script</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        h1, h2, h3 {
            color: #333;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .section {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1>Python Package Installer Script</h1>
    <p>
        This repository contains a Python script designed to dynamically install missing Python packages based on user input. 
        The script checks if specified packages are installed, attempts to install them using <code>pip</code> if they’re missing, 
        and provides a summary of the installation process.
    </p>

    <div class="section">
        <h2>Key Features</h2>
        <ul>
            <li><strong>User Input</strong>: Allows users to specify one or more package names to install.</li>
            <li><strong>Dynamic Installation</strong>: Uses <code>pip</code> to install missing packages instead of relying on a hardcoded list.</li>
            <li><strong>Error Handling</strong>: Includes try/except blocks to manage installation failures gracefully.</li>
            <li><strong>Installation Summary</strong>: Provides feedback on which packages were successfully installed and which failed.</li>
        </ul>
    </div>

    <div class="section">
        <h2>Changes from Previous Version</h2>
        <p>The original script was modified to enhance usability and flexibility. Below are the key updates:</p>
        <ol>
            <li>
                <strong>Removed Hardcoded Package List</strong>
                <ul>
                    <li><em>Original</em>: The script had a predefined list of packages (<code>required_packages</code>) such as <code>pyttsx3</code>, <code>speech_recognition</code>, etc.</li>
                    <li><em>Change</em>: Replaced with an interactive prompt where users input package names (e.g., "numpy pandas") separated by spaces.</li>
                    <li><em>Reason</em>: Makes the script reusable for any package, not just a specific set.</li>
                </ul>
            </li>
            <li>
                <strong>User Input Handling</strong>
                <ul>
                    <li><em>Addition</em>: Added <code>print("Enter the package name(s)...")</code> and <code>input("> ")</code> to collect package names.</li>
                    <li><em>Processing</em>: Uses <code>split()</code> to convert the input string into a list of package names.</li>
                    <li><em>Reason</em>: Enables dynamic package specification at runtime.</li>
                </ul>
            </li>
            <li>
                <strong>Switched from <code>apt-get</code> to <code>pip</code></strong>
                <ul>
                    <li><em>Original</em>: Used <code>subprocess.run(["sudo", "apt-get", "install", "python3-"+package])</code>.</li>
                    <li><em>Change</em>: Now uses <code>subprocess.run(["pip", "install", package], check=True)</code>.</li>
                    <li><em>Reason</em>: <code>pip</code> is the standard Python package manager, more appropriate and widely compatible than <code>apt-get</code> (which is system-specific and requires sudo).</li>
                </ul>
            </li>
            <li>
                <strong>Enhanced Error Handling</strong>
                <ul>
                    <li><em>Addition</em>: Wrapped the <code>subprocess.run</code> call in a <code>try/except</code> block to catch <code>subprocess.CalledProcessError</code>.</li>
                    <li><em>Feedback</em>: Prints success or failure messages for each package (e.g., "Successfully installed numpy" or "Failed to install numpy").</li>
                    <li><em>Reason</em>: Prevents the script from crashing on installation errors and informs the user of specific failures.</li>
                </ul>
            </li>
            <li>
                <strong>Improved Feedback with Installation Summary</strong>
                <ul>
                    <li><em>Addition</em>: After installation, the script displays a summary listing successfully installed packages and notes any that failed.</li>
                    <li><em>Example Output</em>:
                        <pre>
Installation Summary:
- numpy: Installed successfully
- pandas: Installed successfully
                        </pre>
                    </li>
                    <li><em>Reason</em>: Provides clear visibility into the script’s results, especially useful when installing multiple packages.</li>
                </ul>
            </li>
            <li>
                <strong>Conditional Execution</strong>
                <ul>
                    <li><em>Addition</em>: Checks if <code>required_packages</code> is empty and prints "No packages specified for installation" if no input is provided.</li>
                    <li><em>Reason</em>: Prevents unnecessary execution and improves user experience.</li>
                </ul>
            </li>
        </ol>
    </div>

    <div class="section">
        <h2>Usage</h2>
        <ol>
            <li>Clone the repository:
                <pre><code>git clone &lt;repository-url&gt;</code></pre>
            </li>
            <li>Navigate to the directory:
                <pre><code>cd &lt;repository-name&gt;</code></pre>
            </li>
            <li>Run the script:
                <pre><code>python installer_script.py</code></pre>
            </li>
            <li>When prompted, enter the package names separated by spaces:
                <pre>
Enter the package name(s) you want to install (separate multiple packages with spaces):
&gt; numpy pandas
                </pre>
            </li>
        </ol>
        <p><strong>Note</strong>: Ensure you have <code>pip</code> installed and appropriate permissions. You may need to run with <code>sudo</code> or in a virtual environment depending on your system setup.</p>
    </div>

    <div class="section">
        <h2>Requirements</h2>
        <ul>
            <li>Python 3.x</li>
            <li><code>pip</code> (Python package manager)</li>
            <li>Modules used in the script:
                <ul>
                    <li><code>importlib</code> (built-in)</li>
                    <li><code>subprocess</code> (built-in)</li>
                </ul>
            </li>
        </ul>
    </div>

    <div class="section">
        <h2>Future Improvements</h2>
        <ul>
            <li>Add support for specifying package versions (e.g., "numpy==1.21.0").</li>
            <li>Include an option to use alternative package managers (e.g., <code>conda</code>).</li>
            <li>Add logging to save installation results to a file.</li>
        </ul>
    </div>

</body>
</html>