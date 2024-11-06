import requests
import json
import os
from pydantic import BaseModel, Field
from typing import Optional, Dict
import pandas as pd

# Load metadata mapping
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metadata_mapping', 'product_metadata.xlsx')
df_metadata_mapping = pd.read_excel(file_path, sheet_name='Sheet1')
metadata_mapping = {row['metadata_id']: row['field_label'] for _, row in df_metadata_mapping.iterrows()}

# Module: product_api.py
from .api_client import BizowieAPI

from pydantic import RootModel

class ProductMetadata(RootModel):
    """
    Model for product metadata, dynamically created from the metadata mapping.
    """
    root: Dict[str, Optional[str]]
    
    @classmethod
    def from_raw_metadata(cls, raw_metadata: Dict[str, str]):
        parsed_metadata = {}
        for key, value in raw_metadata.items():
            field_label = metadata_mapping.get(int(key), f"metadata_{key}")
            parsed_metadata[field_label] = value
        return cls(root=parsed_metadata)

class ProductDetails(BaseModel):
    """
    Model for product details, including metadata.
    """
    product_id: int
    sku: str
    name: str
    description: Optional[str]
    weight: Optional[float]
    upc_code: Optional[str]
    price: Optional[float]
    metadata: ProductMetadata

class ProductAPI(BizowieAPI):
    def search_products(self, search_params):
        """
        Search for products using Bizowie API.
        
        :param search_params: Dictionary containing search parameters.
        :return: JSON response containing product search results.
        """
        return self._post_request("SalesOrder/product/search", search_params)

    def read_product(self, product_id):
        """
        Read product details by product ID.
        
        :param product_id: The ID of the product to read.
        :return: ProductDetails object containing parsed product details.
        """
        body = {"product_id": product_id}
        response = self._post_request("SalesOrder/product/read", body)
        if response and response.get("success") == 1:
            product_data = response.get("response", {})
            metadata = ProductMetadata.from_raw_metadata(product_data.get("metadata", {}))
            product_details = ProductDetails(
                product_id=int(product_data.get("store_product_id")),
                sku=product_data.get("sku"),
                name=product_data.get("name"),
                description=product_data.get("description"),
                weight=float(product_data.get("weight")) if product_data.get("weight") else None,
                upc_code=product_data.get("upc_code"),
                price=float(product_data.get("price")) if product_data.get("price") else None,
                metadata=metadata
            )
            return product_details
        else:
            raise ValueError(f"Error reading product: {response.get('error_string')}")
    
    def update_product(self, product_id, update_data):
        """
        Update product details.
        
        :param product_id: The ID of the product to update.
        :param update_data: Dictionary containing data to update.
        :return: JSON response containing update result.
        """
        return self._post_request(f"SalesOrder/product/update/{product_id}", update_data)
