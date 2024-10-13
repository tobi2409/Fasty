def replace(string, mapping):
    i = 0

    while i < len(string):
        noMapping = True

        for m in mapping:
            m_length = len(m)
            m_value_length = len(mapping[m])
            
            if string[i:i+m_length] == m:
                string = string[:i] + mapping[m] + string[i + m_length:]
                i = i + m_value_length
                noMapping = False
                break

        if noMapping:
            i = i + 1

    return string

# replace("Good night Sam!", {"od nig": "abc", "t S": "def", "m!": "1"})

def build(components, outputPythonFileName):
    newFile = open(outputPythonFileName, 'w')
    
    for c in components:
        tempFile = open(c['filename'], 'r')

        tempFileContent = tempFile.read()

        params = c['params']
        tempFileContent = replace(tempFileContent, params)

        newFile.write(tempFileContent)

        tempFile.close()

    newFile.close()