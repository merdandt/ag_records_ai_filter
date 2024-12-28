import streamlit as st
import LLM.llm_sql_expert as sql_expert


st.set_page_config(page_title="Ask AgRecord Database", page_icon="🌾")


st.header("Chat With AgRecord Database")

request = st.text_input("Enter your request", key="request")

st.markdown("**For example:**")
st.markdown("""
- Which varieties had the lowest ADF production?
- Which growers had the top 5 milk/ton ratios?
- For the Pioneer P0789AMX variety, what was the average yield, starch, and NDF (specify if it is Earlage or Silage)?
""")

submit = st.button("Get Data")

if submit:
    with st.spinner("Thinking..."):
        try:
            sql = sql_expert.get_sql_from_text(request)
            # Clean the SQL code
            sql = sql_expert.clean_sql_code(sql)
            print(sql)
            # Get the data from the database
            data = sql_expert.get_query_from_database(sql, "ag_records.db")
            st.table(data)
        except Exception as e:
            st.error(f"An error occurred: {e}")
       
        
        
