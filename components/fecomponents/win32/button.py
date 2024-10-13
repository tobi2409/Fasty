class Button:
    @staticmethod
    def declaration(name):
        return 'HWND ' + name + ';'

    @staticmethod
    def create(name, text, left, top, width, height, parentname):
        return name + ' = CreateWindow("BUTTON", "' + text + '", WS_VISIBLE | WS_CHILD | SS_CENTER, ' + left + ', ' + top + ', ' + width + ', ' + height + ', ' + parentname + ', NULL, hInstance, NULL);'
    
    @staticmethod
    def leftAlign(name, width):
        return 'MoveWindow(' + name + ', 0, 0, ' + width + ', height, TRUE);'
    
    @staticmethod
    def rightAlign(name, width):
        return 'MoveWindow(' + name + ', width - ' + width + ', 0, ' + width + ', height, TRUE);'
    
    @staticmethod
    def topAlign(name, height):
        return 'MoveWindow(' + name + ', 0, 0, width, ' + height + ', TRUE);'

    @staticmethod
    def bottomAlign(name, height):
        return 'MoveWindow(' + name + ', 0, height - ' + height + ', width, ' + height + ', TRUE);'
    
    @staticmethod
    def clientAlign(name, centerSize):
        return ''
        #return 'MoveWindow(' + name + ', (width - centerSize) / 2, (height - centerSize) / 2, centerSize, centerSize, TRUE);'