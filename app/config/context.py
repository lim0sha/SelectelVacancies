import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.session import async_session_maker, close_db_connection
from app.services.parser import parse_and_store
from app.services.scheduler import create_scheduler

logger = logging.getLogger(__name__)


async def _run_parse_job() -> None:
    """Фоновая задача парсинга."""
    try:
        logger.info("Запуск фоновой задачи парсинга")
        async with async_session_maker() as session:
            await parse_and_store(session)
        logger.info("Фоновая задача парсинга завершена успешно")
    except Exception as exc:
        logger.exception("Критическая ошибка в фоновой задаче парсинга: %s", exc)


@asynccontextmanager
async def lifespan_manager(app: FastAPI) -> AsyncGenerator[None, None]:
    """Управление жизненным циклом приложения: запуск и остановка сервисов."""
    scheduler: Optional[AsyncIOScheduler] = None
    logger.info("Инициализация приложения и запуск сервисов...")

    try:
        await _run_parse_job()
        scheduler = create_scheduler(_run_parse_job)
        scheduler.start()
        logger.info("Планировщик задач запущен")

        yield

    finally:
        logger.info("Завершение работы приложения...")
        if scheduler:
            logger.info("Остановка планировщика задач...")
            scheduler.shutdown(wait=False)
            logger.info("Планировщик остановлен")
        try:
            await close_db_connection()
            logger.info("Соединения с базой данных закрыты")
        except Exception as e:
            logger.error("Ошибка при закрытии соединений с БД: %s", e)


lifespan = lifespan_manager
