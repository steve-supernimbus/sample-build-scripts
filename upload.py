import argparse
import datetime
import os
import subprocess

URLS_FILE_PATH = os.path.join(os.getcwd(), 'urls.txt')

def main(bucket, local_path, remote_path):
    log_step("Begin Upload.")
    log_step(f"Uploading contents from {local_path}")
    urls = sync_folder(bucket, local_path, remote_path)
    log_step(f"Presigned URLs: {urls}")
    write_urls_file(URLS_FILE_PATH, urls)
    log_step("Finish Uploading.")

def sync_folder(bucket, local_path, remote_path):
    urls = []
    timestamp = get_timestamp()
    for dirpath, dir_names, file_names in os.walk(local_path):
        for file_name in file_names:
            local_path = os.path.join(dirpath, file_name)
            remote_file_name = file_name.replace(" ", "-")
            remote_path = get_remote_path(bucket, remote_path, timestamp, remote_file_name)
            upload_file_to_s3(local_path, remote_path)
            urls.append(generate_presigned_url(remote_path))
    return urls

def upload_file_to_s3(local_path, remote_path):
    log_step(f"Uploading {local_path} to {remote_path}")
    aws_cli(
        [
            "s3",
            "cp",
            local_path,
            remote_path,
            "--storage-class=INTELLIGENT_TIERING",
            "--no-progress",
        ]
    )

def generate_presigned_url(remote_path):
    log_step(f"Generating pre-signed url for {remote_path}")
    return aws_cli(
        [
            "s3",
            "presign",
            remote_path,
        ]
    )

def aws_cli(args):
    aws_call = ["aws"] + args
    log_step(f"AWS CLI: {subprocess.list2cmdline(aws_call)}")
    try:
        return subprocess.run(
            aws_call,
            capture_output = True,
            text = True,
        ).stdout
    except:
        raise Exception("Aws command failed")

def get_timestamp():
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime("%Y-%m-%d-%H:%M:%S")

def get_remote_path(bucket, remote_directory, timestamp, file_name):
    return f"s3://{bucket}/{remote_directory}/{timestamp}/{file_name}"

def write_urls_file(url_file_path, urls):
    log_step("Writing Presigned URLs to disk.")
    write_file(url_file_path, " ".join(urls))
    log_step("Successfully write URLs to disk.")

def write_file(file_name, content):
    f = open(file_name, "w")
    f.write(content)
    f.close()

def log_step(step):
    separator = "===================================================="
    new_line = "\n"
    print(separator)
    print(f"Build Step: {step}")
    print(separator)
    print(new_line)

def get_script_args():
    parser = argparse.ArgumentParser(description="Upload Script")
    parser.add_argument("--bucket")
    parser.add_argument("--local-directory")
    parser.add_argument("--remote-directory")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.bucket, args.local_directory, args.remote_directory)
