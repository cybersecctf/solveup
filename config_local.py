def config(val, default):
    try:
             
        return globals()[val]
    except KeyError:
        return default

def set_config():
    global gitpass,file_history,bloglocaladdress,app
    gitpass=''
    file_history="/home/solup/Desktop/hack3/file_history.json"
    bloglocaladdress="/home/solup/Desktop/blog"
    app="/home/solup/Desktop/hack3"   
set_config()  
 
