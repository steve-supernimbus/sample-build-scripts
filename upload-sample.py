import sys
import subprocess

file_name = "sample-build-file.txt"
local_path = f"./{file_name}"

bucket = "gamelift-tutorial-build-steve"
remote_dir = "nightly-builds"
remote_path = f"s3://{bucket}/{remote_dir}/{file_name}"

def main(argv):
    log_step("Begin Upload.")
    log_step("Uploading file to S3.")
    upload_file_to_s3(local_path, remote_path)
    log_step("Finish Uploading.")

def upload_file_to_s3(local_path, remote_path):
    aws_cli(
        [
            "s3",
            "cp",
            local_path,
            remote_path,
            "--storage-class=INTELLIGENT_TIERING",
            "--no-progress"
        ]
    )

def aws_cli(args):
    aws_call = ["aws"] + args
    log_step(f"AWS CLI: {subprocess.list2cmdline(aws_call)}")
    try:
        subprocess.run(aws_call)
    except:
        raise Exception("Aws command failed")

def log_step(step):
    separator = "===================================================="
    new_line = "\n"
    print(separator)
    print(f"Build Step: {step}")
    print(separator)
    print(new_line)

if __name__ == "__main__":
    main(sys.argv[1:])
