class Button:
    @staticmethod
    def html():
        return '<button></button>'
    
    @staticmethod
    def is_innerhtml_from_xml():
        return True
    
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
        
        return ''