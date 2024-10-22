#IMPORTS_BEGIN
#container
#IMPORTS_END

def runtimeComponent():
    container = Container('runtime-container')
    container.createAtRuntime(document.getElementById('container1_5'))
    container.setLeft(100)
    container.setTop(100)
    container.setWidth(300)
    container.setHeight(300)