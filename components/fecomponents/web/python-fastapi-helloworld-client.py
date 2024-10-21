#IMPORTS_BEGIN
#fetchapi
#IMPORTS_END

class PythonFastAPIHelloWorldClient(FetchAPI):
    async def fetch(self, url, name):
        response = await super().fetch(url + name, 'GET', {'Accept': 'application/json'}, None)
        return await response.json()