class Container:
    # statische Methoden zum Generieren des DOMs innerhalb tohtml.py

    # NO_OBJECT_METHODS_BEGIN ist wichtig, um nur das Nötigste zu importieren bei JS-Generierung

    #NO_OBJECT_METHODS_BEGIN
    @staticmethod
    def is_composed():
        return False

    @staticmethod
    def html():
        return '<div></div>'
    
    @staticmethod
    def text_to_innertext():
        return True
    
    @staticmethod
    def text_to_value():
        return False

    @staticmethod
    def style():
        return ''

    @staticmethod
    def custom_style(xml_style_name, xml_style_value):
        if (xml_style_name == 'left') or (xml_style_name == 'top') or (xml_style_name == 'width') or (xml_style_name == 'height'):
            if xml_style_value.isdigit():
                return xml_style_name + ': ' + xml_style_value + 'px;'
            elif xml_style_value[-1] == '%':
                return xml_style_name + ': ' + xml_style_value + ';'
        elif xml_style_name == 'background-color':
            import re
            if re.compile(r'#[a-fA-F0-9]{6}$').match(xml_style_value):
                return 'background-color: ' + xml_style_value + ';'
            return ''
        elif xml_style_name == 'scrollable-x':
            if xml_style_value == 'true':
                return 'overflow-x: auto'
            return ''
        elif xml_style_name == 'scrollable-y':
            if xml_style_value == 'true':
                return 'overflow-y: auto'
            return ''
            
        return ''
    
    @staticmethod
    def event_handlers(xml_event_name, xml_event_handler):
        if xml_event_name == 'onclick':
            return {'html_event_name': 'onclick', 'event_handler': xml_event_handler}
        
        return ''
    #NO_OBJECT_METHODS_END
    
    # Objektmethoden für vom Entwickler durchzuführende DOM-Manipulationen

    def __init__(self, name):
        self._name = name
    
    def setText(self, text):
        document.getElementById(self._name).innerText = text