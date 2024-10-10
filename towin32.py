#Das ist noch nicht funktionsfähig, bislang nur zum Andeuten (als Richtungsweiser) gedacht

import sys
sys.path.append('components/fecomponents/win32')

import components.fecomponents.html as fecomponents

from lxml import etree

parser = etree.XMLParser(remove_comments=True)
loaded_tree = etree.parse('sample.xml', parser)

root = etree.Element('root')
root.append(loaded_tree.getroot())

code = [
    '#include <windows.h>',
    '',
    '// Fensterprozedur',
    'LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {',
    '    switch (uMsg) {',
    '        case WM_DESTROY:',
    '            PostQuitMessage(0);',
    '            return 0;',
    '        case WM_SIZE: {',
    '            !!!LAYOUT-ADJUSTMENT!!!',
    '            return 0;',
    '        }',
    '    }',
    '    return DefWindowProc(hwnd, uMsg, wParam, lParam);',
    '}',
    '',
    'int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {',
    '    const char CLASS_NAME[] = "Win32PanelsClass";',
    '',
    '    // Fensterklasse definieren',
    '    WNDCLASS wc = {0};',
    '    wc.lpfnWndProc = WindowProc;',
    '    wc.hInstance = hInstance;',
    '    wc.lpszClassName = CLASS_NAME;',
    '',
    '    RegisterClass(&wc);',
    '',
    '    // Fenster erstellen',
    '    HWND main_hwnd = CreateWindowEx(',
    '        0,',
    '        CLASS_NAME,',
    '        "Win32 Frame",',
    '        WS_OVERLAPPEDWINDOW,',
    '        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,',
    '        NULL, NULL, hInstance, NULL',
    '    );',
    '',
    '    if (hwnd == NULL) {',
    '        return 0;',
    '    }',
    '',
    '    !!!CONTROLS!!!',
    '',
    '    ShowWindow(hwnd, nCmdShow);',
    '',
    '    // Nachrichtenverarbeitung',
    '    MSG msg = {0};',
    '    while (GetMessage(&msg, NULL, 0, 0)) {',
    '        TranslateMessage(&msg);',
    '        DispatchMessage(&msg);',
    '    }',
    '',
    '    return 0;',
    '}'
]

def generate_ui_element(xml_part, parentname):
    #TODO: hier Fehler
    if 'name' not in xml_part.attrib:
        return

    index = code.index('    !!!CONTROLS!!!')

    name = xml_part.attrib['name']

    win32Control = ''
    #TODO: das über Komponenten auslagern
    if xml_part.tag == 'container':
        win32Control = 'STATIC'

    text = xml_part.text

    code.insert(index, 'HWND ' + name + ' = CreateWindow("' + win32Control + '", "' + text + '", WS_VISIBLE | WS_CHILD | SS_CENTER, , 0, 0, 100, 600, ' + parentname + ', (HMENU) 1, hInstance, NULL);')

#def generate_ui_layout_adjustment(xml_part):
#TODO: innerhalb WM_SIZE mithilfe von MoveWindow positionieren

def generate_ui_elements(xml_part, parentname):
    for e in xml_part:
        generate_ui_element(e, parentname)
        #generate_ui_layout_adjustment(e)

        #TODO: hier Fehler, falls kein name vorhanden
        if 'name' in e.attrib:
            generate_ui_elements(e, e.attrib['name'])

generate_ui_elements(root, 'main_hwnd')

for c in code:
    print(c)