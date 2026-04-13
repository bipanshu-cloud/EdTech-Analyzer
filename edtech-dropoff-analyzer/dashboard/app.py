"""
app.py  –  EdTech Drop-off Analyzer  |  Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import json
import sys, os

sys.path.insert(0, os.path.dirname(__file__))

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EdTech Drop-off Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.main { background: #0d0f14; }

.metric-card {
    background: linear-gradient(135deg, #1a1d27 0%, #232639 100%);
    border: 1px solid #2e3150;
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-2px); }
.metric-value { font-size: 2.4rem; font-weight: 700; color: #7c6dfa; }
.metric-label { font-size: 0.85rem; color: #8b92a8; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

.insight-card {
    background: linear-gradient(135deg, #1a1d27 0%, #1f2235 100%);
    border-left: 4px solid #7c6dfa;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.insight-title { font-weight: 600; color: #e8eaf0; font-size: 1rem; margin-bottom: 6px; }
.insight-body { color: #8b92a8; font-size: 0.9rem; line-height: 1.5; }

.section-header {
    font-size: 1.3rem;
    font-weight: 600;
    color: #e8eaf0;
    border-bottom: 1px solid #2e3150;
    padding-bottom: 8px;
    margin-bottom: 20px;
}

.ai-response {
    background: linear-gradient(135deg, #12141e, #1a1040);
    border: 1px solid #7c6dfa44;
    border-radius: 12px;
    padding: 20px;
    color: #c8cbdb;
    line-height: 1.7;
    font-size: 0.95rem;
}
.ai-badge {
    display: inline-block;
    background: #7c6dfa22;
    color: #7c6dfa;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 10px;
    letter-spacing: 0.1em;
}

.funnel-step {
    background: linear-gradient(135deg, #1a1d27, #232639);
    border: 1px solid #2e3150;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    margin-bottom: 8px;
}
.funnel-count { font-size: 1.8rem; font-weight: 700; color: #7c6dfa; }
.funnel-label { font-size: 0.8rem; color: #8b92a8; text-transform: uppercase; }
.funnel-pct { font-size: 0.85rem; color: #e05c5c; margin-top: 4px; }

stButton>button {
    background: linear-gradient(135deg, #7c6dfa, #9d6dfa) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(base, "data/students.csv"))
    with open(os.path.join(base, "analysis/insights.json")) as f:
        insights = json.load(f)
    return df, insights

df, ins = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 EdTech Analyzer")
    st.markdown("---")
    page = st.radio("Navigate", [
        "📊 Overview",
        "🔽 Funnel Analysis",
        "💡 Insights & AI",
        "🧪 Recommendations"
    ])

    st.markdown("---")
    st.markdown("**Dataset**")
    st.markdown(f"- `{ins['total_users']}` students")
    st.markdown(f"- `{ins['conversion_rate']}%` conversion rate")
    st.markdown(f"- `{ins['converted']}` paid / `{ins['dropped']}` dropped")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – Overview
# ══════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    st.markdown("# 📊 EdTech Drop-off Dashboard")
    st.markdown("*Investigating why students don't convert after the free trial*")
    st.markdown("---")

    # KPI row
    cols = st.columns(4)
    kpis = [
        (ins["total_users"], "Total Students"),
        (f"{ins['conversion_rate']}%", "Conversion Rate"),
        (ins["dropped"], "Dropped Users"),
        (ins["key_stats_for_llm"]["ghost_users_pct"], "Ghost Users %"),
    ]
    for col, (val, label) in zip(cols, kpis):
        col.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{val}</div>
            <div class='metric-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Converted vs Dropped comparison
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-header'>Behaviour: Converted vs Dropped</div>", unsafe_allow_html=True)
        comp = pd.DataFrame({
            "Metric": ["Sessions", "Time Spent (min)", "Lessons Completed", "Last Active Day"],
            "Dropped": [
                ins["group_means"]["dropped"]["sessions"],
                ins["group_means"]["dropped"]["time_spent_mins"],
                ins["group_means"]["dropped"]["lessons_completed"],
                ins["group_means"]["dropped"]["last_active_day"],
            ],
            "Converted": [
                ins["group_means"]["converted"]["sessions"],
                ins["group_means"]["converted"]["time_spent_mins"],
                ins["group_means"]["converted"]["lessons_completed"],
                ins["group_means"]["converted"]["last_active_day"],
            ],
        })
        st.dataframe(comp, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("<div class='section-header'>Engagement Segments</div>", unsafe_allow_html=True)
        seg_df = pd.DataFrame(ins["segments"])
        seg_df.columns = ["Segment", "Users", "Conversion %"]
        st.dataframe(seg_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("<div class='section-header'>Course Category Performance</div>", unsafe_allow_html=True)
    cat_df = pd.DataFrame(ins["category_performance"])
    cat_df = cat_df.rename(columns={"course_category": "Category", "users": "Users", "conversion_rate": "Conv. Rate %"})
    cat_df = cat_df.sort_values("Conv. Rate %", ascending=False)
    st.dataframe(cat_df, use_container_width=True, hide_index=True)

    # Device & notifications
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div class='section-header'>Conversion by Device</div>", unsafe_allow_html=True)
        dev_df = pd.DataFrame(list(ins["device_conversion"].items()), columns=["Device", "Conv. Rate"])
        dev_df["Conv. Rate %"] = (dev_df["Conv. Rate"] * 100).round(1)
        st.dataframe(dev_df[["Device", "Conv. Rate %"]], use_container_width=True, hide_index=True)

    with col4:
        st.markdown("<div class='section-header'>Notifications Impact</div>", unsafe_allow_html=True)
        notif = ins["notification_conversion"]
        notif_df = pd.DataFrame({
            "Status": ["Notifications OFF", "Notifications ON"],
            "Conv. Rate %": [
                round(notif["disabled"] * 100, 1),
                round(notif["enabled"] * 100, 1)
            ]
        })
        st.dataframe(notif_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – Funnel Analysis
# ══════════════════════════════════════════════════════════════════════════════
elif "Funnel" in page:
    st.markdown("# 🔽 Funnel Drop-off Analysis")
    st.markdown("*Where exactly are students leaving the free trial journey?*")
    st.markdown("---")

    funnel = ins["funnel"]
    steps = list(funnel.keys())
    values = list(funnel.values())

    cols = st.columns(len(steps))
    for i, (col, step, val) in enumerate(zip(cols, steps, values)):
        prev = values[i - 1] if i > 0 else val
        pct = f"▼ {round((1 - val/prev)*100, 1)}% drop" if i > 0 else "Entry Point"
        col.markdown(f"""
        <div class='funnel-step'>
            <div class='funnel-count'>{val:,}</div>
            <div class='funnel-label'>{step}</div>
            <div class='funnel-pct'>{pct}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Drop-off Rates Between Stages")

    drop_data = []
    for i in range(1, len(steps)):
        drop_pct = round((1 - values[i] / values[i - 1]) * 100, 1)
        drop_data.append({
            "Stage Transition": f"{steps[i-1]} → {steps[i]}",
            "Users Lost": values[i - 1] - values[i],
            "Drop-off %": drop_pct,
            "Severity": "🔴 Critical" if drop_pct > 30 else "🟡 High" if drop_pct > 15 else "🟢 Low"
        })

    drop_df = pd.DataFrame(drop_data)
    st.dataframe(drop_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### Onboarding Completion Impact")
    ob = ins["onboarding_conversion"]
    st.markdown(f"""
    | Group | Conversion Rate |
    |---|---|
    | ❌ Did NOT complete onboarding | **{ob['not_completed']*100:.1f}%** |
    | ✅ Completed onboarding | **{ob['completed']*100:.1f}%** |
    | **Lift from onboarding** | **+{ins['key_stats_for_llm']['onboarding_lift_pct']}%** |
    """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – Insights & AI
# ══════════════════════════════════════════════════════════════════════════════
elif "Insights" in page:
    st.markdown("# 💡 Insights & AI Explanations")
    st.markdown("*Key findings with AI-powered plain-English explanations*")
    st.markdown("---")

    ks = ins["key_stats_for_llm"]

    insights_list = [
        {
            "title": "🚨 Onboarding is the #1 Drop-off Gate",
            "body": f"{ins['key_stats_for_llm']['funnel_onboard_dropoff_pct']}% of students never finish onboarding. Those who do are {ins['key_stats_for_llm']['onboarding_lift_pct']}% more likely to convert.",
            "prompt": f"We have an edtech platform. {ins['key_stats_for_llm']['funnel_onboard_dropoff_pct']}% of students never complete onboarding. Students who do complete onboarding are {ins['key_stats_for_llm']['onboarding_lift_pct']}% more likely to convert to paid. Explain why this happens and what a product manager should do about it. Be concise and actionable in 3-4 sentences."
        },
        {
            "title": "👻 34% of Users are Ghosts",
            "body": f"{ins['key_stats_for_llm']['ghost_users_pct']}% of students log only 1 session and disappear. Converted users average {round(ins['group_means']['converted']['sessions'], 1)} sessions vs {round(ins['group_means']['dropped']['sessions'], 1)} for dropped users.",
            "prompt": f"On our edtech platform, {ins['key_stats_for_llm']['ghost_users_pct']}% of users log only 1 session and never return. Converted users average {round(ins['group_means']['converted']['sessions'],1)} sessions while dropped users average {round(ins['group_means']['dropped']['sessions'],1)}. Why does this ghost-user pattern happen and what are 2-3 product interventions to fix it?"
        },
        {
            "title": "🔔 Notifications Drive +39% Conversion Lift",
            "body": f"Users with notifications enabled convert at {ins['notification_conversion']['enabled']*100:.1f}% vs {ins['notification_conversion']['disabled']*100:.1f}% — a massive {ins['key_stats_for_llm']['notification_lift_pct']}pt gap.",
            "prompt": f"On our edtech platform, users who enable push notifications convert at {ins['notification_conversion']['enabled']*100:.1f}% vs only {ins['notification_conversion']['disabled']*100:.1f}% for those who don't — a {ins['key_stats_for_llm']['notification_lift_pct']} percentage point lift. What does this tell us about user intent and engagement? What should we do with this insight?"
        },
        {
            "title": "📱 Mobile Users Convert Less",
            "body": f"Desktop converts at {ins['device_conversion'].get('desktop',0)*100:.1f}% while mobile is at {ins['device_conversion'].get('mobile',0)*100:.1f}%. With 50% of traffic on mobile, this is a big opportunity.",
            "prompt": f"Our edtech platform has 50% mobile traffic. Desktop users convert at {ins['device_conversion'].get('desktop',0)*100:.1f}%, but mobile users only at {ins['device_conversion'].get('mobile',0)*100:.1f}%. What are the most likely reasons for this gap and what should we prioritize to fix the mobile experience?"
        },
        {
            "title": "📚 Course Category Matters",
            "body": f"'{ks['top_category'].title()}' courses convert best, while '{ks['worst_category'].title()}' performs worst. Content difficulty and perceived ROI differ significantly.",
            "prompt": f"On our edtech platform, '{ks['top_category']}' courses have the highest conversion rate while '{ks['worst_category']}' courses perform worst. What factors likely explain this difference, and how should product and content teams respond?"
        },
    ]

    for insight in insights_list:
        st.markdown(f"""
        <div class='insight-card'>
            <div class='insight-title'>{insight['title']}</div>
            <div class='insight-body'>{insight['body']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🤖 Ask AI to Explain")
    st.markdown("Select an insight and let the AI explain it in plain English with product context.")

    selected = st.selectbox("Choose an insight to explain:", [i["title"] for i in insights_list])
    selected_insight = next(i for i in insights_list if i["title"] == selected)

    custom_q = st.text_input(
        "Or ask your own question:",
        placeholder="e.g. Why are students dropping off on mobile?"
    )

    if st.button("🧠 Generate AI Explanation"):
        prompt = custom_q if custom_q.strip() else selected_insight["prompt"]

        with st.spinner("Thinking..."):
            try:
                import requests
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 400,
                        "system": "You are a senior product manager and data analyst specialising in EdTech. Give concise, actionable insights grounded in the data. Avoid jargon. Be direct.",
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                data = response.json()
                answer = data["content"][0]["text"]
                st.markdown(f"""
                <div class='ai-response'>
                    <div class='ai-badge'>✨ AI INSIGHT</div>
                    <p>{answer}</p>
                </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"AI API error: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 – Recommendations
# ══════════════════════════════════════════════════════════════════════════════
elif "Recommendations" in page:
    st.markdown("# 🧪 Product Recommendations")
    st.markdown("*Experiments and improvements to reduce drop-off*")
    st.markdown("---")

    recs = [
        {
            "experiment": "Shorten & Gamify Onboarding",
            "hypothesis": "A 3-step onboarding (vs current) with a progress bar will increase completion by 25%.",
            "type": "A/B Test",
            "priority": "🔴 P0",
            "effort": "Medium",
            "expected_impact": "+8-12% conversion"
        },
        {
            "experiment": "Day-3 Re-engagement Email",
            "hypothesis": "Users inactive for 3 days receive a personalised email showing what they missed. Reduces ghost rate.",
            "type": "Triggered Campaign",
            "priority": "🔴 P0",
            "effort": "Low",
            "expected_impact": "-15% ghost users"
        },
        {
            "experiment": "Push Notification Permission Prompt",
            "hypothesis": "Showing a value-framed permission prompt after first lesson increases notification opt-in by 30%.",
            "type": "A/B Test",
            "priority": "🟡 P1",
            "effort": "Low",
            "expected_impact": "+5-7% conversion"
        },
        {
            "experiment": "Mobile-first Lesson Experience",
            "hypothesis": "Redesigning lesson UI for thumb-zone on mobile will increase session depth on mobile by 40%.",
            "type": "Product Redesign",
            "priority": "🟡 P1",
            "effort": "High",
            "expected_impact": "+10% mobile conversion"
        },
        {
            "experiment": "Coding Course 'Quick Win' Restructure",
            "hypothesis": "Leading with a 15-min project (not theory) in coding courses improves early engagement and perceived value.",
            "type": "Content A/B",
            "priority": "🟡 P1",
            "effort": "Medium",
            "expected_impact": "+15% coding conversion"
        },
        {
            "experiment": "Trial Extension for Engaged Non-Converters",
            "hypothesis": "Users with 5+ sessions who haven't converted get a 7-day extension offer — higher intent, lower CAC.",
            "type": "Targeted Offer",
            "priority": "🟢 P2",
            "effort": "Low",
            "expected_impact": "+3-5% conversion"
        },
    ]

    rec_df = pd.DataFrame(recs)
    rec_df = rec_df.rename(columns={
        "experiment": "Experiment",
        "hypothesis": "Hypothesis",
        "type": "Type",
        "priority": "Priority",
        "effort": "Effort",
        "expected_impact": "Expected Impact"
    })

    st.dataframe(rec_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 📐 Measurement Framework")
    st.markdown("""
    | Metric | Current | Target | Timeframe |
    |---|---|---|---|
    | Onboarding completion rate | ~61% | 80% | 30 days |
    | Ghost user rate | 34% | 20% | 60 days |
    | Mobile conversion rate | Low | Desktop parity | 90 days |
    | Notification opt-in rate | ~54% | 70% | 30 days |
    | Overall conversion rate | 36% | 45% | 90 days |
    """)
