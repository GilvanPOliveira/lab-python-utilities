from fastapi import APIRouter

from src.modules.markdown_tools.schemas import MarkdownListRequest, MarkdownTableRequest, MarkdownTextRequest
from src.modules.markdown_tools.service import (
    generate_markdown_list,
    generate_markdown_table,
    markdown_to_html,
    strip_markdown,
)

router = APIRouter()


@router.post("/preview")
def preview_route(payload: MarkdownTextRequest):
    return markdown_to_html(payload.content)


@router.post("/strip")
def strip_route(payload: MarkdownTextRequest):
    return strip_markdown(payload.content)


@router.post("/table")
def table_route(payload: MarkdownTableRequest):
    return generate_markdown_table(payload.headers, payload.rows)


@router.post("/list")
def list_route(payload: MarkdownListRequest):
    return generate_markdown_list(payload.items, payload.ordered)
