import argparse
import json
import os
import subprocess
import sys
import time

SLEEP_TIME = 10
FLEET_TYPE = "SPOT"
CONCERENT_EXECUTIONS = 3
INSTANCE_TYPE = "c4.large"
OPERATING_SYSTEM = "WINDOWS_2016"
GAME_SESSION_ACTIVATION_TIMEOUT = 600
PROJECT_NAME = "GameliftMultiplayerStarter"

PORTS = json.dumps(
    [
        {
            "FromPort": 7777,
            "ToPort": 7777,
            "IpRange": "0.0.0.0/0",
            "Protocol": "UDP",
        },
        {
            "FromPort": 3389,
            "ToPort": 3389,
            "IpRange": "0.0.0.0/0",
            "Protocol": "TCP",
        },
    ]
)

LOCATIONS = json.dumps(
    [
        {"Location": "eu-west-1"},
        #{"Location": "us-west-1"},
        #{"Location": "us-east-1"},
    ]
)

def main(build_name, build_version, build_path, fleet_name, aws_region):
    launch_path = get_launch_path(PROJECT_NAME, build_path)
    log_step(f"Launch Path: {launch_path}")

    build_id = upload_build(build_name, build_version, build_path, aws_region)
    log_step(f"Build ID: {build_id}")

    while not build_ready_or_failed(build_id):
        log_step(f"Waiting for build to be ready. Sleeping for {SLEEP_TIME} seconds.")
        time.sleep(SLEEP_TIME)

    fleet_id = create_fleet(
        fleet_name, build_id, launch_path, PROJECT_NAME, "production"
    )

    log_step(f"Received Fleet ID: {fleet_id}")

    write_file(
        os.path.join(os.getcwd(), "result.json"), {"fleetId": fleet_id}
    )

def get_launch_path(project_name, build_path):
    launch_path_start = f"{project_name}\Binaries\Win64"
    exe_path = os.path.join(build_path, launch_path_start)
    files = os.listdir(exe_path)
    exe_files = [file for file in files if file.endswith(".exe")]
    executable_name = os.path.splitext(exe_files[0])[0]
    return f"{launch_path_start}\{executable_name}.exe"

def upload_build(name, version, path, region):
    result = aws_cli(
        [
            "gamelift",
            "upload-build",
            "--name",
            name,
            "--build-version",
            version,
            "--build-root",
            path,
            "--region",
            region,
            "--operating-system",
            OPERATING_SYSTEM,
        ]
    )
    return extract_build_id(result)

def build_ready_or_failed(build_id):
    json = aws_cli(["gamelift", "describe-build", "--build-id", build_id], True)
    status = json["Build"]["Status"]

    if status == "ERROR":
        print("Build Uploaded with status: ERROR")
        sys.exit(2)

    return status == "READY"

def create_fleet(name, build_id, launch_path, project_name, environment):
    description = f"Fleet {name} from build {build_id} created from Jenkins"
    tags = json.dumps(
        [
            {"Key": "dev", "Value": "Jenkins"},
            {"Key": "game", "Value": project_name},
            {"Key": "env", "Value": environment},
        ]
    )
    result = aws_cli(
        [
            "gamelift",
            "create-fleet",
            "--name",
            name,
            "--description",
            description,
            "--build-id",
            build_id,
            "--locations",
            LOCATIONS,
            "--tags",
            tags,
            "--ec2-instance-type",
            INSTANCE_TYPE,
            "--fleet-type",
            FLEET_TYPE,
            "--ec2-inbound-permissions",
            PORTS,
            "--runtime-configuration",
            get_runtime_configuration(launch_path),
        ],
        True,
    )
    log_step(f"Created Fleet: {result}")
    return result["FleetAttributes"]["FleetId"]

def get_runtime_configuration(launch_path):
    return json.dumps(
        {
            "ServerProcesses": [
                {
                    "LaunchPath": f"C:\game\{launch_path}",
                    "ConcurrentExecutions": CONCERENT_EXECUTIONS,
                }
            ],
            "GameSessionActivationTimeoutSeconds": GAME_SESSION_ACTIVATION_TIMEOUT,
        }
    )

def write_file(file_path, content):
    with open(file_path, "w") as file:
        json.dump(content, file)

def extract_build_id(output):
    parts = output.split(":")
    return parts[1].strip()

def log_step(step):
    separator = "===================================================="
    new_line = "\n"
    print(separator)
    print(f"Step: {step}")
    print(separator)
    print(new_line)

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
    parser.add_argument("--build-name")
    parser.add_argument("--build-path")
    parser.add_argument("--build-version")
    parser.add_argument("--fleet-name")
    parser.add_argument("--aws-region", default=False)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.build_name, args.build_version, args.build_path, args.fleet_name, args.aws_region)
