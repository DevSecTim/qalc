import os
import yaml
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
_prompt_cache = {}


def get_prompt(prompt_name: str, **kwargs) -> list:
    """
    Load a YAML prompt template from the templates directory, format it with kwargs,
    and return the formatted messages. The YAML file should define 'system' and/or
    'user' message templates. Uses a cache for loaded templates.
    """
    if prompt_name in _prompt_cache:
        chat_template = _prompt_cache[prompt_name]
    else:
        for ext in (".yaml", ".yml"):
            file_path = os.path.join(TEMPLATE_DIR, f"{prompt_name}{ext}")
            if os.path.isfile(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    spec = yaml.safe_load(f)
                messages = []
                if "system" in spec:
                    messages.append(
                        SystemMessagePromptTemplate.from_template(spec["system"])
                    )
                if "user" in spec:
                    messages.append(
                        HumanMessagePromptTemplate.from_template(spec["user"])
                    )
                chat_template = ChatPromptTemplate.from_messages(messages)
                _prompt_cache[prompt_name] = chat_template
                break
        else:
            raise FileNotFoundError(
                f"Prompt template {prompt_name} not found in {TEMPLATE_DIR}."
            )
    formatted_messages = chat_template.format_messages(**kwargs)
    return formatted_messages
