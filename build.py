import argparse
import os
import subprocess

ZIP_DIR = os.path.join(os.getcwd(), "Zips")
OUT_DIR = os.path.join(os.getcwd(), "Packaged")

def main(pre_reqs, client, server, client_target, server_target, configuration, maps):
    log_step(
        "Script Arguments",
        get_argument_message(
            pre_reqs,
            client, server,
            client_target,
            server_target,
            configuration,
            maps
        )
    )

    if pre_reqs:
        build_pre_reqs(configuration)

    if client or server:
        create_zip_directory(ZIP_DIR)
        create_out_directory(OUT_DIR)

def build_project():
    log_step("Begin Building.", "")
    log_step("Finish Building.", "")

def build_pre_reqs(configuration):
    log_step("Building Pre Reqs", "")
    build_engine_editor()
    build_ue4_components(configuration)

def build_engine_editor():
    ue4_cli(["build-target", "UnrealEditor"])

def create_zip_directory(zip_dir):
    log_step(f"Creating zip directory: {zip_dir}")
    cli(f"mkdir {zip_dir}")

def create_out_directory(out_dir):
    log_step(f"Creating out directory: {out_dir}")
    cli(f"mkdir {out_dir}")

def build_ue4_components(configuration):
    build_engine_target("ShaderCompileWorker", configuration)
    build_engine_target("UnrealLightmass", configuration)

def build_engine_target(component, configuration):
    try:
        build_target = ["build-target", component, configuration]
        print(build_target)
        ue4_cli(build_target)
    except:
        raise Exception("Failed to build UE4")

def ue4_cli(args):
    failed_message = "ue4 cli command failed"
    try:
        result = cli(add_args(["ue4"], args))
        if result != 0:
            raise Exception(failed_message)
    except:
        raise Exception(failed_message)

def cli(args):
    try:
        print(f"cli: {subprocess.list2cmdline(args)}")
        return subprocess.call(args)
    except:
        raise Exception("cli call failed")

def add_args(default, args):
    if (args is None) or (len(args) < 1):
        return default
    return default + args

def log_step(step_name, step_output):
    separator = "===================================================="
    print(separator)
    print(f"Step Name: {step_name}")
    print(f"Step Output: {step_output}")
    print(separator)

def get_argument_message(pre_reqs, client, server, client_target, server_target, configuration, maps):
    return f"""pre-reqs: {pre_reqs},
client: {client},
server: {server},
client_target: {client_target},
server_target: {server_target},
configuration: {configuration}
maps: {maps}"""

def get_script_args():
    parser = argparse.ArgumentParser(description="Build Script")
    parser.add_argument("--pre-reqs", default=False)
    parser.add_argument("--client", default=False)
    parser.add_argument("--server", default=False)
    parser.add_argument("--client-target", default="Win64")
    parser.add_argument("--server-target", default="Win64")
    parser.add_argument("--configuration", default="Development")
    parser.add_argument("--maps", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.pre_reqs, args.client, args.server, args.client_target, args.server_target, args.configuration, args.maps)
