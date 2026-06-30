"""FastAPI application for Medical Telegram Analytics."""
from fastapi import FastAPI, Query, HTTPException
from api.schemas import (
    TopProductsResponse, ProductResponse,
    ChannelActivityResponse,
    SearchResponse, MessageResult,
    VisualContentResponse, ErrorResponse
)

app = FastAPI(
    title="Medical Telegram Analytics API",
    description="API for analyzing Ethiopian medical Telegram channels",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Medical Telegram Analytics API", "status": "running"}

@app.get("/api/reports/top-products", response_model=TopProductsResponse)

def top_products(limit: int = Query(10, ge=1, le=50)):
    try:
        products = [
            {"product": "Paracetamol", "mentions": 145},
            {"product": "Amoxicillin", "mentions": 120},
            {"product": "Ibuprofen", "mentions": 98},
            {"product": "Omeprazole", "mentions": 85},
            {"product": "Metformin", "mentions": 72},
            {"product": "Ciprofloxacin", "mentions": 65},
            {"product": "Diclofenac", "mentions": 58},
            {"product": "Azithromycin", "mentions": 52},
            {"product": "Cetirizine", "mentions": 45},
            {"product": "Albendazole", "mentions": 40}
        ]
        return {"top_products": products[:limit]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivityResponse)
def channel_activity(channel_name: str):
    try:
        channel_data = {
            "CheMed": {"total_posts": 350, "avg_views": 1200, "active_days": ["Mon", "Wed", "Fri"]},
            "lobelia_cosmetics": {"total_posts": 220, "avg_views": 850, "active_days": ["Tue", "Thu", "Sat"]},
            "tikvah_pharma": {"total_posts": 180, "avg_views": 950, "active_days": ["Mon", "Thu", "Fri"]}
        }
        if channel_name not in channel_data:
            raise HTTPException(status_code=404, detail=f"Channel {channel_name} not found")
        
        data = channel_data[channel_name]
        return {
            "channel": channel_name,
            "total_posts": data["total_posts"],
            "avg_views": data["avg_views"],
            "active_days": data["active_days"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/messages", response_model=SearchResponse)
def search_messages(query: str, limit: int = Query(20, ge=1, le=100)):
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
        
        results = [
            {"message_id": 1, "text": f"{query} available in stock at good price"},
            {"message_id": 2, "text": f"New shipment of {query} just arrived"},
            {"message_id": 3, "text": f"Looking for {query}? Contact us today"}
        ]
        return {"query": query, "results": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/visual-content", response_model=VisualContentResponse)
def visual_content():
    try:
        return {
            "channels_with_images": 3,
            "total_images": 150,
            "promotional_posts": 45,
            "product_displays": 80
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
