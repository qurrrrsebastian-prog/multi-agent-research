# Project #15 — Multi-Agent Research System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=chainlink&logoColor=white" />
  <img src="https://img.shields.io/badge/Gemini%20API-4285F4?style=flat&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" />
</p>

> Pipeline 3 AI agents: Researcher → Writer → Editor. Riset otomatis dari topik ke artikel final yang terstruktur.

---

## Demo Langsung

[![Deploy to Streamlit Cloud](https://img.shields.io/badge/Deploy-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://share.streamlit.io/deploy?repository=qurrrrsebastian-prog/multi-agent-research)

**Tech Stack:** `LangChain` · `Google Gemini API` · `Multi-Agent Pipeline` · `Streamlit`

---

## Fitur

| Fitur | Status |
|-------|--------|
| 3-agent sequential pipeline | ✅ |
| Researcher: data gathering | ✅ |
| Writer: drafting content | ✅ |
| Editor: final polish | ✅ |
| Export hasil (Markdown/TXT) | ✅ |
| Progress tracking real-time | ✅ |
| Tema gelap AVA purple | ✅ |

---

## Cara Menjalankan

```bash
git clone https://github.com/qurrrrsebastian-prog/multi-agent-research.git
cd multi-agent-research
pip install -r requirements.txt
$env:GEMINI_API_KEY="your_api_key_here"
streamlit run app.py
```

## Deploy ke Streamlit Cloud (GRATIS)

1. [share.streamlit.io](https://share.streamlit.io) → Login GitHub
2. **New app** → Pilih repo ini
3. Tambahkan secret: `GEMINI_API_KEY`
4. **Deploy**

---

## Arsitektur Agent

```
User Input (Topik)
    ↓
┌─────────────┐   ┌──────────────┐   ┌───────────┐
│  Researcher  │ → │   Writer     │ → │  Editor   │
│ (Data hunt)  │   │ (Drafting)   │   │ (Polish)  │
└─────────────┘   └──────────────┘   └───────────┘
                                          ↓
                                    Final Output
```

---

## Struktur Project

```
multi-agent-research/
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
├── .streamlit/
│   └── config.toml    # AVA purple branding
├── .gitignore
└── LICENSE            # MIT License
```

---

**Dibuat oleh:** [Avatar Putra Sigit](https://github.com/qurrrrsebastian-prog) · Founder @AVA.Group
