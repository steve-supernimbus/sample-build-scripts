import sys

def main(argv):
    logStep("Begin Building...")
    logStep("Finish Building...")

def logStep(step):
    separator = "===================================================="
    new_line = "\n"
    print(separator)
    print(f"Build Step: {step}")
    print(separator)
    print(new_line)

if __name__ == "__main__":
    main(sys.argv[1:])
