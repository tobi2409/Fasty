def build(components, outputPythonFileName):
    newFile = open(outputPythonFileName, 'w')

    for c in components:
        tempFile = open(c, 'r')
        newFile.write(tempFile.read())
        tempFile.close()

    newFile.close()