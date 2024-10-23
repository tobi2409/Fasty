#IMPORTS_BEGIN
#container
#IMPORTS_END

def runtimeComponent():
    parent = Container('container1_5')

    container = Container('runtime-container')
    container.createAtRuntime(parent)
    parent.addChildren(container)
    container.setLeft(100)
    container.setTop(100)
    container.setWidth(300)
    container.setHeight(300)

    leftContainer = Container('runtime-left-container')
    leftContainer.createAtRuntime(container)
    container.addChildren(leftContainer)
    leftContainer.setAlign('left')
    leftContainer.setWidth(50)

    bottomContainer = Container('runtime-bottom-container')
    bottomContainer.createAtRuntime(container)
    container.addChildren(bottomContainer)
    bottomContainer.setAlign('bottom')
    bottomContainer.setHeight(50)

    leftContainer2 = Container('runtime-left-container2')
    leftContainer2.createAtRuntime(container)
    container.addChildren(leftContainer2)
    leftContainer2.setAlign('left')
    leftContainer2.setWidth(50)

    container.adjustContainer()