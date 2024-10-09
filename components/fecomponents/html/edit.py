class Edit:
    @staticmethod
    def html():
        return '<input type="edit">'
    
    @staticmethod
    def is_innerhtml_from_xml():
        return False

    @staticmethod
    def style():
        return 'font-size: 25px;'
    
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
    
    #TODO: Compiler zu QT, Android, iOS, (vlt. auch Win32, ncurses)
    #(in gesonderte Klasse auslagern)
    #@staticmethod
    #def qt():
    #    return 'self.textedit = QTextEdit()'