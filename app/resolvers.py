from ariadne import QueryType
from fastapi import Request
from .models import product_collection
from .jwt_utils import verify_token
from bson import ObjectId
import re

query = QueryType()

@query.field("searchProducts")
def resolve_search_products(_, info, keyword):
    request: Request = info.context["request"]
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise Exception("Falta el token")

    token = auth_header.split(" ")[1]
    user = verify_token(token)

    regex = re.compile(f".*{re.escape(keyword)}.*", re.IGNORECASE)
    products = list(product_collection.find({
        "$or": [
            {"name": regex},
            {"brand": regex},
            {"description": regex}
        ]
    }))

    for product in products:
        product["_id"] = str(product["_id"])
    return products
