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

    name = xml_part.attrib['name']

    tag = xml_part.tag
    fe_component_clazz = fecomponents.get(tag)

    if fe_component_clazz == None:
        print("Komponente nicht gefunden")
        sys.exit()
    
    index = frameContent.index('!!DECLARATIONS!!')
    frameContent.insert(index, fe_component_clazz.declaration(name))

    index = frameContent.index('!!CONTROLS!!')

    text = xml_part.attrib['text'] if 'text' in xml_part.attrib else ''
    left = xml_part.attrib['left'] if 'left' in xml_part.attrib and xml_part.attrib['left'][-1] != '%' else '0'
    top = xml_part.attrib['top'] if 'top' in xml_part.attrib and xml_part.attrib['top'][-1] != '%' else '0'
    width = xml_part.attrib['width'] if 'width' in xml_part.attrib and xml_part.attrib['width'][-1] != '%' else '100'
    height = xml_part.attrib['height'] if 'height' in xml_part.attrib and xml_part.attrib['height'][-1] != '%' else '20'

    fe_component = fe_component_clazz.create(name, text, left, top, width, height, parentname)
    frameContent.insert(index, fe_component)

def generate_ui_layout_adjustment(xml_part):
    index = frameContent.index('!!LAYOUT-ADJUSTMENT!!')

    tag = xml_part.tag
    name = xml_part.attrib['name']
    align = xml_part.attrib['align'] if 'align' in xml_part.attrib else ''
    left = xml_part.attrib['left'] if 'left' in xml_part.attrib and xml_part.attrib['left'][-1] != '%' else '0'
    top = xml_part.attrib['top'] if 'top' in xml_part.attrib and xml_part.attrib['top'][-1] != '%' else '0'
    width = xml_part.attrib['width'] if 'width' in xml_part.attrib and xml_part.attrib['width'][-1] != '%' else '100'
    height = xml_part.attrib['height'] if 'height' in xml_part.attrib and xml_part.attrib['height'][-1] != '%' else '20'

    if align == '':
        return
    
    fe_component_clazz = fecomponents.get(tag)
    moveWindow = ''

    if align == 'left':
        moveWindow = fe_component_clazz.leftAlign(name, width)
    elif align == 'right':
        moveWindow = fe_component_clazz.rightAlign(name, width)
    elif align == 'top':
        moveWindow = fe_component_clazz.topAlign(name, height)
    elif align == 'bottom':
        moveWindow = fe_component_clazz.bottomAlign(name, height)
    elif align == 'client':
        moveWindow = fe_component_clazz.clientAlign(name, 0)

    frameContent.insert(index, moveWindow)

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