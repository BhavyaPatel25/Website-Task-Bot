import streamlit as st

from utils.env import load_environment
from chains.task_classifier import build_task_classifier_chain
from chains.transformer_chain import build_transformer_chain
from tools.web_loader import load_web_page
from tools.content_extractor import extract_content


# ---------- Environment ----------
load_environment()

st.set_page_config(
    page_title="Web Task Agent",
    layout="wide"
)

st.title("Web Task Agent")
st.write(
    "Provide a URL and describe the task you want to perform on its content "
    "(e.g., extract text, convert to HTML, summarize, etc.)."
)

# ---------- Inputs ----------
url = st.text_input(
    "Target URL",
    placeholder="https://example.com"
)

task_description = st.text_area(
    "Task Description",
    placeholder="Extract all text and convert it into clean HTML sections"
)

run_button = st.button("Run Task")

# ---------- Execution ----------
if run_button:
    if not url or not task_description:
        st.error("Please provide both a URL and a task description.")
        st.stop()

    try:
        with st.status("Processing...", expanded=True) as status:

            status.write("Classifying task intent...")
            task_chain = build_task_classifier_chain()
            intent = task_chain.invoke({
                "task_description": task_description
            })

            status.write(f"Task type: `{intent.task_type}`")
            status.write(f"Output format: `{intent.output_format}`")

            status.write("Fetching web page...")
            html = load_web_page.invoke({
                "url": url
            })

            status.write("Extracting readable content...")
            extracted_text = extract_content.invoke({
                "html": html
            })

            status.write("Transforming content...")
            transformer_chain = build_transformer_chain(intent)
            transformed = transformer_chain.invoke({
                "content": extracted_text
            })

            status.update(
                label="Task completed successfully",
                state="complete"
            )

        # ---------- Output ----------
        st.subheader("Output")

        if intent.output_format == "html":
            st.code(transformed.content, language="html")
        elif intent.output_format == "markdown":
            st.code(transformed.content, language="markdown")
        elif intent.output_format == "json":
            st.json(transformed.content)
        else:
            st.write(transformed.content)

    except Exception as e:
        st.error(f"An error occurred: {e}")
