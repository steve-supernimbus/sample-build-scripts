import argparse
import datetime
import sys
import subprocess

file_name = "sample-build-file.txt"
local_path = f"./{file_name}"

def main(local_path, remote_path, bucket):
    log_step("Begin Upload.")

    log_step("Generating remote path.")
    remote_path = get_remote_path()
    log_step(remote_path)

    log_step("Uploading file to S3.")
    upload_file_to_s3(local_path, remote_path)
    log_step("Successfully uploaded file to S3.")

    log_step("Generate Presigned URL.")
    url = generate_presigned_url(remote_path)
    log_step(url)

    log_step("Writing Presigned URL to disk.")
    write_file("url.txt", url)
    log_step("Successfully write URL to disk")

    log_step("Finish Uploading.")

def upload_file_to_s3(local_path, remote_path):
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

def get_remote_path(bucket, remote_path):
    bucket = "gamelift-tutorial-build-steve"
    remote_dir = "nightly-builds"
    return f"s3://{bucket}/{remote_dir}/{get_timestamp()}/{file_name}"

def write_file(file_name, content):
    f = open(f"./{file_name}", "w")
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
    parser.add_argument("--remote-directory")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.local_path, args.remote_path, args.bucket)
