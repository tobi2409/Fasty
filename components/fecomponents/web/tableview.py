class TableView:
    #NO_OBJECT_METHODS_BEGIN
    @staticmethod
    def is_composed():
        return True

    # bei tohtml eines Projekts 'test' mit TableView wird folgendes getan:
    # 1.) sofern in .tableview-composition noch kein html, js, css existiert, wird tohtml für .tableview-composition aufgerufen
    # 2.) html von .tableview-composition wird in 'test.html' reingeschrieben
    # 3.) css von .tableview-composition wird in 'test.css' reingeschrieben
    # 4.) js von .tableview-composition wird in 'test.js' reingeschrieben

    # BESSERE VARIANTE:
    # wir haben Projekt 'test'
    # in Projekt 'test' ist eine TableView enthalten und als XML-Parameter stehen u.a. die hier in composition_layout aufgeführten drin
    # und zwar in dem Format: <TableView init-name="..." init-columns="..." init-data="..." init-col_height="..."></TableView>
    # tohtml ruft composition_layout mit params auf
    # params ist ein Dictionary im Format: {'name': '...', 'columns': '...', 'data': '...', 'col_height': '...'}, welches von den init-Felds übernommen wird
    # das composition_python laden und temporär speichern
    # sowohl temp. XML als auch PY in temporäres Projektordner schieben
    # dann kann das XML generiert werden und temporär gespeichert werden
    # anschließend das HTML, CSS, JS über tohtml als temporäre Dateien generieren
    # das HTML in 'test.html' einsetzen
    # das CSS in 'test.css' einsetzen
    # das JS in 'test.js' einsetzen

    # columns: [{'name': 'Col1', 'width': '100'}, {'name': 'Col2', 'width': '100'}, {'name': 'Col3', 'width': '100'}, ...]
    # data: [{'Col1': '1', 'Col2': '2', 'Col3': '3'}, {'Col1': '1', 'Col2': '2', 'Col3': '3'}, ...]
    @staticmethod
    def composition_layout(xml_part, params):
        layout = []

        layout.append('<?xml version="1.0"?>')       

        root_container = '<container name="' + params['name'] + '" '

        if 'left' in xml_part.attrib:
            root_container = root_container + ' left="' + xml_part.attrib['left'] + '"'

        if 'top' in xml_part.attrib:
            root_container = root_container + ' top="' + xml_part.attrib['top'] + '"'

        if 'width' in xml_part.attrib:
            root_container = root_container + ' width="' + xml_part.attrib['width'] + '"'

        if 'height' in xml_part.attrib:
            root_container = root_container + ' height="' + xml_part.attrib['height'] + '"'

        root_container = root_container + ' onclick="tableViewClick()">'

        layout.append(root_container)

        header = xml_part.findall('header')

        #TODO: auch mehrere Header zulassen
        if len(header) != 1:
            print('TableView: Ungültiger Header')
            return
        
        layout.append(' <container name="' + params['name'] + '-header-row" align="top"' + ' height="' + params['col_height'] + '">')

        header = header[0]

        column_widths = []

        for c in header:
            layout.append('      <container name="' + params['name'] + '-header-row-col' + c.attrib['name'] + '" align="left" width="' + c.attrib['width'] + '" height="100%" layout-less="true">')
            layout.append('          <container name="' + params['name'] + '-header-row-' + c.attrib['name'] + '-title" width="100%" height="60%">' + c.text + '</container>')
            layout.append('          <edit name="' + params['name'] + '-header-row-' + c.attrib['name'] + '-searchbar" top="60%" width="100%" height="40%">Search ...</edit>')
            layout.append('      </container>')

            column_widths.append(c.attrib['width'])

        layout.append(' </container>')

        layout.append(' <container name="' + params['name'] + '-tableview-main" align="client" scrollable-y="true">')

        data = xml_part.findall('data')

        if len(data) != 1:
            print('TableView: Ungültige Data')
            return
        
        data = data[0]

        i = 0

        for r in data:
            layout.append('     <container name="' + params['name'] + '-row-' + r.attrib['name'] + '" align="top" width="100%" height="' + params['col_height'] + '">')
            
            for c in r:
                layout.append('         <container name="' + params['name'] + '-row-' + c.attrib['name'] + '" align="left" width="' + column_widths[i] + '" height="100%" layout-less="true">')
                layout.append('             ' + c.text)
                layout.append('         </container>')

            layout.append('     </container>')

        layout.append(' </container>')

        layout.append('</container>')

        return layout
    
    @staticmethod
    def composition_python():
        import os
        return open(os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
                    + '/.tableview-composition/.tableview-composition.py', 'r').read()
    
    # custom_style ist nicht nötig
    # custom_style entspricht den benutzerdefinierten Styles, die in der XML als Attribute eingetragen sind
    # im Custom-Style brauchen wir eine Angaben zu machen
    # in composition_layout werden bereits Style-Attribute der TableView (u.a. left, top, width, height) in den zu erstellenden Containern eingetragen
    # dieser Container wird anschließend von tohtml übersetzt und da die Container-Komponente bekannt ist,
    # wird demnach auch das passende html sowie die in TableView eingetragenen Style-Attribute in das css eingetragen
    #NO_OBJECT_METHODS_END