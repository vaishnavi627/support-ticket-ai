import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Support Ticket Analytics",
    page_icon="🎫",
    layout="wide",
)

st.title("🎫 AI Support Ticket Analytics")
st.caption("Natural-language analytics and anomaly detection for support tickets.")
st.session_state.setdefault("query_result", None)
st.session_state.setdefault("anomaly_result", None)

try:
    health = requests.get(f"{API_URL}/health", timeout=5)
    if health.ok:
        st.success("API is running")
except Exception:
    st.error("Cannot connect to FastAPI. Start the API first.")

st.header("Ask a Question")

question = st.text_input(
    "Enter your question",
    placeholder="How many critical tickets are unresolved?",
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing your question..."):
            st.session_state.query_result = None
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": question},
                    timeout=60,
                )
                if response.ok:
                    st.session_state.query_result = response.json()
                else:
                    st.error(response.json().get("detail", "Query failed."))
            except Exception as e:
                st.error(f"Error: {e}")

query_result = st.session_state.query_result
if query_result is not None:
    st.subheader("Answer")
    st.info(query_result["answer"])

    with st.expander("Generated SQL"):
        st.code(query_result["sql"], language="sql")

    if query_result["data"]:
        st.subheader("Query Result")
        st.dataframe(query_result["data"], use_container_width=True)

st.header("Anomaly Detection")

if st.button("Detect Anomalies"):
    with st.spinner("Checking for anomalies..."):
        st.session_state.anomaly_result = None
        try:
            response = requests.get(f"{API_URL}/anomalies", timeout=60)
            if response.ok:
                st.session_state.anomaly_result = response.json()
            else:
                st.error(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

anomaly_result = st.session_state.anomaly_result
if anomaly_result is not None:
    st.metric("Total Anomalies", anomaly_result["total_anomalies"])
    if anomaly_result["anomalies"]:
        st.dataframe(anomaly_result["anomalies"], use_container_width=True)
    else:
        st.success("No anomalies detected.")
