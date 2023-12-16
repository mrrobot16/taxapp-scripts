# Example of ANSI escape codes in Python

# ANSI color codes
RED = "\033[31m"  # Red text
GREEN = "\033[32m"  # Green text
YELLOW = "\033[33m"  # Yellow text
BLUE = "\033[34m"  # Blue text
MAGENTA = "\033[35m"  # Magenta text
CYAN = "\033[36m"  # Cyan text
RESET = "\033[0m"  # Reset to default color

print(RED + "This is red text." + RESET)
print(GREEN + "This is green text." + RESET)
print(YELLOW + "This is yellow text." + RESET)
print(BLUE + "This is blue text." + RESET)
print(MAGENTA + "This is magenta text." + RESET)
print(CYAN + "This is cyan text." + RESET)
