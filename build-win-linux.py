import os
import subprocess

PROJECT_NAME = "Kids Calculator"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(SCRIPT_DIR, 'source')
PROJECT_OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'bin')
PROJECT_TEMP_DIR = os.path.join(PROJECT_OUTPUT_DIR, 'temp')


def build_project() -> int:
    fonts_dir = os.path.join(PROJECT_DIR, 'fonts')
    icons_dir = os.path.join(PROJECT_DIR, 'icons')
    kv_file = os.path.join(PROJECT_DIR, 'numpad.kv')
    icon_file = os.path.join(PROJECT_DIR, 'icons', 'calculator.ico')
    # workaround: adding delayed button module, kivy is not able to import it
    delayed_button_module = os.path.join(PROJECT_DIR, 'delayed_button.py')

    sep = ";" if os.name == "nt" else ":"

    pyinstaller_cmd = [
        "pyinstaller",
        "--workpath", PROJECT_TEMP_DIR,
        "--specpath", PROJECT_TEMP_DIR,
        "--distpath", PROJECT_OUTPUT_DIR,
        "--noconfirm", "--clean",

        "--hidden-import", "kivy_deps",
        "--collect-submodules", "kivymd",

        "--onedir", "--windowed",
        "--name", PROJECT_NAME,
        "--icon", icon_file,
        "--add-data", f"{icons_dir}{sep}icons/",
        "--add-data", f"{fonts_dir}{sep}fonts/",
        "--add-data", f"{kv_file}{sep}.",
        "--add-data", f"{delayed_button_module}{sep}.",
        os.path.join(PROJECT_DIR, "main.py"),
    ]

    return subprocess.call(pyinstaller_cmd)


def main() -> None:

    os.chdir(PROJECT_DIR)

    # build the project
    status = build_project()
    if status != 0:
        print("Pyinstaller failed to build the project")


if __name__ == '__main__':
    main()
