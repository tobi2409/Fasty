import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../components/fecomponents')))
import web as fecomponents

def generate_event_handlers(xml_part):
    fe_component_clazz = fecomponents.get(xml_part.tag)

    events = {}

    for a in xml_part.attrib:
        if re.search('^on', a): # Events beginnen immer mit on
            event_name = a
            mapped = fe_component_clazz.event_handlers(event_name, xml_part.attrib[event_name])
            events[mapped['html_event_name']] = mapped['event_handler']

    return events