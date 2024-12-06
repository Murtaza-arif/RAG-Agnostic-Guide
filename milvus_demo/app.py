import streamlit as st
from product_search import ProductSearch
import pandas as pd
import atexit
from sample_products import SAMPLE_PRODUCTS

# Set page config
st.set_page_config(
    page_title="Product Search Engine",
    page_icon="🔍",
    layout="wide"
)

# Initialize the search engine
@st.cache_resource(ttl=3600)  # Cache for 1 hour
def get_search_engine():
    search_engine = ProductSearch()
    # Register cleanup
    atexit.register(search_engine.cleanup)
    return search_engine

def show_search_interface():
    st.title("🔍 Semantic Product Search")
    st.write("Search for products using natural language queries!")

    try:
        # Initialize search engine
        search_engine = get_search_engine()

        # Search interface
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input("Enter your search query", placeholder="e.g., comfortable running shoes for marathon")
        with col2:
            threshold = st.slider("Similarity Threshold", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
        
        top_k = st.slider("Maximum number of results", min_value=1, max_value=10, value=3)

        if st.button("Search"):
            if query:
                with st.spinner("Searching..."):
                    results = search_engine.search(query, top_k=top_k, threshold=threshold)
                    
                    if not results:
                        st.warning("😕 No relevant products found. Try:")
                        st.markdown("""
                        - Using different search terms
                        - Lowering the similarity threshold
                        - Being more general in your search
                        """)
                    else:
                        st.success(f"Found {len(results)} relevant products!")
                        
                        # Display results in a nice format
                        for result in results:
                            with st.container():
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.subheader(result['name'])
                                    st.write(result['description'])
                                    st.caption(f"Similarity Score: {result['similarity']:.2%}")
                                with col2:
                                    st.metric("Price", f"${result['price']:.2f}")
                                    st.metric("Rating", f"⭐ {result['rating']:.1f}")
                                st.divider()
            else:
                st.warning("Please enter a search query")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page to try again.")

def show_sample_products():
    st.title("📦 Sample Products Catalog")
    st.write("Here are all the products available in our database:")

    # Create tabs for different views
    view_type = st.radio("Select View", ["Card View", "Table View"], horizontal=True)

    if view_type == "Card View":
        # Display products in a card layout
        cols = st.columns(3)  # Create 3 columns
        for idx, product in enumerate(SAMPLE_PRODUCTS):
            with cols[idx % 3]:
                with st.container():
                    st.subheader(product['name'])
                    st.write(product['description'])
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Price", f"${product['price']:.2f}")
                    with col2:
                        st.metric("Rating", f"⭐ {product['rating']:.1f}")
                    st.divider()
    else:
        # Display products in a table
        df = pd.DataFrame(SAMPLE_PRODUCTS)
        # Reorder columns
        df = df[['id', 'name', 'description', 'price', 'rating']]
        # Format price column
        df['price'] = df['price'].apply(lambda x: f"${x:.2f}")
        # Format rating column
        df['rating'] = df['rating'].apply(lambda x: f"⭐ {x:.1f}")
        st.dataframe(
            df,
            column_config={
                "id": "ID",
                "name": "Product Name",
                "description": "Description",
                "price": "Price",
                "rating": "Rating"
            },
            hide_index=True
        )

def main():
    # Create tabs
    tab1, tab2 = st.tabs(["🔍 Search Products", "📦 Sample Products"])
    
    with tab1:
        show_search_interface()
    with tab2:
        show_sample_products()

if __name__ == "__main__":
    main()
