from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api import monstro as monstro_router
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from typing import AsyncGenerator
from api.utils.setup_logging import setup_logging
from api.profiles.utils import check_working_party_for_append, from_working_parties_to_trash_party

logger = setup_logging()
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    global logger
    """
    Управляет жизненным циклом планировщика приложения.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.
    """
    
    logger.info("Инициализация приложения...")
    try:
        scheduler.add_job(
            check_working_party_for_append,
            trigger=IntervalTrigger(minutes=1),
            id='currency_update_parties',
            replace_existing=True
        )

        scheduler.add_job(
            from_working_parties_to_trash_party,
            trigger=IntervalTrigger(minutes=1),
            id="currency_clear_s_mix",
            replace_existing=True
        )
        scheduler.start()
        logger.info("Планировщик обновления ")
        yield
    except Exception as e:
        logger.error(f"Ошибка инициализации планировщика: {e}")
    finally:
        # Завершение работы планировщика
        scheduler.shutdown()
        logger.info("Планировщик обновления курсов валют остановлен")
    
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
            "message": "",
        }

    # Подключение роутеров
    app.include_router(root_router, tags=["root"])
    #app.include_router(router_auth, prefix='/auth', tags=['Auth'])
    app.include_router(router=monstro_router)


# Создание экземпляра приложения
app = create_app()


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Start the application")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
   
