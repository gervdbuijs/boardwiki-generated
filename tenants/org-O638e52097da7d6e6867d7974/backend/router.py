from fastapi import APIRouter

router = APIRouter()

WELCOME_MESSAGE = (
    "Welcome at the BoardWiki Client Web function page. "
    "You will find links (buttons) to the functions that have been generated for you by BoardWiki."
)


@router.get("/message")
def get_welcome_message():
    return {"message": WELCOME_MESSAGE}