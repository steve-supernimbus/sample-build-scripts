import argparse
import json
import subprocess
import sys
import time

TIMEOUT = 60 * 60 # 1 hour
MONITORING_INTERVAL = 60 * 2 # 2 minutes

def main(alias_id, fleet_id):
    total_time = 0
    while not fleet_ready_or_failed(fleet_id):
        if total_time > TIMEOUT:
            log_step("Update GameLift Alias timeout.")
            sys.exit(2)

        total_time += MONITORING_INTERVAL
        log_step(f"Sleeping for {MONITORING_INTERVAL} seconds.")
        log_step(f"{TIMEOUT - total_time} seconds until timeout.")
        time.sleep(MONITORING_INTERVAL)

    #update_gamelift_alias(alias_id, fleet_id)

def fleet_ready_or_failed(fleet_id):
    result = aws_cli(
        [
            "gamelift",
            "describe-fleet-location-attributes",
            "--fleet-id", fleet_id
        ]
    )

    result_json = json.loads(result.strip())
    attributes = result_json["LocationAttributes"]

    active_regions = 0
    error_in_region = False
    total_regions = len(attributes)

    for attribute in attributes:
        location_state = attribute["LocationState"]
        location = location_state["Location"]
        status = location_state["Status"]

        log_step(f"Location: {location} Status: {status}")
        if status == "ERROR":
            error_in_region = True

        if status == "ACTIVE":
            active_regions += 1

    if error_in_region:
        log_step("Fleet activation error.")
        sys.exit(2)

    return active_regions == total_regions

def update_gamelift_alias(alias_id, fleet_id):
    routing_strategy = {
        "Type": "SIMPLE",
        "FleetId": fleet_id
    }
    result = aws_cli(
        [
            "gamelift",
            "update-alias",
            "--alias-id", alias_id,
            "--routing-strategy", json.dumps(routing_strategy),
        ]
    )
    log_step(result)

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
            text = True,
            check = True,
            capture_output = True,
        ).stdout
    except:
        raise Exception("Aws command failed")

def get_script_args():
    parser = argparse.ArgumentParser(description="Update GameLift Alias Script")
    parser.add_argument("--fleet-id")
    parser.add_argument("--alias-id")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(
        args.alias_id,
        args.fleet_id
    )
