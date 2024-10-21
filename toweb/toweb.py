import sys
import os
import shutil

from lxml import etree

import style
import eventhandlers
import javascript

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../components/fecomponents')))
import web as fecomponents

def run(directory_name):

    def generate_composed_element(fe_component_clazz, xml_part):
        temp_project_directory_name = directory_name + '/' + xml_part.attrib['name'] + '_temp'

        if not os.path.exists(temp_project_directory_name):
            composition_layout = fe_component_clazz.composition_layout(xml_part, xml_part.attrib)
            composition_python = fe_component_clazz.composition_python()

            os.makedirs(temp_project_directory_name)

            with open(temp_project_directory_name + '/' + xml_part.attrib['name'] + '_temp' + '.xml', 'w') as temp_xml_file:
                temp_xml_file.write('\n'.join(composition_layout))

            with open(temp_project_directory_name + '/' + xml_part.attrib['name'] + '_temp' + '.py', 'w') as temp_py_file:
                temp_py_file.write(composition_python)

            run(temp_project_directory_name)

            with open(temp_project_directory_name + '/' + xml_part.attrib['name'] + '_temp' + '.html') as html_file:
                html = html_file.read()
            
            with open(temp_project_directory_name + '/' + xml_part.attrib['name'] + '_temp' + '.css') as css_file:
                css = []

                while line := css_file.readline():
                    css.append(line.rstrip())

            with open(temp_project_directory_name + '/' + xml_part.attrib['name'] + '_temp' + '.js') as js_file:
                js = []

                while line := js_file.readline():
                    js.append(line.rstrip())

            if os.path.exists(temp_project_directory_name):
               shutil.rmtree(temp_project_directory_name)

            return {'html': etree.fromstring(html, etree.HTMLParser()).find('.//body/'),
                    'css': css,
                    'composition_js_script': js,
                    'is_composed': True}
        
    def generate_simple_component(fe_component_clazz, xml_part, column_index):
        html = fe_component_clazz.html()
        fe_component = etree.fromstring(html, etree.HTMLParser()).find('.//body/')

        css_section = style.generate_css_section(xml_part, column_index)

        if fe_component_clazz.text_to_innertext():
            fe_component.text = xml_part.text
        elif fe_component_clazz.text_to_value():
            fe_component.attrib['value'] = xml_part.text

        fe_component.attrib['id'] = xml_part.attrib['name']

        event_handlers = eventhandlers.generate_event_handlers(xml_part)

        for html_event_name in event_handlers:
            fe_component.attrib[html_event_name] = event_handlers[html_event_name]

        return {'html': fe_component,
                'css': css_section,
                'composition_js_script': [],
                'is_composed': False}

    def generate_dom_element(xml_part, column_index):
        if xml_part.text == None:
            xml_part.text = ''

        if 'name' not in xml_part.attrib:
            print('Element muss Namen vergeben werden: ' + xml_part.tag)
            sys.exit()

        fe_component_clazz = fecomponents.get(xml_part.tag)

        if fe_component_clazz == None:
            print('Komponente nicht gefunden')
            sys.exit()

        if fe_component_clazz.is_composed():
            return generate_composed_element(fe_component_clazz, xml_part)
        
        return generate_simple_component(fe_component_clazz, xml_part, column_index)

    def generate_dom_elements(xml_part):
        dom_elements = etree.Element(xml_part.tag)
        css_list = []
        composition_js_list = []

        def _generate_dom_elements(xml_part_element, column_index):
            dom_element = generate_dom_element(xml_part_element, column_index)

            if not dom_element['is_composed']:
                child_elements = generate_dom_elements(xml_part_element)

                dom_element['html'].extend(child_elements[0])
                css_list.extend(child_elements[1])
                composition_js_list.extend(child_elements[2])

            dom_elements.append(dom_element['html'])
            css_list.extend(dom_element['css'])
            composition_js_list.extend(dom_element['composition_js_script'])

        for e in xml_part:
            if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'top'):
                _generate_dom_elements(e, 1)

        counter = 0
        
        for e in xml_part:
            if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'left'):
                counter = counter + 1
                _generate_dom_elements(e, counter)

        # es darf maximal 1 Client geben
        # falls es kein Client gibt, soll dieser Platz freigelassen werden
        # -> deswegen counter immer um 1 erhöhen
        counter = counter + 1

        for e in xml_part:
            if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'client'):
                _generate_dom_elements(e, counter)
                break

        for e in xml_part:
            if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'right'):
                counter = counter + 1
                _generate_dom_elements(e, counter)

        for e in xml_part:
            if (not isinstance(e, str)) and ('align' in e.attrib) and (e.attrib['align'] == 'bottom'):
                _generate_dom_elements(e, 1)

        for e in xml_part:
            if (not isinstance(e, str) and ('align' not in e.attrib)):
                _generate_dom_elements(e, 1)

        return dom_elements, css_list, composition_js_list

    def generate_html_file():
        project_name = directory_name[directory_name.rfind('/') + 1:]

        parser = etree.XMLParser(remove_comments=True)
        loaded_tree = etree.parse(directory_name + '/' + project_name + '.xml', parser)

        root = etree.Element('root')
        root.append(loaded_tree.getroot())

        html_element = etree.Element('html')

        head_element = etree.Element('head')
        head_element.append(etree.fromstring('<link rel="stylesheet" href="' + project_name + '.css">', etree.HTMLParser()).find('.//head/'))

        body_element = etree.Element('body')

        dom_element_root, css_list, composition_js_list = generate_dom_elements(root)

        #in dom_element_root ist die Wurzel ein spezielles root-Tag und nicht die Wurzel der XML-Datei
        #-> somit wird das erste Element (was dann die Wurzel der XML-Datei ist) genommen
        body_element.append(dom_element_root[0])

        #generate_javascript()
        body_element.append(etree.fromstring('<script src="' + project_name + '.js"></script>', etree.HTMLParser()).find('.//head/'))

        html_element.append(head_element)
        html_element.append(body_element)

        etree.indent(html_element)

        #mit method='html' wird korrekter HTML-Code erzeugt
        html_string = etree.tostring(html_element, pretty_print=True, encoding='unicode', method='html')
            
        if os.path.exists(directory_name + '/' + project_name + '.html'):
            os.remove(directory_name + '/' + project_name + '.html')

        with open(directory_name + '/' + project_name + '.html', 'w') as html_file:
            html_file.write(html_string)

        if os.path.exists(directory_name + '/' + project_name + '.css'):
            os.remove(directory_name + '/' + project_name + '.css')

        with open(directory_name + '/' + project_name + '.css', 'w') as written_css:
            written_css.write('\n'.join(css_list))

        javascript.generate_javascript(directory_name, project_name, composition_js_list)

    generate_html_file()

directory_name = sys.argv[1]
run(directory_name)