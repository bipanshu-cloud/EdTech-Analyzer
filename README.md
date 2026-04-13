# EdTech-Analyzer
# 🎓 EdTech Drop-off Analyzer

> An end-to-end AI-powered tool that investigates **why students stop using an EdTech platform after the free trial**.

---

## 🚀 Quick Start

```bash
# 1. Clone & install

cd edtech-dropoff-analyzer
pip install -r requirements.txt

# 2. Generate dataset
python data/simulate_data.py

# 3. Run analysis
python analysis/analysis.py

# 4. Launch dashboard
streamlit run dashboard/app.py
```

---

## 🏗️ Project Structure

```
edtech-dropoff-analyzer/
├── data/
│   ├── simulate_data.py      # Synthetic student dataset generator
│   └── students.csv          # Generated dataset (750 students)
├── analysis/
│   ├── analysis.py           # EDA + feature analysis
│   └── insights.json         # Pre-computed insights for dashboard
├── dashboard/
│   └── app.py                # Streamlit dashboard (4 pages)
├── requirements.txt
└── README.md
```

---

## 📊 What It Does

### 1. Problem Framing
Maps the complete user funnel:
```
Sign Up → Onboarding → Engagement → Conversion
```
Identifies critical drop-off points at each stage.

### 2. Dataset Simulation
Generates 750 realistic students with behavioural signals:
- `sessions`, `time_spent_mins`, `lessons_completed`
- `last_active_day`, `onboarding_completed`
- `device_type`, `course_category`, `notifications_enabled`
- `conversion_status` (target variable)

### 3. Data Analysis
- EDA with Pandas
- Converted vs. dropped user comparison
- Segment analysis (Ghost / Low / Medium / High engagement)
- Feature-level impact on conversion

### 4. Key Insights
1. **Onboarding is the #1 gate** — +53% conversion lift from completing it
2. **34% of users are ghosts** — log 1 session and vanish
3. **Notifications drive +39% lift** — opt-in is a strong intent signal
4. **Mobile converts less** — 50% of traffic, under-indexed in conversion
5. **Course category matters** — Language outperforms Coding significantly

### 5. Dashboard (Streamlit)
Four pages:
- 📊 **Overview** — KPIs, behavioural comparison, segment table
- 🔽 **Funnel Analysis** — visual drop-off at each stage
- 💡 **Insights & AI** — LLM-powered plain-English explanations
- 🧪 **Recommendations** — Prioritised experiments with hypotheses

### 6. AI Integration
Uses the Anthropic Claude API to explain any insight in plain English.
Select a pre-built insight or type your own question:
> "Why are users dropping off on mobile?"

### 7. Recommendations
6 prioritised product experiments:
- Shorter onboarding with gamification
- Day-3 re-engagement email
- Push notification permission prompt
- Mobile-first lesson redesign
- Coding course restructure
- Trial extension for high-intent non-converters

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data | Python, Pandas, NumPy |
| Dashboard | Streamlit |
| AI | Anthropic Claude API |
| Deployment | Streamlit Cloud / Render |

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to http://192.168.1.5:8501/


---


