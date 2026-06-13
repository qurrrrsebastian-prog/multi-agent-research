# Multi-Agent Research System — Gemini Powered

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Gemini](https://img.shields.io/badge/Gemini-1.5_Flash-green)

## 📌 Deskripsi
Multi-agent AI system untuk riset otomatis. 3 agent bekerja sequential: Researcher (kumpulkan data) → Writer (tulis laporan) → Editor (polish & finalisasi).

## 🎯 Fitur
- Input topik → output laporan profesional
- 3-agent pipeline dengan role spesifik
- Download report dalam format Markdown
- Streamlit UI untuk monitoring tiap agent step

## 🛠️ Tech Stack
- Python, Streamlit, LangChain, Gemini API

## 🚀 Cara Menjalankan

```bash
$env:GEMINI_API_KEY="AQ....YOUR_KEY_HERE...."
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
