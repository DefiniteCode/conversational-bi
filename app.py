import streamlit as st
from scripts.run_script import run_query

st.set_page_config(layout="wide")

st.markdown("""
<div style='
    width: 100%;
    background: linear-gradient(90deg, #ff6b6b, #c0392b);
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 20px;
'>
    <h1 style='color: white; margin: 0; font-size: 50px;'>
         Telecel Ghana Conversational Business Intelligence System (cbi v1.0)
    </h1>
</div>
""", unsafe_allow_html=True)

user_prompt = st.text_input("Please enter your prompt")

btn_send_prompt = st.button("Send Prompt")

# store result in session state
if "response" not in st.session_state:
    st.session_state.response = None

if btn_send_prompt:
    if user_prompt == "":
        st.warning("Please enter your request for processing")
    else:
        sql_query = "select * from customer_daily_fact cdf where state = 'Greater Accra' and age >= 30;"
        st.session_state.response = run_query(sql_query)

# display results if available
if st.session_state.response is not None:
    df = st.session_state.response

    st.write("Top 5 rows:")
    st.dataframe(df.head())

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="cbi_export.csv",
        mime="text/csv"
    )