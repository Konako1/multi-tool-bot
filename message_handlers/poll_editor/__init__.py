from aiogram import Router

from .edit_anonymous import router as edit_anonymous_router
from .edit_multiple import router as edit_multiple_router
from .edit_text import router as edit_text_router
from .poll_editor_handler import router as start_poll_editor_router
from .add_option import router as add_option_router
from .delete_option import router as delete_option_router

router = Router()
router.include_router(start_poll_editor_router)
router.include_router(edit_text_router)
router.include_router(add_option_router)
router.include_router(edit_anonymous_router)
router.include_router(edit_multiple_router)
router.include_router(delete_option_router)
