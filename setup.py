def get_user_input(prompt):
    return input(prompt)

def write_config_file(gitpass, file_history, bloglocaladdress, app):
    with open('config_local.py', 'w') as f:
        f.write(f"""
def config(val, default):
    try:
        return globals()[val]
    except KeyError:
        return default

def set_config():
    global gitpass, file_history, bloglocaladdress, app
    gitpass = '{gitpass}'
    file_history = '{file_history}'
    bloglocaladdress = '{bloglocaladdress}'
    app = '{app}'
set_config()
""")

def main():
    print("solveup editor beta  0.1 for run blog writeups easily")
    gitpass = get_user_input("Enter gitpass if you want publish in github: ")
    file_history = get_user_input("Enter file_history path: ")
    bloglocaladdress = get_user_input("Enter bloglocaladdress path: ")
    app = get_user_input("Enter app path: ")
    shfile=get_user_input("Enter temp.sh file path for run sh files: ")
    write_config_file(gitpass, file_history, bloglocaladdress, app)
if __name__ == "__main__":
    main()