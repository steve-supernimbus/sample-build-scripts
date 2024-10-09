import argparse
import os
import shutil

def main(game_override_path, engine_override_path):
    config_dir = os.path.join(os.getcwd(), "Config")
    print(f"Config Directory: {config_dir}")

    if game_override_path is not None:
        game_override(config_dir, game_override_path)

    if engine_override_path is not None:
        engine_override(config_dir, engine_override_path)

    print("Script ended successfully.")

def game_override(config_dir, game_override_path):
    print("Overriding Default Game ini file...")
    remove_ini_file(os.path.join(config_dir, "DefaultGame.ini"))
    copy_ini_file(game_override_path, config_dir, "DefaultGame.ini")

def engine_override(config_dir, engine_override_path):
    print("Overriding Default Engine ini file...")
    remove_ini_file(os.path.join(config_dir, "DefaultEngine.ini"))
    copy_ini_file(engine_override_path, config_dir, "DefaultEngine.ini")

def remove_ini_file(path):
    try:
        os.remove(path)
    except OSError as e:
        print(f"Error on deleting file: {e}")


def copy_ini_file(source, destination, filename):
    try:
        shutil.copy(source, destination)
        original_filename = os.path.basename(source)
        new_filepath = os.path.join(destination, filename)
        os.rename(os.path.join(destination, original_filename), new_filepath)
    except:
        print(f"Error on copying and renaming ini override file...")

def get_script_args():
    parser = argparse.ArgumentParser(description="ini override script")
    parser.add_argument("--game-override-path", default=None)
    parser.add_argument("--engine-override-path", default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_script_args()
    main(args.game_override_path, args.engine_override_path)
