import sys

def main(argv):
    log_step("Begin Building.")
    log_step("Generating mock build.")
    generate_mock_build()
    log_step("Finish Building.")

def generate_mock_build():
    f = open("./sample-build-file.txt", "w")
    f.write("Imagine I'm an Unreal Project Build.\n")
    f.close()

def log_step(step):
    separator = "===================================================="
    new_line = "\n"
    print(separator)
    print(f"Build Step: {step}")
    print(separator)
    print(new_line)

if __name__ == "__main__":
    main(sys.argv[1:])
