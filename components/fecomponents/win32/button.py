class Button:
    @staticmethod
    def create(name, text, left, top, width, height, parentname):
        return 'HWND ' + name + ' = CreateWindow("BUTTON", "' + text + '", WS_VISIBLE | WS_CHILD | SS_CENTER, ' + left + ', ' + top + ', ' + width + ', ' + height + ', ' + parentname + ', NULL, hInstance, NULL);'