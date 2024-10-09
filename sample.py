#IMPORTS_BEGIN
#container
#python-fastapi-helloworld-client
#IMPORTS_END

testContainer = Container("test-container")
testContainer2 = Container("test-container2")

async def clickTest():
    a = "Hallo"
    b = " Tobias"
    testContainer.setText(a + b)

    helloWorldResponse = await PythonFastAPIHelloWorldClient().helloWorld("http://localhost:8000/helloworld/", "Tobias")
    testContainer2.setText(helloWorldResponse["message"])

    #document.getElementById("test-container").innerHTML = a + b