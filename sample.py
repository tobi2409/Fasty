#IMPORTS_BEGIN
#container
#edit
#python-fastapi-helloworld-client
#IMPORTS_END

testContainer = Container("test-container")
testContainer2 = Container("test-container2")
edit2 = Edit("edit2")

async def clickTest():
    a = "Hallo"
    b = " Tobias"
    testContainer.setText(a + b)

    helloWorldResponse = await PythonFastAPIHelloWorldClient().helloWorld("http://localhost:8000/helloworld/", "Tobias")
    testContainer2.setText(helloWorldResponse["message"])

    #document.getElementById("test-container").innerHTML = a + b

def clickTest2(name):
    #sollte name keine Konstante sein (z.B. Wert eines UI-Elements, dann kann man mittels getElementById().innerText es hier ablesen)
    edit2.setText("Hallo " + name)