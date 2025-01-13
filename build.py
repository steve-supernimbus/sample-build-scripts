import argparse
import os
import subprocess
import shutil

U_PROJECT_PATH = os.path.join(os.getcwd(), "ClonkBR.uproject")
BUILD_PARAMS = [
    "BuildCookRun",
    "-noP4",
    "-build",
    "-cook",
    "-stage",
    "-package",
    "-compile",
    "-archive",
    "-pak",
    "-nodebuginfo",
    "-2017"
]

def main(pre_reqs, mode, target, cookflavor, configuration, maps):
    log_step(
        "Script Arguments",
        get_argument_message(pre_reqs, mode, target, configuration, maps)
    )

    if pre_reqs:
        build_pre_reqs()

    if mode != "server" and mode != "client":
        log_step("Finished build request.")
        return

    out_dir = os.path.join(os.getcwd(), f"{mode}-build")
    create_directory(out_dir)

    if mode == "server":
        log_step("Build UE4 Server Target")
        cli(["ue4", "build", "Development", "Server"])
        log_step("Successfully built UE4 Server Target")

    build_project(mode, target, cookflavor, configuration, maps, out_dir)
    log_step("Finished build request.")

def build_pre_reqs():
    log_step("Building Pre Reqs")
    cli(["ue4", "build-target", "UnrealEditor"])
    cli(["ue4", "build-target", "UnrealLightmass", "Development"])
    cli(["ue4", "build-target", "ShaderCompileWorker", "Development"])

def build_project(mode, target, cookflavor, configuration, maps, out_dir):
    log_step(
        "Building project with following params",
        f"Mode: {mode}, Target: {target}, Configuration: {configuration}, Map: {maps}, Target Directory: {out_dir}"
    )
    fullArgs = BUILD_PARAMS
    fullArgs += [
        f"-platform={target}",
        f'-project="{U_PROJECT_PATH}"',
        f"-clientconfig={configuration}",
        f"-serverconfig={configuration}",
        f'-archivedirectory="{out_dir}"',
        f"-configuration={configuration}",
    ]

    if cookflavor is not None:
        fullArgs += [
            f"-cookflavor={cookflavor}",
        ]

    if maps is not None:
        fullArgs += [
            f"-map={maps}",
        ]

    if mode == "client":
        fullArgs += [
            f"-targetplatform={target}",
        ]
    else:
        fullArgs += [
            "-server",
            "-noclient",
            f"-servertargetplatform={target}",
        ]

    cli(["ue4", "uat"] + fullArgs)

def create_directory(dir_path):
    if os.path.exists(dir_path):
        log_step(f"Removing directory: {dir_path}")
        shutil.rmtree(dir_path)
    if not os.path.exists(dir_path):
        log_step(f"Creating directory: {dir_path}")
        os.makedirs(dir_path)

def cli(args):
    try:
        log_step(f"Making the following CLI call: {' '.join(args)}")
        return subprocess.run(args, check=True)
    except:
        raise Exception("cli call failed")

def log_step(step_name, step_output="No Output"):
    separator = "===================================================="
    print(separator)
    print(step_name)
    print(f"Step Output: {step_output}")
    print(separator)

def get_argument_message(pre_reqs, mode, target, configuration, maps):
    return f"""pre-reqs: {pre_reqs},
mode: {mode},
target: {target},
configuration: {configuration}
maps: {maps}"""

def get_script_args():
    parser = argparse.ArgumentParser(description="Build Script")
    parser.add_argument("--pre-reqs", default=False)
    parser.add_argument("--mode", default="client")
    parser.add_argument("--target", default="Win64")
    parser.add_argument("--cookflavor", default="ASTC")
    parser.add_argument("--configuration", default="Development")
    parser.add_argument("--maps", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.pre_reqs, args.mode, args.target, args.cookflavor, args.configuration, args.maps)
