import json
import subprocess

REGIONS = [
    'eu-west-1',
    'us-east-1',
]
ACCOUNT_ID = '927704468320'
TAG_TO_DELETE = 'development'

def main():
    for region in REGIONS:
        fleet_ids = get_gamelift_fleet_list(region)
        log_step(fleet_ids)

        for fleet_id in fleet_ids:
            if has_alias_attached(fleet_id, region):
                log_step(f"{fleet_id} in {region} has an attached alias, skipping.")
                continue

            tags = get_gamelift_fleet_tags(fleet_id, region)
            log_step(tags)

            if not should_delete_fleet(tags):
                continue

            log_step(f"Will attempt to delete {fleet_id} in {region}")
            delete_gamelift_fleet(fleet_id, region)

def has_alias_attached(fleet_id, region):
    result = aws_cli(
        [
            'gamelift',
            'list-aliases',
            f'--region={region}',
            f"--query=Aliases[?RoutingStrategy.FleetId=='{fleet_id}']"
        ]
    )
    json_result = json.loads(result)

    if not json_result:
        return False
    return True

def should_delete_fleet(tags):
    return any(tag['Value'] == TAG_TO_DELETE for tag in tags) and any(tag['Value'] == 'Jenkins' for tag in tags)

def get_gamelift_fleet_list(region):
    result = aws_cli(
        [
            'gamelift',
            'list-fleets',
            f'--region={region}',
        ]
    )
    log_step(result)
    json_result = json.loads(result)
    return json_result["FleetIds"]

def get_gamelift_fleet_tags(fleet_id, region):
    result = aws_cli(
        [
            'gamelift',
            'list-tags-for-resource',
            f'--region={region}',
            f'--resource-arn={get_fleet_arn(fleet_id, region)}',
        ]
    )
    json_result = json.loads(result)
    return json_result["Tags"]

def get_fleet_arn(fleet_id, region):
    return f"arn:aws:gamelift:{region}:{ACCOUNT_ID}:fleet/{fleet_id}"

def delete_gamelift_fleet(fleet_id, region):
    aws_cli(
        [
            'gamelift',
            'delete-fleet',
            f'--region={region}',
            f'--fleet-id={fleet_id}'
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
    new_line = "\n"
    print(separator)
    print(step)
    print(separator)
    print(new_line)

if __name__ == "__main__":
    main()
