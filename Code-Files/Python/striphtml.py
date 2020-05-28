import re

def striphtml(data):
    p = re.compile(r'<.*?>|&.+;')
    return p.sub('', data)

txt = '<a href="something.com" class="bar">I Want <strong>STRONG This &nbsp; </strong> TEST <b>text!</b></a>'

print(txt + "\n")

msg = striphtml(txt)

print(msg)