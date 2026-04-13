"""
analysis.py
EDA and feature analysis for EdTech drop-off investigation.
Outputs a JSON insights file consumed by the dashboard.
"""

import pandas as pd
import numpy as np
import json
import os

def run_analysis(csv_path="data/students.csv"):
    df = pd.read_csv(csv_path)

    results = {}

    # ── 1. Basic stats ─────────────────────────────────────────────
    results["total_users"] = len(df)
    results["converted"] = int(df["conversion_status"].sum())
    results["dropped"] = int((df["conversion_status"] == 0).sum())
    results["conversion_rate"] = round(df["conversion_status"].mean() * 100, 1)

    # ── 2. Funnel stages ───────────────────────────────────────────
    signed_up = len(df)
    completed_onboarding = int(df["onboarding_completed"].sum())
    engaged = int((df["sessions"] >= 3).sum())
    converted = results["converted"]

    results["funnel"] = {
        "Signed Up": signed_up,
        "Completed Onboarding": completed_onboarding,
        "Engaged (3+ sessions)": engaged,
        "Converted": converted
    }

    # ── 3. Converted vs Dropped comparison ────────────────────────
    grp = df.groupby("conversion_status")[
        ["sessions", "time_spent_mins", "lessons_completed", "last_active_day"]
    ].mean().round(2)

    results["group_means"] = {
        "dropped": grp.loc[0].to_dict(),
        "converted": grp.loc[1].to_dict()
    }

    # ── 4. Onboarding impact ───────────────────────────────────────
    onboard_conv = df.groupby("onboarding_completed")["conversion_status"].mean().round(3)
    results["onboarding_conversion"] = {
        "not_completed": float(onboard_conv.get(0, 0)),
        "completed": float(onboard_conv.get(1, 0))
    }

    # ── 5. Device breakdown ────────────────────────────────────────
    device_conv = df.groupby("device_type")["conversion_status"].mean().round(3).to_dict()
    results["device_conversion"] = device_conv

    # ── 6. Notification impact ─────────────────────────────────────
    notif_conv = df.groupby("notifications_enabled")["conversion_status"].mean().round(3)
    results["notification_conversion"] = {
        "disabled": float(notif_conv.get(0, 0)),
        "enabled": float(notif_conv.get(1, 0))
    }

    # ── 7. Course category performance ────────────────────────────
    cat_conv = df.groupby("course_category").agg(
        users=("user_id", "count"),
        conversion_rate=("conversion_status", "mean")
    ).round(3).reset_index()
    cat_conv["conversion_rate"] = (cat_conv["conversion_rate"] * 100).round(1)
    results["category_performance"] = cat_conv.to_dict("records")

    # ── 8. Engagement segments ─────────────────────────────────────
    df["segment"] = pd.cut(
        df["sessions"],
        bins=[0, 1, 3, 7, 100],
        labels=["Ghost (1 session)", "Low (2-3)", "Medium (4-7)", "High (8+)"]
    )
    seg = df.groupby("segment", observed=True).agg(
        count=("user_id", "count"),
        conversion_rate=("conversion_status", "mean")
    ).reset_index()
    seg["conversion_rate"] = (seg["conversion_rate"] * 100).round(1)
    results["segments"] = seg.to_dict("records")

    # ── 9. Last active day distribution ───────────────────────────
    results["last_active_dist"] = {
        "dropped_avg": round(float(df[df["conversion_status"]==0]["last_active_day"].mean()), 1),
        "converted_avg": round(float(df[df["conversion_status"]==1]["last_active_day"].mean()), 1)
    }

    # ── 10. Key insights (rule-based, fed to LLM) ─────────────────
    onboard_lift = round(
        (results["onboarding_conversion"]["completed"] - results["onboarding_conversion"]["not_completed"]) * 100, 1
    )
    notif_lift = round(
        (results["notification_conversion"]["enabled"] - results["notification_conversion"]["disabled"]) * 100, 1
    )
    session_diff = round(
        results["group_means"]["converted"]["sessions"] - results["group_means"]["dropped"]["sessions"], 1
    )

    results["key_stats_for_llm"] = {
        "conversion_rate": results["conversion_rate"],
        "onboarding_lift_pct": onboard_lift,
        "notification_lift_pct": notif_lift,
        "session_gap": session_diff,
        "funnel_onboard_dropoff_pct": round((1 - completed_onboarding / signed_up) * 100, 1),
        "funnel_engage_dropoff_pct": round((1 - engaged / completed_onboarding) * 100, 1) if completed_onboarding else 0,
        "top_category": cat_conv.sort_values("conversion_rate", ascending=False).iloc[0]["course_category"],
        "worst_category": cat_conv.sort_values("conversion_rate").iloc[0]["course_category"],
        "ghost_users_pct": round(float(seg[seg["segment"]=="Ghost (1 session)"]["count"].values[0]) / signed_up * 100, 1)
    }

    os.makedirs("analysis", exist_ok=True)
    out_path = "analysis/insights.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Analysis complete → {out_path}")
    print(json.dumps(results["key_stats_for_llm"], indent=2))
    return results


if __name__ == "__main__":
    run_analysis()
