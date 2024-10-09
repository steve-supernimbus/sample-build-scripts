import argparse
import os
import subprocess

ZIP_DIR = os.path.join(os.getcwd(), "zips")
OUT_DIR = os.path.join(os.getcwd(), "packaged")
U_PROJECT_PATH = os.path.join(os.getcwd(), "ClonkBR.uproject")
BUILD_PARAMS = [
    "BuildCookRun",
    "-noP4",
    "-clientconfig=Development",
    "-serverconfig=Development",
    "-targetplatform=Android",
    "-platform=Android",
    "-cookflavor=ASTC",
    "-build",
    "-cook",
    "-stage",
    "-package",
    "-compile",
    "-archive",
    "-cookflavor=ASTC",
    "-pak",
    "-nodebuginfo",
    "-2017"
]

def main(pre_reqs, mode, target, configuration, maps):
    log_step(
        "Script Arguments",
        get_argument_message(pre_reqs, mode, target, configuration, maps)
    )

    if pre_reqs:
        build_pre_reqs(configuration)

    if mode != "server" and mode != "client":
        log_step("Finished build request.")
        return

    create_directory(ZIP_DIR)
    create_directory(OUT_DIR)

    if mode == "server":
        log_step("Build UE4 Server Target")
        cli(["ue4", "build", "Development", "Server"])
        log_step("Successfully built UE4 Server Target")

    build_project(mode, target, configuration, maps, OUT_DIR)
    log_step("Finished build request.")

def build_pre_reqs(configuration):
    log_step("Building Pre Reqs")
    cli(["ue4", "build-target", "UnrealEditor"])
    cli(["ue4", "build-target", "ShaderCompileWorker", configuration])
    cli(["ue4", "build-target", "UnrealLightmass", configuration])

def build_project(mode, target, configuration, maps, out_dir):
    log_step(
        "Building project with following params",
        f"Mode: {mode}, Target: {target}, Configuration: {configuration}, Map: {maps}, Directory: {out_dir}"
    )
    fullArgs = BUILD_PARAMS
    fullArgs += [f'-project="{U_PROJECT_PATH}"']
    fullArgs += [f"-map={maps}"]
    fullArgs += [f"-configuration={configuration}"]

    if mode == "client":
        fullArgs += [f"-targetplatform={target}"]
    else:
        fullArgs += ["-noclient"]

    if mode == "server":
        fullArgs += [f"-servertargetplatform={target}", "-server"]

    fullArgs += [f'-archivedirectory="{out_dir}"']

    cmd = ["ue4", "uat"] + fullArgs
    cli(cmd)

def create_directory(dir_path):
    log_step(f"Creating directory: {dir_path}")
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def cli(args):
    try:
        log_step(f"Making the following CLI call: {' '.join(args)}")
        return subprocess.call(args)
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
    parser.add_argument("--mode", default="")
    parser.add_argument("--target", default="Win64")
    parser.add_argument("--configuration", default="Development")
    parser.add_argument("--maps", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.pre_reqs, args.mode, args.target, args.configuration, args.maps)
