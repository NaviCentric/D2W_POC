import re

def remove_utf_characters(data):
    pattern = re.compile(r'\\u([\da-fA-F]{4})')
    matches = pattern.finditer(data)
    buf = []
    last_end = 0
    
    for match in matches:
        start, end = match.span()
        buf.append(data[last_end:start])
        ch = chr(int(match.group(1), 16))
        buf.append(ch)
        last_end = end
    
    buf.append(data[last_end:])
    return ''.join(buf)

data = "\u003Cdiv id=\"MASTER_1\" data-id=\"child-docs-1\"\u003E\u003Cp data-master=\"MASTER_1\""
result = remove_utf_characters(data)
print(result)