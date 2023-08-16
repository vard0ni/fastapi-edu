from fastapi_users import FastAPIUsers

from fastapi import FastAPI, Depends

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app = FastAPI(
    title="Trading App"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# добавляем роутеры

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# получаем текущего пользователя
current_user = fastapi_users.current_user()


# создаём endpoint, чтобы он был доступен только зашедшим пользователям
# если jwt-токен истёк(куки исчёз), то мы не сможем войти по этому роуту
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


# создаём endpoint, чтобы он был доступен для всех
@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"
