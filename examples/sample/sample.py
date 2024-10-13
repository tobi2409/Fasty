#IMPORTS_BEGIN
#edit
#button
#fetchapi
#IMPORTS_END

edit1 = Edit("edit1")
button1 = Button("button1")

async def testClick():
    #edit1.setText("Hallo")
    
    #response = await FetchAPI().fetch('http://localhost:8000/tags', 'GET', {'Accept': 'application/json'}, None)
    #edit1.setText(await response.json())

    edit1.setText('TEST')