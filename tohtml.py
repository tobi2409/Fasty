import sys
sys.path.append('components/fecomponents/html')

import os

import components.fecomponents.html as fecomponents

from lxml import etree

import re

directory_name = sys.argv[1]
project_name = directory_name[directory_name.rfind('/') + 1:]

parser = etree.XMLParser(remove_comments=True)
loaded_tree = etree.parse(directory_name + '/' + project_name + '.xml', parser)

root = etree.Element('root')
root.append(loaded_tree.getroot())

written_css = open(directory_name + '/' + project_name + '.css', 'w')

def count_layout_container_childs_by_align(xml_part):
    counted_childs_by_align = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0, 'client': 0, 'none': 0}
    
    for child in xml_part:
        if not 'align' in child.attrib:
            counted_childs_by_align['none'] = counted_childs_by_align['none'] + 1
        else:
            counted_childs_by_align[child.attrib['align']] = counted_childs_by_align[child.attrib['align']] + 1

    #TODO: maximal 1 Client-Align zulassen, ansonsten Fehler!

    return counted_childs_by_align

def generate_layout_container_grid_template_columns_style_assignment(counted_layout_container_childs_by_align):
    result = 'grid-template-columns: '

    for c in range(0, counted_layout_container_childs_by_align['left']):
        result = result + ' auto '

    # falls es kein Client-Align gibt, wird hier eben Platz freigelassen
    result = result + ' 1fr '

    for c in range(0, counted_layout_container_childs_by_align['right']):
        result = result + ' auto '

    result = result + ';'

    return result

def generate_layout_container_grid_template_rows_style_assignment(counted_layout_container_childs_by_align):
    result = 'grid-template-rows: '

    for c in range(0, counted_layout_container_childs_by_align['top']):
        result = result + ' auto '

    result = result + ' 1fr '

    for c in range(0, counted_layout_container_childs_by_align['bottom']):
        result = result + ' auto '

    result = result + ';'

    return result

def generate_layout_container_based_style_assignments(xml_part):
    counted_layout_container_childs_by_align = count_layout_container_childs_by_align(xml_part) 
    layout_container_grid_template_columns_style_assignment = generate_layout_container_grid_template_columns_style_assignment(counted_layout_container_childs_by_align)
    layout_container_grid_template_rows_style_assignment = generate_layout_container_grid_template_rows_style_assignment(counted_layout_container_childs_by_align)
    return 'display: grid; ' + layout_container_grid_template_columns_style_assignment + layout_container_grid_template_rows_style_assignment + ';'

def generate_layout_container_child_based_style_assignments(xml_part, column_index):
    if xml_part.attrib['align'] == 'top' or xml_part.attrib['align'] == 'bottom':
        return 'grid-column: 1 / -1;'
    elif xml_part.attrib['align'] == 'left' or xml_part.attrib['align'] == 'right' or xml_part.attrib['align'] == 'client':
        return 'grid-column: ' + str(column_index) + ';'

def generate_style_assignments(xml_part, column_index):
    style = ''

    # layout-less-container für Platzierung von DOM-Elementen ohne Align

    if (xml_part.tag == 'container') and ('layout-less' not in xml_part.attrib or xml_part.attrib['layout-less'].lower() == 'false'):
        style = style + generate_layout_container_based_style_assignments(xml_part)
    # relative, damit die Position der Child-Elemente vom Layout-Less-Container
    # nicht vom letzten Child-Element abhängt
    elif (xml_part.tag == 'container') and ('layout-less' in xml_part.attrib) and (xml_part.attrib['layout-less'].lower() == 'true'):
        style = style + 'position: relative;'
    
    if 'align' in xml_part.attrib:
        style = style + generate_layout_container_child_based_style_assignments(xml_part, column_index)
    elif (xml_part.getparent().tag == 'container') and ('layout-less' in xml_part.getparent().attrib) and (xml_part.getparent().attrib['layout-less'].lower() == 'true'):
        style = style + 'position: absolute;'

    # die Custom Styles dynamischer Komponenten
    # auch ein Container zählt hier mit rein
    # da auch dort die XML-Styles nicht denen von CSS entsprechen
    fe_component_clazz = fecomponents.get(xml_part.tag)

    style = style + fe_component_clazz.style()

    for style_name in xml_part.attrib:
        if style_name not in ['align', 'layout-less']:
            custom_style = fe_component_clazz.custom_style(style_name, xml_part.attrib[style_name])
            style = style + custom_style

    return style

