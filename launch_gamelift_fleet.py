import argparse
import json
import os
import subprocess
import sys
import time

FLEET_TYPE = "SPOT"
BUILD_SLEEP_TIME = 10
PROJECT_NAME = "ClonkBR"
CONCURRENT_EXECUTIONS = 3
INSTANCE_TYPE = "c4.large"
LAUNCH_PATH_ROOT = "C:\\game\\"
RESULT_FILE_NAME = "result.json"
OPERATING_SYSTEM = "WINDOWS_2016"
GAME_SESSION_ACTIVATION_TIMEOUT = 600
PORTS = [
    {
        "ToPort": 7796,
        "FromPort": 7777,
        "Protocol": "UDP",
        "IpRange": "0.0.0.0/0",
    },
    {
        "ToPort": 3389,
        "FromPort": 3389,
        "Protocol": "TCP",
        "IpRange": "0.0.0.0/0",
    },
]
LOCATIONS = [
    {"Location": "eu-west-1"},
    #{"Location": "us-east-1"},
]

def main(build_name, build_version, build_path, fleet_name, aws_region):
    build_id = upload_build(build_name, build_version, build_path, aws_region)
    log_step(f"Build ID: {build_id}")

    while not build_ready_or_failed(build_id):
        log_step(f"Waiting for build to be ready. Sleeping for {BUILD_SLEEP_TIME} seconds.")
        time.sleep(BUILD_SLEEP_TIME)

    launch_path = get_launch_path(build_path)
    log_step(f"Launch Path: {launch_path}")

    fleet_id = create_fleet(
        fleet_name, build_id, launch_path, PROJECT_NAME, aws_region, "production"
    )
    log_step(f"Received Fleet ID: {fleet_id}")

    write_file(
        os.path.join(os.getcwd(), RESULT_FILE_NAME), {"fleetId": fleet_id}
    )

def get_launch_path(build_path):
    files = os.listdir(build_path)
    exe_files = [file for file in files if file.endswith(".exe")]
    executable_name = os.path.splitext(exe_files[0])[0]
    return f"{LAUNCH_PATH_ROOT}{executable_name}.exe"

def upload_build(name, version, path, region):
    result = aws_cli(
        [
            "gamelift",
            "upload-build",
            "--name", name,
            "--region", region,
            "--build-root", path,
            "--build-version", version,
            "--operating-system", OPERATING_SYSTEM,
        ]
    )
    return extract_build_id(result)

def build_ready_or_failed(build_id):
    result = aws_cli(["gamelift", "describe-build", "--build-id", build_id])
    json_result = json.loads(result)
    status = json_result["Build"]["Status"]

    if status == "ERROR":
        print("Build Uploaded with status: ERROR")
        sys.exit(2)

    return status == "READY"

def create_fleet(name, build_id, launch_path, project_name, region, environment):
    tags = [
        {"Key": "dev", "Value": "Jenkins"},
        {"Key": "game", "Value": project_name},
        {"Key": "env", "Value": environment},
    ]
    result = aws_cli(
        [
            "gamelift",
            "create-fleet",
            "--name", name,
            "--region", region,
            "--build-id", build_id,
            "--fleet-type", FLEET_TYPE,
            "--tags", json.dumps(tags),
            "--ec2-instance-type", INSTANCE_TYPE,
            "--locations", json.dumps(LOCATIONS),
            "--ec2-inbound-permissions", json.dumps(PORTS),
            "--runtime-configuration", get_runtime_configuration(launch_path),
            "--description", f"Fleet {name} from {build_id} created from Jenkins.",
        ]
    )
    json_result = json.loads(result)
    log_step(f'Fleet Attributes: {json_result["FleetAttributes"]}')
    return json_result["FleetAttributes"]["FleetId"]

def get_runtime_configuration(launch_path):
    return json.dumps(
        {
            "ServerProcesses": [
                {
                    "LaunchPath": launch_path,
                    "ConcurrentExecutions": CONCURRENT_EXECUTIONS,
                }
            ],
            "GameSessionActivationTimeoutSeconds": GAME_SESSION_ACTIVATION_TIMEOUT,
        }
    )

def write_file(file_path, content):
    with open(file_path, "w") as file:
        json.dump(content, file)

def extract_build_id(output):
    parts = output.split("Build ID:")
    return parts[1].strip()

def log_step(step):
    separator = "===================================================="
    print(separator)
    print(f"Step: {step}")
    print(separator)
    print("\n")

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

def get_script_args():
    parser = argparse.ArgumentParser(description="Launch GameLift Script")
    parser.add_argument("--build-name", default="test-build")
    parser.add_argument("--fleet-name", default="test-fleet")
    parser.add_argument("--build-version", default="0.0.1")
    parser.add_argument("--build-path", default="..\\project\\Packaged\\WindowsServer")
    parser.add_argument("--aws-region", default="eu-west-1")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(
        args.build_name,
        args.build_version,
        args.build_path,
        args.fleet_name,
        args.aws_region
    )
