import streamlit as st

from csv_io import read_csv_text
from profiling import build_report, to_profile
from render import generate_json_report, generate_markdown_report

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    csv_text = uploaded.getvalue().decode("utf-8")
    rows = read_csv_text(csv_text)

    if st.button("Generate Report"):
        report = build_report(rows)
        profile = to_profile(report)
        st.session_state["profile"] = profile

profile = st.session_state.get("profile")

if profile:
    st.subheader("Summary")
    st.write(f"Rows: {profile['n_rows']}")
    st.write(f"Columns: {profile['n_cols']}")

    st.download_button(
        "Download JSON",
        data=generate_json_report(profile),
        file_name="report.json",
        mime="application/json",
    )

    st.download_button(
        "Download Markdown",
        data=generate_markdown_report(profile),
        file_name="report.md",
        mime="text/markdown",
    )