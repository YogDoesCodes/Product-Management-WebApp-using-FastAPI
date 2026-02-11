import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("📦 Product Management System")

# -------------------------
# ADD PRODUCT
# -------------------------

st.header("Add Product")

name = st.text_input("Product Name")
price = st.number_input("Price", min_value=0.0)
quantity = st.number_input("Quantity", min_value=0)

if st.button("Add Product"):
    data = {
        "name": name,
        "price": price,
        "quantity": quantity
    }

    response = requests.post(f"{API_URL}/products", json=data)

    if response.status_code == 200:
        st.success("✅ Product Added Successfully!")
    else:
        st.error("❌ Error adding product")

# -------------------------
# VIEW PRODUCTS
# -------------------------

st.header("Product List")

response = requests.get(f"{API_URL}/products")

if response.status_code == 200:
    products = response.json()

    if products:
        df = pd.DataFrame(products)
        st.dataframe(df)
    else:
        st.info("No products found")

# -------------------------
# DELETE PRODUCT
# -------------------------

st.header("Delete Product")

product_id = st.number_input("Enter Product ID", min_value=1)

if st.button("Delete Product"):
    response = requests.delete(f"{API_URL}/products/{product_id}")

    if response.status_code == 200:
        st.success("✅ Product Deleted!")
    else:
        st.error("❌ Product not found")
