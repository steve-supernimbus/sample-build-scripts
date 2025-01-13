import argparse
import subprocess

def main(s3_location, profile):
    log_step(generate_presigned_url(s3_location, profile))

def generate_presigned_url(remote_path, profile):
    log_step(f"Generating accelerated pre-signed url for {remote_path}")
    return aws_cli(
        [
            "s3",
            "presign",
            remote_path,
            "--expires-in=604800",
            "--endpoint-url=https://s3-accelerate.amazonaws.com",
            "--region=eu-west-1",
            f"--profile={profile}",
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

def log_step(step):
    separator = "===================================================="
    print(separator)
    print(f"Step: {step}")
    print(separator)
    print("\n")

def get_script_args():
    parser = argparse.ArgumentParser(description="Generate Accelerated URL")
    parser.add_argument("--s3-location")
    parser.add_argument("--profile", default="default")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.s3_location, args.profile)
