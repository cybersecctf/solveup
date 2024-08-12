import sys
import subprocess
import os
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QAction, QFileDialog, QInputDialog, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QSizePolicy, QCompleter
from PyQt5.QtGui import QColor, QFont
from PyQt5.Qsci import QsciScintilla, QsciLexerPython
from config_local import *
from actions import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from Timer import *
import pandas as pd
import json
import sys
sys.path.append('/home/solup/Desktop/blog')  # This is an absolute path
import blog
import requests 
import webbrowser
       
current_file=""
bloglocaladdress = config("bloglocaladdress", "")
history = config("history", "")
gitpass = config("gitpass", "123")
apps = config("app", "")
solveups = [""] * 10000
filenames = [""] * 10000
countc=0
findterm="" 
print("start hack3.sh")
class TextEditor(QsciScintilla):
    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)
        
        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)
        
        # Set the lexer
        self.lexer = QsciLexerPython()
        self.lexer.setDefaultFont(font)
        self.setLexer(self.lexer)
        
        # Set the margin width
        self.setMarginsForegroundColor(QColor('#cccccc'))
        self.setMarginsBackgroundColor(QColor('#333333'))
        self.setMarginWidth(0, '00000')
        self.setMarginLineNumbers(0, True)
        
        # Brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        
        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor('#ffe4e4'))
        
        # Enable folding
        self.setFolding(QsciScintilla.BoxedTreeFoldStyle)
        
        # Enable autocompletion
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(True)
        self.setAutoCompletionThreshold(1)
        
        # Set other properties
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setIndentationGuides(True)
        self.setIndentationGuidesForegroundColor(QColor('#008888'))
        self.set_dark_mode()     
    def set_dark_mode(self):
        # Background and foreground colors for dark mode
        self.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        self.setCaretLineBackgroundColor(QColor('#2d2d2d'))
        self.setMarginsBackgroundColor(QColor('#1e1e1e'))
        self.setMarginsForegroundColor(QColor('#858585'))
        self.setMarginsBackgroundColor(QColor('#1e1e1e'))
        self.SendScintilla(QsciScintilla.SCI_STYLESETBACK, QsciScintilla.STYLE_DEFAULT, QColor('#1e1e1e').rgb())
        self.SendScintilla(QsciScintilla.SCI_STYLESETFORE, QsciScintilla.STYLE_DEFAULT, QColor('#d4d4d4').rgb())
        
        # Set syntax highlighting colors
        lexer = self.lexer
        if lexer:
            lexer.setPaper(QColor('#1e1e1e'))
            lexer.setColor(QColor('#d4d4d4'))  # Default text color
            lexer.setColor(QColor('#569cd6'), QsciLexerPython.Keyword)  # Keywords
            lexer.setColor(QColor('#dcdcaa'), QsciLexerPython.DoubleQuotedString)  # Double-quoted strings
            lexer.setColor(QColor('#dcdcaa'), QsciLexerPython.SingleQuotedString)  # Single-quoted strings
            lexer.setColor(QColor('#4ec9b0'), QsciLexerPython.Comment)  # Comments
            lexer.setColor(QColor('#9cdcfe'), QsciLexerPython.ClassName)  # Class names
            lexer.setColor(QColor('#4fc1ff'), QsciLexerPython.FunctionMethodName)  # Function names
            lexer.setColor(QColor('#c586c0'), QsciLexerPython.Number)  # Numbers
            lexer.setColor(QColor('#ce9178'), QsciLexerPython.Operator)  # Operators

