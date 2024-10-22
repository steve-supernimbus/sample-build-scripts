import argparse
import os
import subprocess
import shutil
import sys

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

    zip_dir = os.path.join(os.getcwd(), f"{mode}-zips")
    out_dir = os.path.join(os.getcwd(), f"{mode}-packaged")

    create_directory(zip_dir)
    create_directory(out_dir)

    if mode == "server":
        log_step("Build UE4 Server Target")
        cli(["ue4", "build", "Development", "Server"])
        log_step("Successfully built UE4 Server Target")

    build_project(mode, target, configuration, maps, out_dir)
    log_step("Finished build request.")

    compress_directory(out_dir, zip_dir)
    log_step(f"Finished compressing {out_dir} to {zip_dir}")

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

def create_mock_build(out_dir, mock_filename):
    mock_dir = os.path.join(out_dir, 'mock-build')
    create_directory(mock_dir)
    f = open(os.path.join(mock_dir, mock_filename), "w")
    f.write("This is a mock build file.")
    f.close()

def create_directory(dir_path):
    if os.path.exists(dir_path):
        log_step(f"Removing directory: {dir_path}")
        shutil.rmtree(dir_path)
    if not os.path.exists(dir_path):
        log_step(f"Creating directory: {dir_path}")
        os.makedirs(dir_path)

def compress_directory(out_dir, zip_dir):
    for dir in get_subdirectories(out_dir):
        zip_path(dir, os.path.join(os.getcwd(), zip_dir))

def get_subdirectories(root):
    sub_dirs = []
    for it in os.scandir(root):
        if it.is_dir():
            sub_dirs.append(it.path)
    return sub_dirs

def zip_path(source_dir, output_dir):
    zip_path = os.path.join(output_dir, f"{os.path.basename(source_dir)}.zip")
    print(f"Zipping {source_dir} to {zip_path}")
    cli(["7z", "a", zip_path, source_dir])

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
    parser.add_argument("--mode", default="")
    parser.add_argument("--target", default="Win64")
    parser.add_argument("--configuration", default="Development")
    parser.add_argument("--maps", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.pre_reqs, args.mode, args.target, args.configuration, args.maps)
