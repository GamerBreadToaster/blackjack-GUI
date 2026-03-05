import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Blackjack game arguments.")
parser.add_argument("--debug", "-d", action="store_true", help="Launch the game in debug mode")

# Parse the arguments
args, unknown = parser.parse_known_args()
DEBUG_MODE = args.debug

def log(*args_list, **kwargs):
    """Prints debug messages only if --debug is passed as an argument."""
    if DEBUG_MODE:
        print("[DEBUG]", *args_list, **kwargs)