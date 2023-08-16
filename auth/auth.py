from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

# куки в которой будем хранить секретный ключ
cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

SECRET = "SECRET"


# способы аутентификации:
# https://fastapi-users.github.io/fastapi-users/12.1/configuration/overview/

#  jwt-токен хранится у нас только у пользователя в браузере
# и мы можем проверить на сервере валидный токен или нет
# минус jwt стратегии в том, что мы не можем его убить. Если злоумышлиник получил jwt токен, то гг. Если
# бы токен хранился в бд/редисе мы могли бы выключить его, а у jwt токен не валидный только при истечении времени

# в итоге куки + jwt = AuthenticationBackend

# функция для кодирования и декодирования токенов
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
