from aiogram import Router

from filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import start, echo
    from .errors import error_handler
    import handlers.chat_update_checker
    
    router = Router()
    
    # Устанавливаем локальный фильтр, если нужно
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))
    
    router.include_router(error_handler.router)
    router.include_router(handlers.chat_update_checker.router)
    router.include_router(start.router)
    router.include_router(echo.router)
    
    return router
