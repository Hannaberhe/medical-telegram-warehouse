"""Pydantic schemas for API request/response validation."""
from pydantic import BaseModel
from typing import Optional

class ProductResponse(BaseModel):
    product: str
    mentions: int

class TopProductsResponse(BaseModel):
    top_products: list[ProductResponse]

class ChannelActivityResponse(BaseModel):
    channel: str
    total_posts: int
    avg_views: float
    active_days: list[str]

class MessageResult(BaseModel):
    message_id: int
    text: str

class SearchResponse(BaseModel):
    query: str
    results: list[MessageResult]

class VisualContentResponse(BaseModel):
    channels_with_images: int
    total_images: int
    promotional_posts: int
    product_displays: int

class ErrorResponse(BaseModel):
    error: str
    status_code: int
