from aiohttp import web

from .views import get_context


def init():

    app = web.Application()
    app.router.add_post('/get_context', get_context)
    return app

def run():
    app = init()
    web.run_app(app, host='0.0.0.0', port=9000)
