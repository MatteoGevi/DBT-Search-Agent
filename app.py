import streamlit as st

user_query = st.text_input("Ask a question about the dbt data models:")
if st.button("Search"):
    results = search_models(user_query, dbt_metadata_df)
    st.write(results)