class TabbedEditor(QMainWindow):
    def __init__(self, initial_file=None):
        super().__init__()
        
        self.initUI()
        
        if initial_file:
            self.open_file(initial_file)
        
    def initUI(self):
        global  filenames,current
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
       
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        self.new_tab()
        
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        open_recent = menubar.addMenu('Open Recent')
        s=self.read_history(10)
        s = pd.Series(s).drop_duplicates().tolist()
         
      
        i=0
        open_rect=[""]*15
        try:
         if len(s)>0:
          for i, x in enumerate(s):
           x=x[:-1]
           open_act = QAction(x, self)
           open_act.triggered.connect(lambda checked, filename=x: self.open_file(filename))
           open_recent.addAction(open_act)
             
        except Exception as e:
               pass
        new_act = QAction('New', self)
        new_act.triggered.connect(self.new_tab)
        file_menu.addAction(new_act)
        
        open_act = QAction('Open', self)
        open_act.triggered.connect(lambda: self.open_file())
        file_menu.addAction(open_act)
        
        save_act = QAction('Save', self)
        save_act.triggered.connect(self.save_file)
        file_menu.addAction(save_act)
        
        save_as_act = QAction('Save As', self)
        save_as_act.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_act)

        input_text_act = QAction('Input Text', self)
        input_text_act.triggered.connect(self.input_text)
        file_menu.addAction(input_text_act)
                    
        run_script_act = QAction('Run Script', self)
        run_script_act.triggered.connect(self.run_script)
        file_menu.addAction(run_script_act)
        findnext = QAction('find next', self)
        findnext.triggered.connect(self.find_next)
        file_menu.addAction(findnext)
        dark_mode_act = QAction('Toggle Dark Mode', self)
        dark_mode_act.triggered.connect(self.toggle_dark_mode)
        file_menu.addAction(dark_mode_act)

        # Layout for the status bar and command execution
        layout = QVBoxLayout()

        # Command input
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText('Enter command and press Enter...')
        self.command_input.setFixedHeight(30)  # Set the height for the input line
        self.command_input.returnPressed.connect(self.run_command)
        
        # Command output display
        self.command_output = QTextEdit(self)
        self.command_output.setReadOnly(True)
        self.command_output.setFixedHeight(30)  # Initially set the same height as input line
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.command_input)
        layout.addWidget(self.command_output)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Command list for auto-completion
        self.command_list = ['ls', 'cd', 'mkdir', 'rm', 'touch', 'echo', 'cat', 'pwd', 'chmod', 'chown', 'cp', 'mv', 'grep', 'find', 'ps', 'kill', 'top', 'df', 'du', 'tar', 'zip', 'unzip']
        
        # Set up the completer
        self.completer = QCompleter(self.command_list, self)
        self.completer.setCaseSensitivity(False)
        self.command_input.setCompleter(self.completer)
        
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Sol Up')
        self.toggle_dark_mode()
        self.show()
   
    def search_blog(self, term):
        global solveups, bloglocaladdress
        solveups = []
        blog_file_path =  "/home/solup/Desktop/blog/Ai"
        try:
            if not os.path.exists(blog_file_path):
                print(self, "Warning", f"File not found: {blog_file_path}")
                return
            with open(blog_file_path, "r") as blog_file:
                lines = blog_file.readlines()
                for line in lines:
                    s = line.split(",")
                    if term in s[0] and line != "":
                        solveups.append(s[1].strip())
                self.completer = QCompleter(solveups, self)
                self.completer.setCaseSensitivity(False)
                self.command_input.setCompleter(self.completer)
            print(self, "No Matches", f"No matches found for term: {term}")
        except Exception as e:
            print(self, "Error", f"Error searching blog: {e}")

    def new_tab(self):
        new_editor = TextEditor()
        index = self.tab_widget.addTab(new_editor, 'Untitled')
        self.tab_widget.setCurrentIndex(index)
    def on_tab_changed(self):
        index = self.tab_widget.currentIndex()
        file_name = filenames[index]
        self.setWindowTitle('Sol Up - '+filenames[index])
    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)
    def select_file(self,title="open file"):
        global current_file ,filenames    
        try:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getOpenFileName(self, title, "", "All Files (*);;Python Files (*.py)", options=options)
            return file_name
        except Exception as e:
             print(str(e))
             return "" 
    def select_folder(self, title="Select Folder"):
     try:
        options = QFileDialog.Options()
        folder_name = QFileDialog.getExistingDirectory(self, title, "", options=options)
        return folder_name
     except Exception as e:
        print(f"error select path :{str(e)}")
        return ""
          
    def open_file(self, file_name=""):
        global current_file ,filenames    
        try:
            options = QFileDialog.Options()
            if not file_name :
                file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
               
            if file_name:
                with open(file_name, 'r') as file: 
                    content = file.read()
                    dir_path = os.path.dirname(os.path.realpath(file_name))                          
                    os.chdir(dir_path)  
                    self.write_history(file_name)           
                new_editor = TextEditor()
                new_editor.setText(content)
                index = self.tab_widget.addTab(new_editor, file_name.split('/')[-1])
                filenames[index]=file_name 
                self.tab_widget.setCurrentIndex(index)
        except Exception as e:
            print(f"Error in open_file: {str(e)}")
    def read_file(self, file_name=""):
        global current_file ,filenames    
        try:
            options = QFileDialog.Options()
            if not file_name :
                file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Python Files (*.py)", options=options)
               
            if file_name:
                with open(file_name, 'r') as file:
                    content = file.read()
                return content
        except Exception as e:
            return f"Error in open_file: {str(e)}"
    def save_file(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            index = self.tab_widget.currentIndex()
            file_name = filenames[index]
            if file_name == 'Untitled':
                self.save_as_file()
            else:
                with open(file_name, 'w') as file:
                    file.write(current_widget.text())
    def read_history(self,last=10):
        try:
           s=[]
           history="/home/solup/Desktop/hack3/file_history.json" 
            
           with open(history,"r") as f:
               s=f.readlines()
          
           if len(s)>last:
            return s[-last:]
           else:
             return s  
        except Exception as e:
            return f"error write in {history}: {str(e)}"
   

    def write_history1(self, content):
     try:
        history = "/home/solup/Desktop/hack3/file_history.json"

        # Read existing data or create an empty DataFrame
        try:
            with open(history, "r") as json_file:
                data = json.load(json_file)
                df = pd.DataFrame(data)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["file_path"])

        # Append the new content to the DataFrame
        df = df.append({"file_path": content}, ignore_index=True)

        # Make the DataFrame unique (remove duplicates)
        df.drop_duplicates(subset=["file_path"], inplace=True)

        # Write the unique data back to file_history.json
        with open(history, "w") as json_file:
            json.dump(df.to_dict(orient="records"), json_file, indent=4)

        print("File history updated successfully!")
     except Exception as e:
        print(f"Error writing to {history}: {str(e)}")

    def write_history(self,content):
        try:
           history="/home/solup/Desktop/hack3/file_history.json" 
        
           with open(history,"a") as f:
                f.write(content+"\n")
        except Exception as e:
            print(f"error write in {history}: {str(e)}")                    
    def save_as_file(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*);;Python Files (*.py)", options=options)
            if file_name:
                with open(file_name, 'w') as file:
                    file.write(current_widget.text())
                current_index = self.tab_widget.currentIndex()
            
                self.tab_widget.setTabText(current_index, file_name.split('/')[-1])

    def input_text(self):
        text, ok = QInputDialog.getText(self, 'Input Text', 'Enter text:')
        if ok and text:
            current_widget = self.tab_widget.currentWidget()
            if current_widget:
                current_widget.insert(text)
    def extract_text_inside_pre(self, content):
        pre_pattern = r'<pre>(.*?)<\/pre>'
        match = re.search(pre_pattern, content, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return content
    def run_python_code(self, code):
     try:
        global apps,filenames     
        file=""     
        current_index = self.tab_widget.currentIndex()
        file = filenames[current_index]
        if  file!="":
         dir_path = os.path.dirname(os.path.realpath(file))                          
         os.chdir(dir_path) 
        else: 
         file = apps+"/temp.py"  # Default temp file
        

        if file and file != "None":
            if file.endswith('.md'):
                # If it's a markdown file, create a new .py file with the same name
                file = file.replace('.md', '.py')
          

        if "<pre>" in code or not code.startswith("#python") or not code.startswith("import"):
            code = self.extract_text_inside_pre(code)
                           
        with open(file, "w") as f:
            f.write(code)

        # Determine the command based on the operating system
        if sys.platform == "win32":
            command = ["start", "cmd", "/k", f"python {file}"]
        elif sys.platform == "darwin":
            command = ["osascript", "-e", f'tell app "Terminal" to do script "python3 {file}"']
        else:
          subprocess.Popen(["konsole", "-e", "python3", "-i", file])
        
     except Exception as e:
        print(self, "Error", f"Error running code: {e}")
    def run_script1(self):
        s = self.file_names.get(current_index)
        file = app+"/temp_code.py"  # Default temp file 
        current_widget = self.tab_widget.currentWidget()
        code=current_widget.text()                      
        if "<pre>" in code or not code.startswith("#python") or not code.startswith("import"):
            code = self.extract_text_inside_pre(code)
                           
        with open(file, "w") as f:
            f.write(code)
        if s and s != "None":
            if s.endswith('.md'):
                # If it's a markdown file, create a new .py file with the same name
                file = s.replace('.md', '.py')
            else:
                # If it's any other text file, use it directly
                file = s  
        # Determine the command based on the operating system
        if sys.platform == "win32":
            command = ["start", "cmd", "/k", f"python {file}"]
        elif sys.platform == "darwin":
            command = ["osascript", "-e", f'tell app "Terminal" to do script "python3 {file}"']
        else:
          subprocess.Popen(["konsole", "-e", "python3", "-i", file])  
    def run_script(self):
        current_widget = self.tab_widget.currentWidget()
        file_name = self.tab_widget.tabText(current_index)
        dir_path = os.path.dirname(os.path.realpath(file_name))                          
        os.chdir(dir_path) 
        if current_widget:
            script_content = current_widget.text()
            try:
                process = subprocess.Popen(['python', '-c', script_content], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if stdout:
                    self.command_output.append(stdout.decode())
                if stderr:
                    self.command_output.append(stderr.decode())
                self.command_output.setFixedHeight(int(self.command_output.document().size().height()) + 10)
            except Exception as e:
                self.command_output.append(f'Error: {str(e)}')
                self.command_output.setFixedHeight(int(self.command_output.document().size().height()) + 10)
    def check_network(self,url="https://www.github.com"):
      try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
      except requests.RequestException:
        return False 
    def goto_line(self, line_number):
        try:
            line_number = int(line_number)
            current_widget = self.tab_widget.currentWidget()
            
            # Move the cursor to the specified line number
            current_widget.setCursorPosition(line_number - 1, 0)
            #current_widget.setFocus()
            
            # Get the position of the cursor in the widget coordinates
            start_pos = current_widget.SendScintilla(QsciScintilla.SCI_POSITIONFROMLINE, line_number - 1)
            cursor_x = current_widget.SendScintilla(QsciScintilla.SCI_POINTXFROMPOSITION, 0, start_pos)
            cursor_y = current_widget.SendScintilla(QsciScintilla.SCI_POINTYFROMPOSITION, 0, start_pos)
            
            # Map the widget coordinates to the global screen coordinates
            global_pos = current_widget.mapToGlobal(QPoint(cursor_x, cursor_y))
            
            # Move the mouse cursor to the global position
            QCursor.setPos(global_pos)
        except ValueError:
            print("Invalid line number.")
    def runsh(self,file_path, search=""):
     if not os.path.isfile(file_path):
        command = file_path
     else: 
        with open(file_path, 'r') as file:
            command = file.read().strip()
     shfile="/home/solup/Desktop/hack3/temp.sh"
     full_command = f"sudo {command} > {shfile} && chmod +x {shfile} && strings {shfile}"
    
     try:
        result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
        combined_output = result.stdout + result.stderr
     except subprocess.TimeoutExpired:
        combined_output = "Command timed out after 15 seconds."
     except subprocess.CalledProcessError as e:
        combined_output = e.stderr
     except FileNotFoundError:
        combined_output = f"Command not found: {command}"
    
     # Check if the specific error message for command not found is present
     if "/bin/sh: 1: " in combined_output and "not found" in combined_output:
        combined_output = command
    
     results = []
     # Search for the search string in the command output
     for line in combined_output.splitlines():
        if search in line:
            results.append(line)
    
     # If no results found and the file exists, process the file content itself
     if len(results) == 0 and os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
        for line in file_content.splitlines():
            if search in line:
                results.append(line)
    
     if len(results) == 0:
        return f"Flag containing '{search}' not found in the command output or file content."
     else:
        return "\n".join(results)   
    def run_command(self):
        command = self.command_input.text()
        current_index = self.tab_widget.currentIndex()
        if command:
            try:
                if os.path.exists(command):
                    self.open_file(command)
                if command.startswith("http"):
                    local_file_path = command.replace("https://cybersecctf.github.io/blog", bloglocaladdress)
                    if os.path.exists(local_file_path):
                        self.open_file(local_file_path) 
                        return
                elif command.startswith("$$v"):
                     args=command.replace("$$v","").split(" ")
                     args=" ".join(args)  
                     os.system("python writeup1.py "+args)
                elif "$blog publish" in command:
                   try:             
                    global countc
                    import pyperclip
                    self.check_network()
                    s =gitpass
                    print(s) 
                    pyperclip.copy(s)
                    os.chdir(bloglocaladdress)
                    p = command.split()[2]
                    if countc==0: 
                           os.system("git add .")
                           s=command.replace("$blog publish ","")
                           if s=="":
                              s=self.filename
                          
                    if countc==1:    
                           os.system("git commit -m "+p)         
                    if countc==2:
                           os.system("git push origin main")
                       
                    if countc==3:
                     countc=0  
                    countc+=1
                   except Exception as e:
                     countc=0
                     print(f"Error: {e}")
                elif command == "clear":
                    self.command_output.setText("")
                    self.command_output.setFixedHeight(30)
                    self.setGeometry(100, 100, 800, 600)
                    return
                elif command == "$$main":
                    current_widget = self.tab_widget.currentWidget()
                    current_widget.insert(addmain())
                    return
               
                elif command == "$run":
                    current_widget = self.tab_widget.currentWidget()
                    
                    code=current_widget.text()
                    code=modifycode(code)
                    self.run_python_code( code)
                    return
                elif command == "$weblocal":
                  # Assuming `self.tab_widget.currentWidget()` and related code works correctly.
                  current_widget = self.tab_widget.currentWidget()
                  current_index = self.tab_widget.currentIndex()  # Assuming you want the index of the current tab
                  file_name = self.tab_widget.tabText(current_index)
                  content=self.read_file(file_name)
                  local_path = "/home/solup/Desktop/hack3/temp.html"
                  with open(local_path, 'w') as file:
                   file.write(' <link rel="stylesheet" href="https://cybersecctf.github.io/blog/static/css/style.css" />'+content) 
                  # Open the local file in the browser
                  firefox_path = webbrowser.get(using='firefox')        
                  firefox_path.open(f"file://{local_path}", new=0, autoraise=True)
                elif command == "$web":
                    current_widget = self.tab_widget.currentWidget()
                                            
                    file_name = self.tab_widget.tabText(current_index)
                    dir_path = os.path.dirname(os.path.realpath(file_name))             
                    ctfdirs=dir_path.split("/")
                    search=ctfdirs[len(ctfdirs)-1]
                    webbrowser.open(f"https://cybersecctf.github.io/blog/?q={search}", new=0, autoraise=True)               
                    return                         
                elif command == "$runsh":
                    file_name = self.tab_widget.tabText(current_index)
                    dir_path = os.path.dirname(os.path.realpath(file_name))                          
                    os.chdir(dir_path) 
                    current_widget = self.tab_widget.currentWidget()
                    current_index = self.tab_widget.currentIndex()
                    file_name = self.tab_widget.tabText(current_index)
                    run_shscript(self, file_name)
                    return
                elif command.startswith("$$goto"):
                    _, term = command.split(maxsplit=1)
                    self.goto_line(int(term))
                elif command.startswith("$$findnext"):
                     self.find_next()                        
                elif command.startswith("$$find"):
                    global findterm 
                    _, term = command.split(maxsplit=1)
                    matches=[]   
                    if  findterm!=term:
                     self.find_term(term)
                     findterm=term
                     
                    else:
                     self.find_next()  
                   
                    self.search_blog(term)
                    
                    return
                elif command == "$$save gpg":
                                     
                    d=self.select_folder()
                    blog.islog=True
                    private,public=blog.solveup("tryhackme sign file","generate keys")
                    d=self.select_file()     
                    return
                elif command=="$$new": 
                 global apps 
                 try:  
                              
                   
                   sfile=apps+'/writeup1.md'
                   current_widget = self.tab_widget.currentWidget()
                   current_widget.insert(self.read_file(sfile))                                        
                      
                   self.setWindowTitle("Solveup-"+sfile)                 
                 except Exception as e:
                   print("new writeup making error: " + str(e))  
                elif command.startswith("$$timer"):
                  try:
                   time=100    
                   if len(command)>7:
                    time=command.split(" ")[1]
                    time=int(time)                    
                   dialog = Timer(duration=time)  # 100-second timer    or defiiferent 
                   dialog.exec_()
                  except Exception as e:
                      print(f"error in timer:{str(e)}")
                elif command.startswith("$$linkgithub"): 
                  file=self.select_file() 
                  current_widget = self.tab_widget.currentWidget()
                  current_widget.insert(addlinkgithub(file))
                  return  
                elif command.startswith("$$link"): 
                  file=self.select_file() 
                  current_widget = self.tab_widget.currentWidget()
                  current_widget.insert(addlink(file))
                  return
                
                elif command == "$$image":
                  file=self.select_file() 
                  current_widget = self.tab_widget.currentWidget()
                  current_widget.insert(addimage(file))
                elif command == "$$dark":
                    self.toggle_dark_mode()
                    return
                elif command.startswith("$"):
                     if command.startswith('$'):
                        # Send command to QTerminal
                        subprocess.Popen(['konsole', '-e', f'bash -c "{command[1:]}; exec bash"'])
                     return
                else:
                  try:
                    self.find_term(command)           
                    dir_path = os.path.dirname(os.path.realpath(filenames[current_index]))                          
                    os.chdir(dir_path)
                    result =self.runsh(command)
                    output = result
                    self.command_output.setText(f'$ {command}\n{output}')
                  except Exception as e:
                            print(str(e)) 
                self.command_output.setFixedHeight(int(self.command_output.document().size().height()) + 10)
            except Exception as e:
                self.find_term(command)           
                self.command_output.append(f'Error: {str(e)}')
                self.command_output.setFixedHeight(int(self.command_output.document().size().height()) + 10)
    def find_next(self):
     current_index = self.tab_widget.currentIndex()
     current_widget = self.tab_widget.currentWidget()

     # Ensure there are matches to navigate
     if not hasattr(current_widget, 'matches'):
        print("No previous search results to navigate.")
        return

     matches = current_widget.matches
     current_match_index = getattr(current_widget, 'current_match_index', -1)
     # Move to the next match
     if current_match_index < len(matches) - 1:
        current_match_index += 1
     else:
        current_match_index = 0  # Wrap around to the first match

     # Highlight the next match
     match = matches[current_match_index]
     start_pos = match.start()
     length = match.end() - start_pos
     # Clear previous indicator and set new one
     current_widget.SendScintilla(QsciScintilla.SCI_INDICATORCLEARRANGE, 0, current_widget.length())
     indicator_num = 0
     current_widget.SendScintilla(QsciScintilla.SCI_INDICSETSTYLE, indicator_num, QsciScintilla.INDIC_ROUNDBOX)
     current_widget.SendScintilla(QsciScintilla.SCI_INDICSETFORE, indicator_num, QColor("yellow").rgb())
     current_widget.SendScintilla(QsciScintilla.SCI_INDICSETUNDER, indicator_num, True)
     # Highlight the match
     current_widget.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, start_pos, length)
     # Move the cursor to the start position of the match
     line_num = current_widget.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, start_pos)
     current_widget.SendScintilla(QsciScintilla.SCI_ENSUREVISIBLE, line_num)
     current_widget.SendScintilla(QsciScintilla.SCI_SETSEL, start_pos, start_pos)

     # Update current match index
     current_widget.current_match_index = current_match_index

     # Get the position of the cursor in the widget coordinates
     cursor_x = current_widget.SendScintilla(QsciScintilla.SCI_POINTXFROMPOSITION, 0, start_pos)
     cursor_y = current_widget.SendScintilla(QsciScintilla.SCI_POINTYFROMPOSITION, 0, start_pos)

     # Map the widget coordinates to the global screen coordinates
     global_pos = current_widget.mapToGlobal(QPoint(cursor_x, cursor_y))

     # Move the mouse cursor to the global position
     QCursor.setPos(global_pos)
   
    def find_term(self, term):
     current_index = self.tab_widget.currentIndex()
     current_widget = self.tab_widget.currentWidget()
     editor_text = current_widget.text()
     # Set focus to the current widget before starting the search
     #self.tab_widget.setFocus()
     # Use QRegularExpression to match the whole word only
     regex = QRegularExpression(f"\\b{term}\\b")
     # Find the word and move the cursor
     if isinstance(current_widget, TextEditor):
        current_widget.SendScintilla(QsciScintilla.SCI_INDICATORCLEARRANGE, 0, current_widget.length())
        pattern = re.escape(term)
        matches = list(re.finditer(pattern, editor_text))
        current_widget.matches = matches
        if matches:
            indicator_num = 0
            current_widget.SendScintilla(QsciScintilla.SCI_INDICSETSTYLE, indicator_num, QsciScintilla.INDIC_ROUNDBOX)
            current_widget.SendScintilla(QsciScintilla.SCI_INDICSETFORE, indicator_num, QColor("red").rgb())
            current_widget.SendScintilla(QsciScintilla.SCI_INDICSETUNDER, indicator_num, True)

            # Highlight all matches
            for match in matches:
                start_pos = match.start()
                length = match.end() - start_pos
                current_widget.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, start_pos, length)

            # Move the cursor to the start position of the first match
            first_match = matches[0]
            start_pos = first_match.start()
            line_num = current_widget.SendScintilla(QsciScintilla.SCI_LINEFROMPOSITION, start_pos)
            index_in_line = start_pos - current_widget.SendScintilla(QsciScintilla.SCI_POSITIONFROMLINE, line_num)

            # Scroll to the line
            current_widget.SendScintilla(QsciScintilla.SCI_ENSUREVISIBLE, line_num)

            # Set the cursor position
            current_widget.SendScintilla(QsciScintilla.SCI_SETSEL, start_pos, start_pos)

            # Get the position of the cursor in the widget coordinates
            cursor_x = current_widget.SendScintilla(QsciScintilla.SCI_POINTXFROMPOSITION, 0, start_pos)
            cursor_y = current_widget.SendScintilla(QsciScintilla.SCI_POINTYFROMPOSITION, 0, start_pos)

            # Map the widget coordinates to the global screen coordinates
            global_pos = current_widget.mapToGlobal(QPoint(cursor_x, cursor_y))

            # Move the mouse cursor to the global position
            QCursor.setPos(global_pos)
            return matches
        else:
            print(f"No matches found for term: {term}")


    def toggle_dark_mode(self):
        self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")
        self.command_input.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")
        self.command_output.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if isinstance(widget, TextEditor):
                widget.set_dark_mode()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    initial_file = sys.argv[1] if len(sys.argv) > 1 else None
    editor = TabbedEditor(initial_file=initial_file)
    sys.exit(app.exec_())
 

 