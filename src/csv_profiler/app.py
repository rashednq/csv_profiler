import streamlit as st

from csv_profiler.csv_io import read_csv_text
from csv_profiler.profiling import build_report, to_profile
from csv_profiler.render import generate_json_report, generate_markdown_report

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload CSV → Generate → Download")

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if not uploaded:
    st.info("Upload a CSV file to begin.")
    st.stop()

csv_text = uploaded.getvalue().decode("utf-8")
rows = read_csv_text(csv_text)

if not rows:
    st.error("CSV is empty or could not be parsed.")
    st.stop()

if st.button("Generate Report"):
    report = build_report(rows)
    profile = to_profile(report)
    st.session_state["report"] = report
    st.session_state["profile"] = profile

profile = st.session_state.get("profile")
report = st.session_state.get("report")

if not profile:
    st.warning("Click **Generate Report** to see results.")
    st.stop()

st.subheader("Summary")
c1, c2 = st.columns(2)
c1.metric("Rows", f"{profile['n_rows']:,}")
c2.metric("Columns", f"{profile['n_cols']:,}")

st.subheader("Column Details")
cols_sorted = sorted(profile["columns"], key=lambda x: x["missing"], reverse=True)
st.dataframe(cols_sorted, use_container_width=True)

json_data = generate_json_report(profile)
md_data = generate_markdown_report(profile)

st.subheader("Download")
d1, d2 = st.columns(2)

with d1:
    st.download_button(
        "Download JSON",
        data=json_data,
        file_name="report.json",
        mime="application/json",
        use_container_width=True,
    )

with d2:
    st.download_button(
        "Download Markdown",
        data=md_data,
        file_name="report.md",
        mime="text/markdown",
        use_container_width=True,
    )

with st.expander("Preview Markdown"):
    st.markdown(md_data)

with st.expander("Preview JSON"):
    st.json(profile)
