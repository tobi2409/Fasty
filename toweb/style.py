import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../components/fecomponents')))
import web as fecomponents

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

    fixed_style = fe_component_clazz.style()
    style = style + fixed_style

    for style_name in xml_part.attrib:
        if style_name not in ['align', 'layout-less']:
            custom_style = fe_component_clazz.custom_style(style_name, xml_part.attrib[style_name])
            style = style + custom_style

    return style

def generate_css_section(xml_part, column_index):
    result = []

    result.append('#' + xml_part.attrib['name'] + '{')
    result.append(generate_style_assignments(xml_part, column_index))
    result.append('}')

    return result
