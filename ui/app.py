import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Offline RAG Assistant", layout="wide")
st.title("Offline RAG LLM")

try:
    health_response = requests.get(f"{API_URL}/health", timeout=5)
    health_response.raise_for_status()
    health = health_response.json()
    if health.get("vector_store_ready"):
        st.success("API is reachable and the vector store is ready.")
    else:
        st.warning("API is reachable, but the vector store has not been built yet.")
except requests.RequestException as exc:
    st.error(f"API is not reachable: {exc}")

question = st.text_area("Ask a question from your documents", height=120)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        try:
            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question},
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Sources")
            if data["sources"]:
                st.json(data["sources"])
            else:
                st.info("No supporting sources were returned.")
        except requests.HTTPError:
            detail = "Unknown API error"
            try:
                detail = response.json().get("detail", detail)
            except Exception:
                pass
            st.error(detail)
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
