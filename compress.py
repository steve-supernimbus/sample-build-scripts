import argparse
import os
import subprocess
import shutil

def main(source, target, build_id):
    create_directory(os.path.join(os.getcwd(), target))
    compress_directory(source, target, build_id)
    log_step(f"Finished compressing {source} to {target}")

def create_directory(dir_path):
    if os.path.exists(dir_path):
        log_step(f"Removing directory: {dir_path}")
        shutil.rmtree(dir_path)
    if not os.path.exists(dir_path):
        log_step(f"Creating directory: {dir_path}")
        os.makedirs(dir_path)

def compress_directory(out_dir, zip_dir, build_id):
    for dir in get_subdirectories(out_dir):
        zip_path(dir, os.path.join(os.getcwd(), zip_dir), build_id)

def get_subdirectories(root):
    sub_dirs = []
    for it in os.scandir(root):
        if it.is_dir():
            sub_dirs.append(it.path)
    return sub_dirs

def zip_path(source_dir, output_dir, build_id):
    zip_path = os.path.join(output_dir, f"{os.path.basename(source_dir)}_{build_id}.zip")
    log_step(f"Zipping {source_dir} to {zip_path}")
    cli(["7z", "a", zip_path, source_dir])

def cli(args):
    try:
        log_step(f"Making the following CLI call: {' '.join(args)}")
        return subprocess.run(args, check=True)
    except:
        raise Exception("cli call failed")

def log_step(step_name, step_output="No Output"):
    separator = "===================================================="
    print(separator)
    print(step_name)
    print(f"Step Output: {step_output}")
    print(separator)

def get_script_args():
    parser = argparse.ArgumentParser(description="Compress Script")
    parser.add_argument("--source")
    parser.add_argument("--target", default=os.getcwd())
    parser.add_argument("--build-id", default="0")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.source, args.target, args.build_id)
