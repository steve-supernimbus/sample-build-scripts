import argparse
import os

COMMIT_ID_FILE_NAME="commit-id.txt"

def main(source, commit_id):
    log_step("Adding configs.")
    create_config_files(source, commit_id)
    log_step("Finished adding configs.")

def create_config_files(out_dir, commit_id):
    for dir in get_subdirectories(out_dir):
        log_step(f"Creating config inside {dir}")
        create_commit_id_file(dir, commit_id)

def get_subdirectories(root):
    sub_dirs = []
    for it in os.scandir(root):
        if it.is_dir():
            sub_dirs.append(it.path)
    return sub_dirs

def create_commit_id_file(path, commit_id):
    commit_id_file_path = os.path.join(path, COMMIT_ID_FILE_NAME)
    write_file(commit_id_file_path, commit_id)

def write_file(path, content):
    log_step(f"Writing {path}")
    f = open(path, "w")
    f.writelines(content)
    f.close()
    log_step(f"Successfully wrote {path}")

def log_step(step_name, step_output="No Output"):
    separator = "===================================================="
    print(separator)
    print(step_name)
    print(f"Step Output: {step_output}")
    print(separator)

def get_script_args():
    parser = argparse.ArgumentParser(description="Compress Script")
    parser.add_argument("--source")
    parser.add_argument("--commit-id", default="0")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.source, args.commit_id)
