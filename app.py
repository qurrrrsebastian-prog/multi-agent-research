"""Multi-Agent Research System — Groq (Llama 3.3 70B) | v2.0 production upgrade.

Cyan Research theme with a horizontal pipeline visualizer. Three agents run in
sequence (Researcher → Writer → Editor). v2.0 adds SQLite session persistence
(research_sessions, agent_steps, audit_log), a live pipeline tracker, per-step
execution-time tracking, a step detail viewer (input/output), a history browser
and Markdown/TXT/JSON export. Lazy Groq client keeps the UI usable without a key.

Author: Avatar Putra Sigit | GitHub: qurrrrsebastian-prog
"""
import json
import os
import time

import streamlit as st

import database as db
from security import generate_session_token, sanitize_input
from ui_components import pipeline_html, render_footer, render_header

st.set_page_config(page_title="Multi-Agent Research", layout="wide", page_icon="🤖")

db.init_db()

AGENTS = ["Researcher", "Writer", "Editor"]


@st.cache_resource(show_spinner=False)
def get_llm():
    """Return a cached Groq chat model, or None if no API key."""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return None
    try:
        from langchain_groq import ChatGroq
        return ChatGroq(model="llama-3.3-70b-versatile", api_key=key, temperature=0.3)
    except Exception:  # noqa: BLE001
        return None


def _agent_prompt(agent: str, topic: str, prior: str) -> str:
    """Return the prompt for a given agent."""
    if agent == "Researcher":
        return (f"You are a market research analyst. Research this topic and "
                f"provide 5 key facts/data points:\nTopic: {topic}\n"
                "Return as bullet points.")
    if agent == "Writer":
        return ("You are a business writer. Using this research, write a "
                "professional report (300 words) in Indonesian:\n"
                f"Research: {prior}\nStructure: Executive Summary, Key Findings, "
                "Recommendation.")
    return ("You are an editor. Review this report for clarity and grammar. "
            f"Return the polished version:\n{prior}")


def run_pipeline(topic: str, llm, placeholder) -> dict:
    """Run the 3-agent pipeline with live tracking and persistence."""
    token = generate_session_token()[:16]
    session_id = db.create_session(token, topic)
    statuses = {a: "pending" for a in AGENTS}

    def render():
        placeholder.markdown(
            pipeline_html([(a, statuses[a]) for a in AGENTS]),
            unsafe_allow_html=True)

    render()
    outputs = {}
    prior = topic
    start_all = time.perf_counter()
    for order, agent in enumerate(AGENTS, 1):
        statuses[agent] = "running"
        render()
        prompt = _agent_prompt(agent, topic, prior)
        t0 = time.perf_counter()
        try:
            out = llm.invoke(prompt).content
            status = "done"
        except Exception as exc:  # noqa: BLE001
            out = f"Error: {exc}"
            status = "error"
        ms = (time.perf_counter() - t0) * 1000
        db.add_step(session_id, agent, order, prompt[:2000], out, ms, status)
        outputs[agent] = out
        statuses[agent] = status
        render()
        if status == "error":
            db.finalize_session(session_id, out, time.perf_counter() - start_all, "error")
            return {"session_id": session_id, "outputs": outputs, "error": True}
        prior = out
    total = time.perf_counter() - start_all
    db.finalize_session(session_id, outputs["Editor"], total, "completed")
    db.add_log("research", f"{topic} ({total:.1f}s)")
    return {"session_id": session_id, "outputs": outputs, "error": False,
            "total": total}


def session_export_json(session_id: int) -> bytes:
    """Build a JSON export for a session and its steps."""
    sess = db.get_session(session_id) or {}
    steps = db.get_steps(session_id).to_dict("records")
    return json.dumps({"session": sess, "steps": steps}, indent=2,
                      ensure_ascii=False).encode("utf-8")


# --------------------------------------------------------------------------- #
# UI
# --------------------------------------------------------------------------- #
llm = get_llm()
render_header("🤖 Multi-Agent Research System",
              "Researcher → Writer → Editor · live pipeline · v2.0 Cyan Research")
if llm is None:
    st.info("ℹ️ GROQ_API_KEY not set — running the pipeline is disabled. The "
            "research history browser and export remain available.")

