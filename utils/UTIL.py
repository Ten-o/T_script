import platform
import os


def load_so_file():
    system = platform.system().lower()
    if system == 'windows':
        file_ext = 'pyd'
    else:
        file_ext = 'so'
    machine_type = platform.machine().replace('aarch64', 'arm').replace('x86_64', 'amd').replace('AMD64','amd')
    python_version = f"py{platform.python_version_tuple()[0]}{platform.python_version_tuple()[1]}"
    so_filename = f"TEN_UTIL_{system}_{machine_type}_{python_version}.{file_ext}"
    os.system(f'cp ./utils/{so_filename} ./utils/TEN_UTIL.{file_ext}')
    return so_filename
