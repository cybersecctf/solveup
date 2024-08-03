
def config(val, default):
    try:
        return globals()[val]
    except KeyError:
        return default

def set_config():
    global gitpass, file_history, bloglocaladdress, app,shfile
    gitpass = '11w'#add your own if you want publish in github
    file_history = '/home/user/Desktop/hack3/file_history.json'#add your own file_history.json
    bloglocaladdress = '/home/user/Desktop/blog' #add your clone location
    app = '/home/user/Desktop/solveupeditor' #addyour solveup editor path
    shfile="temp.sh"#add your complete sh file if you run sh file
set_config()
