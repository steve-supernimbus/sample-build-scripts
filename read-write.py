import os
import subprocess

def main():
    read_write(os.getcwd())

def read_write(project_dir):
    log_step(f"Making the following directory read/writable: {project_dir}")
    run_powershell_command((
        f'Get-ChildItem -Path "{project_dir}"'
        + r"-Recurse -File | % { $_.IsReadOnly=$False }"
    ))

def log_step(step_name, step_output="No Output"):
    separator = "===================================================="
    print(separator)
    print(step_name)
    print(f"Step Output: {step_output}")
    print(separator)

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
