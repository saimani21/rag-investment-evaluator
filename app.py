import streamlit as st
import tempfile
from utils.summarize_memo import process_memo
from utils.evaluate_fields import evaluate_memo_fields
from utils.report_utils import generate_pdf_report
from utils.chat_handler import query_data
from key_param import OPENAI_API_KEY

# === PAGE SETUP ===
st.set_page_config(page_title="Investment Memo Evaluator", layout="wide")
st.title("🤖 AI-Powered Investment Memo Evaluator")

# === SESSION STATE ===
if "memo_path" not in st.session_state:
    st.session_state.memo_path = None
if "memo_fields" not in st.session_state:
    st.session_state.memo_fields = None
if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = None

# === SIDEBAR TOGGLE ===
mode = st.sidebar.radio("Choose Mode", ["Evaluator", "Chatbot"])

# === MEMO EVALUATOR ===
if mode == "Evaluator":
    st.header("📄 Upload Investment Memo PDF")

    uploaded_file = st.file_uploader("Upload Memo PDF", type=["pdf"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
            st.session_state.memo_path = tmp_path

    if st.button("🔍 Analyze Memo") and st.session_state.memo_path:
        st.success("Analyzing memo...")
        st.session_state.memo_fields = process_memo(st.session_state.memo_path)

    if st.session_state.memo_fields:
        st.subheader("🧠 Extracted Fields")
        for field, value in st.session_state.memo_fields.items():
            st.markdown(f"**{field}**: {value}")

        if st.button("✅ Evaluate Against Guidelines"):
            st.session_state.evaluation_results = evaluate_memo_fields(st.session_state.memo_fields)

    if st.session_state.evaluation_results:
        st.subheader("📊 Evaluation Results")
        for field, evaluation in st.session_state.evaluation_results.items():
            st.markdown(f"**{field}**: {evaluation}")


        st.subheader("📥 Download Evaluation Report")
        pdf = generate_pdf_report(st.session_state.evaluation_results)
        st.download_button("Download PDF", data=pdf, file_name="evaluation_report.pdf", mime="application/pdf")




elif mode == "Chatbot":
    st.header("💬 Ask about investment guidelines or finance")

    with st.form("chat-form"):
        user_query = st.text_input(
            "Enter your question",
            value="",
            placeholder="e.g., Which sectors are restricted for investments?"
        )
        submitted = st.form_submit_button("Ask")

        if submitted and user_query.strip() != "":
            with st.spinner("Searching the guidelines..."):
                response = query_data(user_query)

            st.markdown("**Answer:** " + response)
            st.caption("🔍 Source: Guidelines Vector Database")

