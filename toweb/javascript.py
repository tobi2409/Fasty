import os
import re

def generate_javascript(directory_name, project_name, composition_js_list):
    if os.path.exists(directory_name + '/' + project_name + '.py.tmp'):
        os.remove(directory_name + '/' + project_name + '.py.tmp')

    newFile = open(directory_name + '/' + project_name + '.py.tmp', 'w')

    file = open(directory_name + '/' + project_name + '.py', 'r')

    importedFilenames = []

    def resolve_imports(f):
        firstLine = f.readline().rstrip()

        if firstLine != '#IMPORTS_BEGIN':
            newFile.write(firstLine + '\n')
            return

        for l in f:
            strippedLine = l.rstrip()

            if strippedLine == '#IMPORTS_END':
                break

            componentFileName = os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
                                                + '/../components/fecomponents/web/' + strippedLine[1:] + '.py')

            if importedFilenames.__contains__(componentFileName):
                return

            componentFile = open(componentFileName, 'r')
            resolve_imports(componentFile)

            doWrite = True

            for cl in componentFile:
                strippedCl = cl.rstrip()

                #TODO: dahinter darf nichts stehen, davor nur Leerzeichen oder Tabulatoren
                if re.search('#NO_OBJECT_METHODS_BEGIN', strippedCl):
                    doWrite = False

                if doWrite:
                    newFile.write(strippedCl + '\n')

                if re.search('#NO_OBJECT_METHODS_END', strippedCl):
                    doWrite = True

            componentFile.close()

            importedFilenames.append(componentFileName)

    resolve_imports(file)

    for l in file:
        newFile.write(l)

    file.close()
    newFile.close()

    if os.path.exists(directory_name + '/' + project_name + '.js'):
        os.remove(directory_name + '/' + project_name + '.js')

    if os.path.exists(directory_name + '/' + project_name + '.js.map'):
        os.remove(directory_name + '/' + project_name + '.js.map')

    import subprocess
    subprocess.run(['.venv/bin/pj', directory_name + '/' + project_name + '.py.tmp', '--output', directory_name + '/' + project_name + '.js'])

    with open(directory_name + '/' + project_name + '.js', 'a+') as js_file:
        for c in composition_js_list:
            js_file.write(c)

    if os.path.exists(directory_name + '/' + project_name + '.py.tmp'):
        os.remove(directory_name + '/' + project_name + '.py.tmp')