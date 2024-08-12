import re
import subprocess

def solve(command, search="DUCTF"):
    # Append commands to save output to temp.sh, make it executable, and run it
    full_command = f"{command} > temp.sh && chmod +x temp.sh && strings ./temp.sh"
    print(full_command)
    # Execute the full command and capture the output
    result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Combine stdout and stderr to cover all output
    combined_output = result.stdout + result.stderr

    # Debugging: Print the command output to verify
    print("Command output:")
    print(combined_output)

    # Search for the search string using regex in the command output
    search_pattern = re.compile(fr'{re.escape(search)}\{{[^\}}]+\}}')
    match = search_pattern.search(combined_output)

    if match:
        return match.group(0)
    else:
        return f"Flag containing '{search}' not found in the command output."

# Example usage
command = "curl -sL https://pastebin.com/raw/ysYcKmbu | base64 -d"
print(solve(command))
