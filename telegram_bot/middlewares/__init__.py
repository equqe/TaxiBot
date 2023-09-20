from loader import dp

from .authentication import AuthenticationMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(AuthenticationMiddleware())
