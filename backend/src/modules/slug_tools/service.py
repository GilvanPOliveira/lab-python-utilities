from slugify import slugify

from src.modules.slug_tools.schemas import SlugRequest


def generate_slug(payload: SlugRequest) -> dict[str, str]:
    return {
        "original": payload.value,
        "slug": slugify(payload.value),
    }
