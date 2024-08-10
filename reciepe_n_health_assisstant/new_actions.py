from aijson import register_action

@register_action
def split_text(text: str) -> list[str]:
    """
    Split text by comma
    """
    return text.split(".")[1:]
