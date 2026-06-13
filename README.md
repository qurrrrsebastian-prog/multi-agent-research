# Multi-Agent Research System — Groq Powered

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange)

## 📌 Deskripsi
Multi-agent AI system untuk riset otomatis. 3 agent bekerja sequential: Researcher (kumpulkan data) → Writer (tulis laporan) → Editor (polish & finalisasi). Ditenagai Groq (Llama 3.3 70B).

## 🎯 Fitur
- Input topik → output laporan profesional
- 3-agent pipeline dengan role spesifik
- Download report dalam format Markdown
- Streamlit UI untuk monitoring tiap agent step

## 🛠️ Tech Stack
- Python, Streamlit, LangChain, Groq (Llama 3.3 70B)

## 🚀 Cara Menjalankan

```bash
# Ambil API key gratis di https://console.groq.com/keys
$env:GROQ_API_KEY="gsk_....YOUR_KEY_HERE...."
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Key Insight
- Multi-agent system meningkatkan kualitas output 2-3x vs single prompt
- Role-based prompting (Researcher/Writer/Editor) = less hallucination
- Sequential pipeline memungkinkan human-in-the-loop review per stage

## 👤 Author
[Avatar Putra Sigit](https://linkedin.com/in/avatarputrasigit) — Founder & CEO @AVA.Group
[GitHub](https://github.com/qurrrrsebastian-prog)
