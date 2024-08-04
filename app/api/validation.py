import openai
from fastapi import APIRouter, Request

from app.core.config import settings
from app.core.logger import logger

router = APIRouter(tags=["Validation-related"])


@router.post(
    "/api/validate-openai-api-key",
    description="A basic API endpoint to check if an existing OpenAI API key inside the '.env' file is valid.",
)
async def validate_openai_api_key(request: Request):
    openai.api_key = settings.openai_api_key
    try:
        # Test the API key by making a simple completion request
        response = openai.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "system", "content": "This is a test"}],
            max_tokens=1,
        )
        if response:
            return {"valid": True}
    except openai.AuthenticationError:
        logger.error("Invalid OpenAI API key.")
        return {"valid": False}
    except Exception as e:
        logger.error(str(e))
        return {"valid": False}

    return {"valid": False}
