import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Research Copilot",
    layout="wide"
)

st.title("Research Copilot")

# -------------------------
# Sidebar
# -------------------------

st.sidebar.title("Tools")

mode = st.sidebar.radio(
    "Choose Mode",
   [
 "Document Chat",
 "Grammar Checker",
 "Email Generator",
 "Citation Generator",
 "Document Manager",
 "Research Notebook"
]
)

# -------------------------
# Health Check
# -------------------------

try:

    health_response = requests.get(
        f"{API_URL}/health",
        timeout=5
    )

    health_response.raise_for_status()

    health = health_response.json()

    if health.get("vector_store_ready"):
        st.sidebar.success("Vector Store Ready")
    else:
        st.sidebar.warning(
            "Vector Store Not Built"
        )

except requests.RequestException as exc:

    st.sidebar.error(
        f"API Offline\n\n{exc}"
    )

# =====================================================
# DOCUMENT CHAT
# =====================================================

if mode == "Document Chat":

    st.header("Chat With Documents")

    question = st.text_area(
        "Ask a question",
        height=150
    )

    if st.button("Ask"):

        if question.strip():

            try:

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                st.subheader("Answer")

                st.write(
                    data["answer"]
                )

                st.subheader("Sources")

                if data["sources"]:
                    st.json(
                        data["sources"]
                    )
                else:
                    st.info(
                        "No sources returned."
                    )

            except Exception as exc:

                st.error(str(exc))

# =====================================================
# GRAMMAR
# =====================================================

elif mode == "Grammar Checker":

    st.header("Grammar Checker")

    text = st.text_area(
        "Paste text",
        height=250
    )

    if st.button("Improve Grammar"):

        try:

            response = requests.post(
                f"{API_URL}/grammar",
                json={
                    "text": text
                }
            )

            response.raise_for_status()

            result = response.json()

            st.subheader(
                "Corrected Text"
            )

            st.write(
                result["result"]
            )

        except Exception as exc:

            st.error(str(exc))

# =====================================================
# EMAIL
# =====================================================

elif mode == "Email Generator":

    st.header("Email Generator")

    instruction = st.text_area(
        "Describe email",
        height=200
    )

    if st.button("Generate Email"):

        try:

            response = requests.post(
                f"{API_URL}/email",
                json={
                    "text": instruction
                }
            )

            response.raise_for_status()

            result = response.json()

            st.subheader(
                "Generated Email"
            )

            st.write(
                result["result"]
            )

        except Exception as exc:

            st.error(str(exc))

# =====================================================
# CITATION
# =====================================================

elif mode == "Citation Generator":
    
    st.header("Citation Generator")

    citation_info = st.text_area(
        "Enter citation details",
        height=200,
        placeholder="""
Author:
Title:
Year:
Publisher:
DOI:
"""
    )

    if st.button(
        "Generate Citation"
    ):

        try:

            response = requests.post(
                f"{API_URL}/citation",
                json={
                    "text": citation_info
                }
            )

            response.raise_for_status()

            result = response.json()

            st.subheader(
                "Citation"
            )

            st.write(
                result["result"]
            )

        except Exception as exc:

            st.error(str(exc))


elif mode == "Document Manager":

    st.header(
        "Document Manager"
    )

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=[
            "pdf",
            "docx",
            "xlsx",
            "xls"
        ]
    )

    if uploaded_file:

        if st.button(
            "Upload"
        ):
            try:
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue()
                    )
                }

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    timeout=30
                )
                response.raise_for_status()

                result = response.json()
                st.success(
                    f"{result['message']}: {result['path']}"
                )
                st.info(
                    result["rebuild_status"]["message"]
                )
            except Exception as exc:
                st.error(str(exc))

    st.subheader(
        "Current Documents"
    )

    try:

        documents = requests.get(
            f"{API_URL}/documents"
        ).json()

        for doc in documents:

            col1, col2 = st.columns(
                [4, 1]
            )

            with col1:

                st.write(
                    doc["filename"]
                )

            with col2:

                if st.button(
                    "Delete",
                    key=doc[
                        "filename"
                    ]
                ):

                    requests.delete(
                        f"{API_URL}/documents/{doc['filename']}"
                    )

                    st.rerun()

    except Exception as exc:

        st.error(str(exc))

    st.subheader(
        "Knowledge Base"
    )

    try:

        stats = requests.get(
            f"{API_URL}/stats"
        ).json()

        st.metric(
            "Documents",
            stats["documents"]
        )
        st.write(
            f"Rebuild status: {stats['rebuild_status']['status']}"
        )
        st.caption(
            stats["rebuild_status"]["message"]
        )

    except Exception as exc:

        st.error(str(exc))

    if st.button(
        "Rebuild Vector Store"
    ):
        try:
            response = requests.post(
                f"{API_URL}/rebuild",
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            st.success(result["message"])
        except Exception as exc:
            st.error(str(exc))
