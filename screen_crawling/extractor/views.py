""" Module for desc web methods of service """

from aiohttp import web
from aiohttp import ClientSession

from .classifier import get_content


async def fetch(url):
    async with ClientSession(headers={'User-Agent': 'Robot'}) as session:
        async with session.post(url) as respose:
            content = await respose.text()
            return content
    return None


async def get_context(request):
    data = await request.post()
    raw_site_data = await fetch(data['url'])
    data = get_content(raw_site_data)
    return web.Response(text=data)