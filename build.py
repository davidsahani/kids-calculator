import os
import shutil
import subprocess
import sys
from configparser import ConfigParser


def parse_version(version: str) -> tuple[int, ...]:
    return tuple(map(int, (
        v for v in version.split(".") if v.isdigit())
    ))


def clean_dir(directory: str) -> None:
    try:
        shutil.rmtree(directory)
    except OSError:  # may fail once.
        shutil.rmtree(directory)


def build(name: str, src_dir: str, out_dir: str) -> int:
    fonts_dir = os.path.join(src_dir, 'fonts')
    icons_dir = os.path.join(src_dir, 'icons')
    kv_file = os.path.join(src_dir, 'numpad.kv')
    icon_file = os.path.join(src_dir, 'icons', 'calculator.ico')
    # workaround: adding delayed button module, kivy is not able to import it
    delayed_button_module = os.path.join(src_dir, 'delayed_button.py')

    sep = ";" if os.name == "nt" else ":"

    dist_dir = os.path.join(out_dir, "dist")

    pyinstaller_cmd = [
        "pyinstaller",
        "--distpath", out_dir,
        "--workpath", dist_dir,
        "--specpath", dist_dir,
        "--noconfirm", "--clean",

        "--hidden-import", "kivy_deps",
        "--collect-submodules", "kivymd",

        "--onedir", "--windowed",
        "--name", name,
        "--icon", icon_file,
        "--add-data", f"{icons_dir}{sep}icons/",
        "--add-data", f"{fonts_dir}{sep}fonts/",
        "--add-data", f"{kv_file}{sep}.",
        "--add-data", f"{delayed_button_module}{sep}.",
        os.path.join(src_dir, "main.py"),
    ]

    pyinstaller_version = subprocess.check_output(
        ["pyinstaller", "--version"]).decode().strip()

    if parse_version(pyinstaller_version) > (5, 13, 2):
        pyinstaller_cmd.extend(["--contents-directory", "."])

    return subprocess.call(pyinstaller_cmd)


def create_setup_installer(script_file: str, app_version: str) -> int:
    program_path = "C:\\Program Files (x86)"
    inno_setup_dir = [pathname for pathname in os.listdir(
        program_path) if pathname.lower().startswith("inno setup")
    ]
    if not inno_setup_dir:
        print(
            f"Couldn't locate Inno Setup in '{program_path}' " +
            "Either it's not installed or is in alternate path.",
            file=sys.stderr
        )
        return 1
    iscc = os.path.join(program_path, inno_setup_dir[0], "ISCC.exe")
    if not os.path.exists(iscc):
        print(
            "Couldn't locate Inno Setup Complier (ISCC.exe) " +
            f"in '{os.path.dirname(iscc)}'", file=sys.stderr
        )
        return 1

    # create setup installer using inno setup compiler.
    return subprocess.call([iscc, script_file, f"/DAppVersion={app_version}"])


def main() -> int:
    project_name = "kids-calculator"

    script_dir = os.path.dirname(__file__)  # project directory.
    source_dir = os.path.join(script_dir, "source")
    output_dir = os.path.join(script_dir, "build")

    config = ConfigParser()  # Initialize parser.
    config.read(os.path.join(script_dir, "buildozer.spec"))
    version = config.get("app", "version")

    if os.path.exists(output_dir):
        clean_dir(output_dir)

    os.chdir(script_dir)  # change cwd to script directory.

    # disable kivy logger for executable.
    os.environ["KIVY_NO_FILELOG"] = "1"
    os.environ["KIVY_NO_CONSOLELOG"] = "1"

    status = build(project_name, source_dir, output_dir)

    if status != 0:
        return status  # abort build failed.

    if sys.platform == 'win32':
        shutil.make_archive(
            os.path.join(output_dir, f"{project_name}-portable"),
            'zip', os.path.join(output_dir, project_name),
        )
        return create_setup_installer("setup.iss", version)

    return 0  # success


if __name__ == '__main__':
    sys.exit(main())