tab_run, tab_history = st.tabs(["🚀 Run Pipeline", "🗂️ History"])

# --------------------------------------------------------------------------- #
# TAB — Run
# --------------------------------------------------------------------------- #
with tab_run:
    topic = st.text_input("📌 Research topic:",
                          "Tren jasa rope access di Jakarta 2024")
    pipeline_ph = st.empty()
    pipeline_ph.markdown(
        pipeline_html([(a, "pending") for a in AGENTS]), unsafe_allow_html=True)

    if st.button("🔥 Run Research Pipeline", type="primary", disabled=llm is None) and topic:
        result = run_pipeline(sanitize_input(topic, 500), llm, pipeline_ph)
        outputs = result["outputs"]
        if result.get("error"):
            st.error("Pipeline stopped due to an agent error (see steps below).")
        else:
            st.success(f"Pipeline complete in {result['total']:.1f}s.")
        t1, t2, t3 = st.tabs(["📊 Research", "📝 Draft Report", "✅ Final Edit"])
        with t1:
            st.markdown(outputs.get("Researcher", "—"))
        with t2:
            st.markdown(outputs.get("Writer", "—"))
        with t3:
            final = outputs.get("Editor", "—")
            st.markdown(final)

        st.divider()
        st.subheader("🔬 Step Detail Viewer")
        steps = db.get_steps(result["session_id"])
        for _, s in steps.iterrows():
            with st.expander(f"Step {s['step_order']} · {s['agent_name']} · "
                             f"{s['execution_time_ms']:.0f} ms · {s['status']}"):
                st.markdown("**Input (prompt):**")
                st.code(s["input_data"][:1500])
                st.markdown("**Output:**")
                st.markdown(s["output_data"])

        st.divider()
        sid = result["session_id"]
        final = outputs.get("Editor", "")
        e1, e2, e3 = st.columns(3)
        e1.download_button("⬇️ Markdown", final.encode("utf-8"),
                           file_name="report.md", mime="text/markdown",
                           use_container_width=True)
        e2.download_button("⬇️ TXT", final.encode("utf-8"),
                           file_name="report.txt", mime="text/plain",
                           use_container_width=True)
        e3.download_button("⬇️ JSON", session_export_json(sid),
                           file_name="research_session.json",
                           mime="application/json", use_container_width=True)

# --------------------------------------------------------------------------- #
# TAB — History
# --------------------------------------------------------------------------- #
with tab_history:
    st.subheader("🗂️ Research History")
    sessions = db.get_sessions()
    if sessions.empty:
        st.caption("No research sessions yet.")
    else:
        hc1, hc2 = st.columns([3, 1])
        hc1.metric("Sessions", len(sessions))
        if hc2.button("🗑️ Clear history", use_container_width=True):
            db.clear_sessions()
            st.rerun()
        st.dataframe(
            sessions[["id", "timestamp", "topic", "status", "total_time_seconds"]],
            use_container_width=True, hide_index=True)
        sel = st.selectbox(
            "View a session", sessions["id"].tolist(),
            format_func=lambda i: sessions.loc[sessions["id"] == i, "topic"].iloc[0])
        sess = db.get_session(int(sel))
        if sess:
            st.markdown(f"#### {sess['topic']}")
            st.caption(f"Status: {sess['status']} · "
                       f"{sess.get('total_time_seconds') or 0:.1f}s total")
            st.markdown(sess.get("final_output") or "_No final output_")
            steps = db.get_steps(int(sel))
            for _, s in steps.iterrows():
                with st.expander(f"Step {s['step_order']} · {s['agent_name']} · "
                                 f"{s['execution_time_ms']:.0f} ms"):
                    st.markdown(s["output_data"])
            ec1, ec2 = st.columns(2)
            ec1.download_button("⬇️ Final (MD)",
                                (sess.get("final_output") or "").encode("utf-8"),
                                file_name=f"session_{sel}.md", mime="text/markdown",
                                use_container_width=True)
            ec2.download_button("⬇️ Session (JSON)", session_export_json(int(sel)),
                                file_name=f"session_{sel}.json",
                                mime="application/json", use_container_width=True)

render_footer()
