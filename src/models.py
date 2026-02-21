from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import datetime

@dataclass
class Product:
    id: str
    name: str
    price: Optional[str]  # Might be None if login required
    stock_status: str     # "In Stock", "Out of Stock", "Unknown"
    images: List[str]     # List of image URLs
    product_url: str
    category: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[str] = None
    is_online_exclusive: bool = False
    is_warehouse_exclusive: bool = False
    crawled_at: str = datetime.datetime.now().isoformat()
    last_updated: str = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
