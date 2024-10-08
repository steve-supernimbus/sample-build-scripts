import os
import subprocess

def main():
    read_write(os.getcwd())

def read_write(project_dir):
    run_powershell_command((
        f'Get-ChildItem -Path "{project_dir}"'
        + r"-Recurse -File | % { $_.IsReadOnly=$False }"
    ))

def run_powershell_command(cmd):
    return subprocess.run(
        [
            "powershell",
            "-Command",
            cmd
        ],
        capture_output=True
    )

if __name__ == "__main__":
    main()
