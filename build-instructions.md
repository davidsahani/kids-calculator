## Build Instructions for Kids-Calculator

Follow these steps to successfully build Kids-Calculator on your system.

### 1. Install Python 3.10

Ensure that you have Python 3.10 installed on your system. If you don't have it installed, follow the instructions below to install it.

**For Linux users:**

If it's your first time installing Python on Linux, I would recommend using pyenv. To install `pyenv` on Linux, follow these steps:

**Prerequisites:**

Before installing `pyenv`, make sure your system meets the following requirements:

- Linux operating system (e.g., Ubuntu, CentOS, Fedora)
- Basic development tools (e.g., `gcc`, `make`, `git`)
- Additional dependencies for building Python (refer to `pyenv` documentation for specific requirements)

1. Clone the `pyenv` repository by executing the following command in a terminal:

   ```
   git clone https://github.com/pyenv/pyenv.git ~/.pyenv
   ```

   This will clone the `pyenv` repository into the `~/.pyenv` directory.

2. Configure your shell to recognize `pyenv`. Add the following lines to your shell configuration file (e.g., `~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, or `~/.profile`):

   **For Bash:**

   ```bash
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init --path)"
   ```

   **For Zsh:**

   ```zsh
   export PYENV_ROOT="$HOME/.pyenv"
   export PATH="$PYENV_ROOT/bin:$PATH"
   eval "$(pyenv init --path zsh)"
   ```

   Save the file and reload your shell configuration by running:

   ```bash
   source ~/.bashrc  # or ~/.zshrc, depending on your shell
   ```

3. Verify the installation by running the following command:

   ```bash
   pyenv --version
   ```

   If the installation was successful, it should display the version of `pyenv` installed.

4. Install the required Python version by executing the following command:

   ```bash
   pyenv install 3.10.11
   ```

5. Set the global Python version to be used by default:

   ```bash
   pyenv global 3.10.11
   ```

Note: These installation instructions may change in the future. If they don't work, refer to the official `pyenv` installation instructions: [pyenv GitHub repository](https://github.com/pyenv/pyenv#getting-pyenv).


### 2. Install Buildozer

Install Buildozer by following the instructions provided in the [Buildozer documentation](https://buildozer.readthedocs.io/en/latest/).

   - Make sure to install the necessary build dependencies for Buildozer to run successfully.

   - Confirm that Buildozer is added to your system's PATH environment variable, allowing you to execute it from the command line.

### 3. Navigate to the Kids-Calculator Project Directory

Navigate to the root directory of the Kids-Calculator project. For example, if the project is located in `~/Documents/GitHub/kids-calculator`, use the following command:

```bash
cd ~/Documents/GitHub/kids-calculator
```

### 4. Build the Kids-Calculator App

Start the build process by running the following command:

- To build the app in debug mode, use the following command:
 
    ```bash
    buildozer android debug
    ```

- To build the app in release mode, use the following command:

    ```bash
    buildozer android release
    ```


## Building for Linux and Windows

To successfully build your project for Linux and Windows operating systems, follow the steps below:

1. Ensure that all project requirements are installed.

2. Install `pyinstaller` by executing the following command:
   ```bash
   pip install pyinstaller
   ```

**For Linux users:**

3. Open a terminal and navigate to project directory.

4. Run the following command to build the project for Linux:
   ```bash
   python build-win-linux.py
   ```

**For Windows users:**

Before proceeding, make sure you have a C++ compiler installed on your system. If you have Visual Studio 2019 or a later version installed, follow these additional steps:

   - Check if the Windows 10 SDK (10.0.18362 or later) is installed. If not, install it.

   - Use Visual Studio's installer to install the "C++ for MFC for ..." package.

   - Alternatively, you can install the Visual Studio Build Tools from the following link: 
     [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

3. Open a command prompt and navigate to project directory.

4. Run the following command to build the project for Windows:
   ```bash
   python build-win-linux.py
   ```

Following these steps will start the build process for the respective platforms (Linux/Windows). This will build the application and generate application files along with its executable, which will be available in the project's bin directory under the name "Kids Calculator".