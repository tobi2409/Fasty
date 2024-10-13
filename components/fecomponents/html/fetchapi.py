class FetchAPI:
    async def fetch(self, url, method, headers, body):
        return await fetch(url, {
            'method': method,
            'headers': headers,
            'body': body,
        })