import os,sys,re
import subprocess
from config_local import *
countc=0
bloglocaladdress=config("bloglocaladdress","")
gitpass=config("gitpass", "123")
app=config("app","") 
def openurlinlocal(self, url):
        try:
            global bloglocaladdress,app                      
            file = url.replace("https://cybersecctf.github.io/blog", bloglocaladdress)
            with open(file, "r") as blog_file:
                content = blog_file.read()
                os.chdir(os.path.dirname(file))                    
                current_index = self.tab_widget.currentIndex()
                self.text_editors[current_index].setPlainText(content)
                
                self.file_names[current_index] = file  
        except Exception as e:
            print(str(e))
def replace_blog_path(link):
     old_path = "/home/solup/Desktop/blog"
     new_path = "https://cybersecctf.github.io/blog"
     updated_link = link.replace(old_path, new_path)
     return updated_link
def replace_github_path(link):

     old_path = "/home/solup/Desktop/blog/"
     new_path = "https://github.com/cybersecctf/blog/blob/main/"
     updated_link = link.replace(old_path, new_path)
     return updated_link
def run_shscript(self,file_name):
    current_widget = self.tab_widget.currentWidget()
    if current_widget:
        file_name = '/home/solup/Desktop/hack3/temp_script.sh'
        with open(file_name, 'w') as file:
            file.write(current_widget.text())
        
        if sys.platform == "win32":
            command = ["start", "cmd", "/k", f"python {file_name} & pause"]
        
        else:
            command = ["qterminal", "-e", "bash", "-c", f"sh {file_name}; read -p 'Press enter to continue...'"]
        
        try:
            subprocess.Popen(command)
        except Exception as e:
            self.command_output.append(f'Error: {str(e)}')
            self.command_output.setFixedHeight(int(self.command_output.document().size().height()) + 10)
def run_script(self):
    current_widget = self.tab_widget.currentWidget()
    if current_widget:
        file_name = '/home/solup/Desktop/hack3/temp_script.py'
        with open(file_name, 'w') as file:
            file.write(current_widget.text())
        
        if sys.platform == "win32":
            command = ["start", "cmd", "/k", f"python {file_name} & pause"]
        
        else:
            command = ["qterminal", "-e", "bash", "-c", f"python3 {file_name}; read -p 'Press enter to continue...'"]
        
        try:
            subprocess.Popen(command)
        except Exception as e:
            self.command_output.append(f'Error: {str(e)}')
            self.command_output.setFixedHeight(int(self.command_output.document().size().height()) + 10)
def extract_text_inside_pre(self, content):
        pre_pattern = r'<pre>(.*?)<\/pre>'
        match = re.search(pre_pattern, content, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return content
def run_python_code(self, code):
     try:
        global app          
        current_index = self.tab_widget.currentIndex()
      
        file = app+"/temp_code.py"  # Default temp file
        s=file        
        if s and s != "None":
            if s.endswith('.md'):
                # If it's a markdown file, create a new .py file with the same name
                file = s.replace('.md', '.py')
            else:
                # If it's any other text file, use it directly
                file = s

        if "<pre>" in code or not code.startswith("#python") or not code.startswith("import"):
            code = extract_text_inside_pre(self,code)
                           
        with open(file, "w") as f:
            f.write(code)

        print(file)
        subprocess.Popen(["qterminal", "-e", "python3", "-i", file])
        
     except Exception as e:
        print( f"Error running code: {e}")
def addimage(file):
       try:
        link=replace_blog_path(file); 

        s='<img src=" '+link+'" alt="ctf quetion image" width="500" height="600" class="inline"/>'            
        return s
       except Exception  as e:
            return "missn error:"+str(e)  
       return file    
def addlink(file):
       try: 
        link=replace_blog_path(file); 
        return  '<a href="'+link+'">link text</a>'           
       except Exception  as e:
            return "add link  error:"+str(e) 
def addlinkgithub(file):
       try: 
        link=replace_github_path(file); 
        return  '<a href="'+link+'">link text</a>'           
       except Exception  as e:
            return "add github link  error:"+str(e) 
def addmain():          
            return('if __name__ == "__main__" :')     
          
def run(s):
  if "$publish" in s:
       publish(s) 
  os.system(s)
def modifycode(codes):   
   if "import blog" in codes and not "sys.path.append" in codes:
        # Replace 'import blog' with the new lines of code
        new_lines = "import sys\nsys.path.append('/home/solup/Desktop/blog')  # This is an absolute path\nimport blog"
        codes = codes.replace('import blog', new_lines)
        return codes
   return codes
def publish(sr):
   global countc
   if "publish" in sr:
                          import pyperclip
                          s=config("gitpass1","123")
                          pyperclip.copy(s)
                          os.chdir("/home/solup/Desktop/blog")
                          p=sr.split()[2]
                          
                         # if countc==0: 
                          #   os.system("git checkout "+p)  
                          if countc==0: 
                           os.system("git add .")
                          s=sr.replace("$blog publish ","")
                          if s=="":
                              s=self.filename
                          if countc==1: 
                       
                           os.system("git commit -m "+p)
                          
                          if countc==2:
                           os.system("git push origin main")
                           print("pass is",s,"countc",countc)
                          countc+=1
                          if countc==3:
                                  countc=0
               
