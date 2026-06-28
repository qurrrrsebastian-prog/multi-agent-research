"""ui_components.py — Reusable UI components.
Author: Avatar Putra Sigit | GitHub: qurrrrsebastian-prog
"""
import streamlit as st

PRIMARY = "#0891B2"
SECONDARY = "#22D3EE"

PORTFOLIO_LINKS = [
    ("#11 RAG Q&A", "https://github.com/qurrrrsebastian-prog/rag-document-qa"),
    ("#12 SQL Agent", "https://github.com/qurrrrsebastian-prog/text-to-sql-agent"),
    ("#13 YouTube", "https://github.com/qurrrrsebastian-prog/youtube-summarizer"),
    ("#14 Leads", "https://github.com/qurrrrsebastian-prog/lead-qualification-bot"),
    ("#15 Research", "https://github.com/qurrrrsebastian-prog/multi-agent-research"),
    ("#16 Jobs", "https://github.com/qurrrrsebastian-prog/autonomous-web-research"),
    ("#17 Email", "https://github.com/qurrrrsebastian-prog/ai-email-auto-responder"),
    ("#18 IoT", "https://github.com/qurrrrsebastian-prog/smart-water-iot-dashboard"),
    ("#19 RBAC", "https://github.com/qurrrrsebastian-prog/enterprise-rag-rbac"),
]

_STATUS_STYLE = {
    "done": ("#059669", "✓"),
    "running": ("#0891B2", "⟳"),
    "pending": ("#475569", "○"),
    "error": ("#DC2626", "✕"),
}


def render_header(title: str, subtitle: str, color: str = PRIMARY) -> None:
    """Render a gradient page header."""
    st.markdown(
        f"""
    <div style="background: linear-gradient(135deg, {color}22, {color}08);
        border-left: 4px solid {color}; border-radius: 8px; padding: 20px 24px; margin-bottom: 20px;">
        <h1 style="color: {color}; margin: 0; font-size: 28px;">{title}</h1>
        <p style="color: #94A3B8; margin: 8px 0 0 0; font-size: 14px;">{subtitle}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the portfolio footer with navigation and social links."""
    st.markdown("---")
    active = "#15 Research"
    nav_html = ""
    for label, url in PORTFOLIO_LINKS:
        is_active = label == active
        bg = f"{PRIMARY}33" if is_active else "#1C1F26"
        border = PRIMARY if is_active else "#334155"
        text = PRIMARY if is_active else "#94A3B8"
        weight = "600" if is_active else "400"
        nav_html += f'<a href="{url}" target="_blank" style="text-decoration:none;margin:3px;"><span style="background:{bg};border:1px solid {border};border-radius:6px;padding:3px 10px;font-size:11px;color:{text};font-weight:{weight};">{label}</span></a>'
    st.markdown(
        f"""<div style="text-align:center;margin-bottom:12px;">
            <p style="color:#94A3B8;font-size:11px;margin-bottom:8px;">🚀 PORTFOLIO NAVIGATION</p>
            <div style="display:flex;flex-wrap:wrap;justify-content:center;">{nav_html}</div>
        </div>
        <div style="text-align:center;color:#64748B;font-size:12px;padding:10px;">
            <p><a href="https://github.com/qurrrrsebastian-prog" target="_blank" style="color:{PRIMARY};text-decoration:none;">GitHub</a> · 
            <a href="https://www.linkedin.com/in/avatarputrasigit/" target="_blank" style="color:{PRIMARY};text-decoration:none;">LinkedIn</a> · 
            <a href="mailto:putraavaar@gmail.com" style="color:{PRIMARY};text-decoration:none;">Email</a></p>
            <p>Built with ❤️ by Avatar Putra Sigit | Founder @AVA.Group | © 2026</p>
        </div>""",
        unsafe_allow_html=True,
    )


def render_status_badge(label: str, color: str) -> None:
    """Render a small pill-style status badge."""
    st.markdown(
        f"""
    <span style="background: {color}22; color: {color}; border: 1px solid {color}44;
        border-radius: 12px; padding: 4px 12px; font-size: 12px; font-weight: 600;">{label}</span>
    """,
        unsafe_allow_html=True,
    )


def pipeline_html(stages) -> str:
    """Return HTML for a horizontal pipeline tracker."""
    boxes = []
    for i, (name, status) in enumerate(stages):
        color, icon = _STATUS_STYLE.get(status, _STATUS_STYLE["pending"])
        boxes.append(
            f"""<div style="flex:1; text-align:center; background:{color}14;
                border:2px solid {color}; border-radius:10px; padding:14px 8px; margin:0 4px;">
                <div style="font-size:22px; color:{color};">{icon}</div>
                <div style="color:#E2E8F0; font-weight:600; font-size:13px; margin-top:4px;">{name}</div>
                <div style="color:{color}; font-size:11px; text-transform:uppercase;">{status}</div>
            </div>""")
        if i < len(stages) - 1:
            arrow_color = SECONDARY if stages[i][1] == "done" else "#475569"
            boxes.append(
                f'<div style="align-self:center; color:{arrow_color}; '
                f'font-size:24px; padding:0 2px;">→</div>')
    return (f'<div style="display:flex; align-items:stretch; margin:12px 0;">'
            f'{"".join(boxes)}</div>')


def render_card(title: str, content: str, color: str = PRIMARY) -> None:
    """Render a titled content card."""
    st.markdown(
        f"""
    <div style="background: {color}11; border: 1px solid {color}33; border-radius: 10px;
        padding: 16px; margin: 8px 0;">
        <h4 style="color: {color}; margin: 0 0 8px 0;">{title}</h4>
        <p style="color: #CBD5E1; margin: 0; font-size: 13px;">{content}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )
