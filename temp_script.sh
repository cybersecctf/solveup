
<!DOCTYPE html>
<html>

<body>
    <h1>Keep It Zipped- CTF1</h1>

    <h2>Challenge Description</h2>
    <p>crack zip file and find flag inside zip that is protected by password 
<a href="https://phantom1ss.github.io/blog/2024/practice/cryptoctf1/keepitzipped/super-secret-files.zip">super-secret-files.zip</a>
</p>
 
    <h2>Solution Approach</h2>
    <p>Here are the steps we took to solve the challenge:</p>
    <ol>
        <pre>
          
           $sudo fcrackzip -u -D -p   "${2:=-/home/rockyou.txt}" $1
           for i in *.zip; do
    echo "Scanning $i"
    unzip -q -c "$i" | grep "utflag" && echo "Found in $i:" && unzip -q -c "$i" | grep $2 || echo "Not found in $i"
done

          </pre> 
       and see password inside zip 
    
    </ol>
<br>
    <h2>Flag</h2>
    <p class="flag">utflag{d0wn_th3_r@bb1t_h0l3}

</p>

    <h2>Conclusion</h2>
    <p>this is a very   easy chanllenge for  search password in zip</p>
</body>
</html>


