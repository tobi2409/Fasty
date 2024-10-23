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
        self._children = []

    def getName(self):
        return self._name

    def createAtRuntime(self, parent):
        container = document.createElement('div')
        container.id = self._name
        document.getElementById(parent.getName()).appendChild(container)

    def addChildren(self, e):
        self._children.push(e)

    def getChildren(self):
        return self._children

    def adjustContainer(self):
        #TODO: Methoden von style.py nutzen
        def count_layout_container_childs_by_align():
            counted_childs_by_align = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0, 'client': 0, 'none': 0}
            
            for child in self._children:
                #TODO: sollte kein align im Child drin sein
                if child.
                    counted_childs_by_align['none'] = counted_childs_by_align['none'] + 1
                else:
                    counted_childs_by_align[child.attrib['align']] = counted_childs_by_align[child.attrib['align']] + 1

            #TODO: maximal 1 Client-Align zulassen, ansonsten Fehler!

            return counted_childs_by_align

        console.log(count_layout_container_childs_by_align())
    
    def setText(self, text):
        document.getElementById(self._name).innerText = text

    #TODO: left, top, width, height und hinterher auch background-color und scrollable
    # muss den möglichen Eigenschaftswerten der custom_style-Methode entsprechen
    def setLeft(self, left):
        document.getElementById(self._name).style.left = left

    def setTop(self, top):
        document.getElementById(self._name).style.top = top

    def setWidth(self, width):
        document.getElementById(self._name).style.width = width

    def setHeight(self, height):
        document.getElementById(self._name).style.height = height

    def setAlign(self, align):
        self._align = align

    #def setLayoutLess(self, layoutLess):