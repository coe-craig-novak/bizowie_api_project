from bizowie_api.product_api import ProductAPI

# Example usage
if __name__ == "__main__":
    base_url = "https://coe.mybizowie.com/bz/apiv2/call/"
    
    # Initialize Product API client
    product_api = ProductAPI(base_url)
    
    # # Search products
    # search_params = {"Collection": "Oslo"}
    # products = product_api.search_products(search_params)
    # if products:
    #     print("Search Results:", products)
    
    # Read product details
    product_id = 112379
    product_details = product_api.read_product(product_id)
    if product_details:
        print("Product Details:", product_details)
    
    # # Update product details
    # update_data = {"Category (Web)": "New Category"}
    # update_response = product_api.update_product(product_id, update_data)
    # if update_response:
    #     print("Update Response:", update_response)
    