from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app import main
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.utils.setup_logging import setup_logging

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    global logger
    """
    Управляет жизненным циклом планировщика приложения.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.
    """
    
    logger.info("Инициализация приложения...")
    yield
    logger.info("Завершение работы приложения...")

def create_app() -> FastAPI:
    """
   Создание и конфигурация FastAPI приложения.

   Returns:
       Сконфигурированное приложение FastAPI
   """
    app = FastAPI(
        title="Стартовая сборка FastAPI",
        description=(
            "Стартовая сборка с интегрированной SQLAlchemy 2 для разработки FastAPI приложений с продвинутой "
            "архитектурой\n\n"
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Регистрация роутеров
    register_routers(app)

    return app


def register_routers(app: FastAPI) -> None:
    """Регистрация роутеров приложения."""
    # Корневой роутер
    root_router = APIRouter()

    @root_router.get("/", tags=["root"])
    def home_page():
        return {
            "message": "Hello",
        }

    # Подключение роутеров
    app.include_router(root_router, tags=["root"])
    #app.include_router(router_auth, prefix='/auth', tags=['Auth'])
    app.include_router(router=main)


# Создание экземпляра приложения
app = create_app()


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Start the application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=3)
   
