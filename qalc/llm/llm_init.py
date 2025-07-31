import os
from typing import Any
from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_PROVIDER = "openai"
DEFAULT_TEMPERATURE = 0.3


def llm_init(**kwargs: Any) -> BaseChatModel:
    model = kwargs.pop("model", os.getenv("QALC_LLM_MODEL", DEFAULT_MODEL))
    provider = kwargs.pop("provider", os.getenv("QALC_LLM_PROVIDER", DEFAULT_PROVIDER))
    temperature = kwargs.pop(
        "temperature",
        float(os.getenv("QALC_LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
    )

    return init_chat_model(
        model=model, model_provider=provider, temperature=temperature, **kwargs
    )
