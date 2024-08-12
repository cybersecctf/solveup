
<!DOCTYPE html>
<html>
 ss
<body>
    <h1>picoctf2019---glory of garden  Writeup </h1>

    <h2>Challenge Description</h2>
    <p> This garden contains more than it seems.
garden:https://jupiter.challenges.picoctf.org/static/43c4743b3946f427e883f6b286f47467/garden.jpg
</p>

    <h2>Solution Approach</h2>
    <p>Here are the steps we took to solve the challenge:</p>
    <ol> 
        <li>after using binawalk and exiftool not working using 

<pre>
import blog

import os,subprocess
def solve(file, search=""):
    result=""
    if search!="":       
        result = subprocess.run(f"strings {file} | grep {search}", shell=True, text=True, capture_output=True)
    else:
           result = subprocess.run(f"strings {file}", shell=True, text=True, capture_output=True)          
    return result.stdout

if __name__ == "__main__" :
  print(solve("garden.jpg"))
</pre>
    </ol>
<br>
    <h2>Flag</h2>
    <p class="flag">picoCTF{more_than_m33ts_the_3y3657BaB2C}
</p>

    <h2>Conclusion</h2>
    <p>this is a very   easy chanllenge for work on develper tools in in chrome and web exploitations</p>
</body>
</html>
