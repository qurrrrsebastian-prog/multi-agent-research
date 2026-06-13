"""Multi-Agent Research System with Groq (Llama 3.3 70B). Author: Avatar Putra Sigit"""
import os
import sys
import streamlit as st
from langchain_groq import ChatGroq

def get_llm() -> ChatGroq:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        st.error("GROQ_API_KEY not found.")
        sys.exit(1)
    return ChatGroq(model="llama-3.3-70b-versatile", api_key=key, temperature=0.3)

def run_research(topic: str, llm: ChatGroq) -> dict:
    """Run 3-agent research pipeline."""
    # Agent 1: Researcher
    r1 = llm.invoke(f"""You are a market research analyst. Research this topic and provide 5 key facts/data points:
Topic: {topic}
Return as bullet points.""")
    research = r1.content

    # Agent 2: Writer
    r2 = llm.invoke(f"""You are a business writer. Using this research, write a professional report (300 words) in Indonesian:
Research: {research}
Structure: Executive Summary, Key Findings, Recommendation.""")
    report = r2.content

    # Agent 3: Editor
    r3 = llm.invoke(f"""You are an editor. Review this report for clarity and grammar. Return the polished version:
{report}""")
    edited = r3.content

    return {"research": research, "report": report, "edited": edited}

def main() -> None:
    st.set_page_config(page_title="Multi-Agent Research", layout="wide")
    st.title("🤖 Multi-Agent Research System — Groq Powered")
    st.markdown("3 AI agents bekerja bareng: Researcher → Writer → Editor")

    topic = st.text_input("📌 Topik riset:", "Tren jasa rope access di Jakarta 2024")
    if st.button("🔥 Run Research Pipeline", type="primary") and topic:
        llm = get_llm()
        with st.spinner("Agent 1: Researcher collecting data..."):
            result = run_research(topic, llm)

        c1, c2, c3 = st.tabs(["📊 Research", "📝 Draft Report", "✅ Final Edit"])
        with c1:
            st.markdown(result["research"])
        with c2:
            st.markdown(result["report"])
        with c3:
            st.markdown(result["edited"])
            st.download_button("Download Report", result["edited"], file_name="report.md")

if __name__ == "__main__":
    main()
