class PythonFastAPIHelloWorldClient:
    async def helloWorld(self, url, name):
        response = await fetch(url + name, {
            "method": "GET",
            "headers": {
                "Accept": "application/json"
            }
        })

        return await response.json()