def generate_css_section(xml_part, column_index):
    written_css.write('#' + xml_part.attrib['name'] + ' {\n')
    written_css.write(generate_style_assignments(xml_part, column_index) + '\n')
    written_css.write('}\n')

def generate_event_handlers(xml_part):
    fe_component_clazz = fecomponents.get(xml_part.tag)

    events = {}

    for a in xml_part.attrib:
        if re.search('^on', a): # Events beginnen immer mit on
            event_name = a
            mapped = fe_component_clazz.event_handlers(event_name, xml_part.attrib[event_name])
            events[mapped['html_event_name']] = mapped['event_handler']

    return events

def generate_dom_element(xml_part, column_index):
    if xml_part.text == None:
        xml_part.text = ''

    if 'name' not in xml_part.attrib:
        print('Element muss Namen vergeben werden')
        sys.exit()

    fe_component_clazz = fecomponents.get(xml_part.tag)

    if fe_component_clazz == None:
        print('Komponente nicht gefunden')
        sys.exit()

    generate_css_section(xml_part, column_index)

    fe_component = etree.fromstring(fe_component_clazz.html(), etree.HTMLParser()).find('.//body/')

    if fe_component_clazz.text_to_innertext():
        fe_component.text = xml_part.text
    elif fe_component_clazz.text_to_value():
        fe_component.attrib['value'] = xml_part.text

    fe_component.attrib['id'] = xml_part.attrib['name']

    event_handlers = generate_event_handlers(xml_part)

    for html_event_name in event_handlers:
        fe_component.attrib[html_event_name] = event_handlers[html_event_name]

    return fe_component

def generate_dom_elements(xml_part):
    dom_elements = etree.Element(xml_part.tag)

    for e in xml_part:
        if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'top'):
            dom_element = generate_dom_element(e, 1)
            dom_element.extend(generate_dom_elements(e))
            dom_elements.append(dom_element)

    counter = 0
    
    for e in xml_part:
        if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'left'):
            counter = counter + 1
            dom_element = generate_dom_element(e, counter)
            dom_element.extend(generate_dom_elements(e))
            dom_elements.append(dom_element)

    # es darf maximal 1 Client geben
    # falls es kein Client gibt, soll dieser Platz freigelassen werden
    # -> deswegen counter immer um 1 erhöhen
    counter = counter + 1

    for e in xml_part:
        if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'client'):
            dom_element = generate_dom_element(e, counter)
            dom_element.extend(generate_dom_elements(e))
            dom_elements.append(dom_element)
            break

    for e in xml_part:
        if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'right'):
            counter = counter + 1
            dom_element = generate_dom_element(e, counter)
            dom_element.extend(generate_dom_elements(e))
            dom_elements.append(dom_element)

    for e in xml_part:
        if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'bottom'):
            dom_element = generate_dom_element(e, 1)
            dom_element.extend(generate_dom_elements(e))
            dom_elements.append(dom_element)

    for e in xml_part:
        if (not isinstance(e, str) and ('align' not in e.attrib)):
            dom_element = generate_dom_element(e, 1)
            dom_element.extend(generate_dom_elements(e))
            dom_elements.append(dom_element)

    return dom_elements

def generate_javascript():
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

            componentFileName = 'components/fecomponents/html/' + strippedLine[1:] + '.py'

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

    if os.path.exists(directory_name + '/' + project_name + '.py.tmp'):
        os.remove(directory_name + '/' + project_name + '.py.tmp')

html_element = etree.Element('html')

head_element = etree.Element('head')
head_element.append(etree.fromstring('<link rel="stylesheet" href="' + project_name + '.css">', etree.HTMLParser()).find('.//head/'))

body_element = etree.Element('body')

dom_element_root = generate_dom_elements(root)

#in dom_element_root ist die Wurzel ein spezielles root-Tag und nicht die Wurzel der XML-Datei
#-> somit wird das erste Element (was dann die Wurzel der XML-Datei ist) genommen
body_element.append(dom_element_root[0])

generate_javascript()
body_element.append(etree.fromstring('<script src="' + project_name + '.js"></script>', etree.HTMLParser()).find('.//head/'))

html_element.append(head_element)
html_element.append(body_element)

etree.indent(html_element)

#mit method='html' wird korrekter HTML-Code erzeugt
html_string = etree.tostring(html_element, pretty_print=True, encoding='unicode', method='html')

import os
if os.path.exists(directory_name + '/' + project_name + '.html'):
    os.remove(directory_name + '/' + project_name + '.html')

with open(directory_name + '/' + project_name + '.html', 'w') as text_file:
    text_file.write(html_string)
    text_file.close()