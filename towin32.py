#Das ist noch nicht funktionsfähig, bislang nur zum Andeuten (als Richtungsweiser) gedacht

import sys
sys.path.append('components/fecomponents/win32')

import components.fecomponents.win32 as fecomponents

from lxml import etree

parser = etree.XMLParser(remove_comments=True)
loaded_tree = etree.parse('sample.xml', parser)

root = etree.Element('root')
root.append(loaded_tree.getroot())

frame = open('win32frame.c', 'r')
frameContent = frame.read().splitlines()

newFile = open('sample.c', 'w')

def generate_ui_element(xml_part, parentname):
    if 'name' not in xml_part.attrib:
        print('Element muss Namen vergeben werden')
        sys.exit()

    index = frameContent.index('!!CONTROLS!!')

    tag = xml_part.tag
    name = xml_part.attrib['name']
    text = xml_part.attrib['text'] if 'text' in xml_part.attrib else ''
    left = xml_part.attrib['left'] if 'left' in xml_part.attrib and xml_part.attrib['left'][-1] != '%' else '0'
    top = xml_part.attrib['top'] if 'top' in xml_part.attrib and xml_part.attrib['top'][-1] != '%' else '0'
    width = xml_part.attrib['width'] if 'width' in xml_part.attrib and xml_part.attrib['width'][-1] != '%' else '100'
    height = xml_part.attrib['height'] if 'height' in xml_part.attrib and xml_part.attrib['height'][-1] != '%' else '20'
    
    fe_component_clazz = fecomponents.get(tag)

    if fe_component_clazz == None:
        print("Komponente nicht gefunden")
        sys.exit()

    fe_component = fe_component_clazz.create(name, text, left, top, width, height, parentname)
    frameContent.insert(index, fe_component)

#def generate_ui_layout_adjustment(xml_part):


#TODO: innerhalb WM_SIZE mithilfe von MoveWindow positionieren

def generate_ui_elements(xml_part, parentname):
    for e in xml_part:
        generate_ui_element(e, parentname)
        generate_ui_layout_adjustment(e)

        if 'name' in e.attrib:
            generate_ui_elements(e, e.attrib['name'])

generate_ui_elements(root, 'main_hwnd')

newFile.write('\n'.join(frameContent))

newFile.close()
frame.close()