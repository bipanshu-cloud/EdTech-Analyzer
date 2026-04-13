"""
simulate_data.py
Generates a realistic dataset of 500-1000 students for the EdTech drop-off analysis.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

def simulate_students(n=750):
    user_ids = [f"USR_{str(i).zfill(4)}" for i in range(1, n + 1)]

    # ~35% conversion rate (realistic for edtech free trials)
    conversion_prob = np.random.random(n)
    converted = (conversion_prob < 0.35).astype(int)

    # Converted users have better engagement patterns
    sessions = np.where(
        converted == 1,
        np.random.negative_binomial(8, 0.4, n).clip(3, 60),
        np.random.negative_binomial(2, 0.5, n).clip(1, 20)
    )

    time_spent = np.where(
        converted == 1,
        sessions * np.random.normal(22, 7, n),
        sessions * np.random.normal(10, 5, n)
    ).clip(5, 900).astype(int)

    lessons_completed = np.where(
        converted == 1,
        np.random.normal(12, 4, n).clip(4, 30),
        np.random.normal(3, 2, n).clip(0, 10)
    ).astype(int)

    last_active_day = np.where(
        converted == 1,
        np.random.choice(range(1, 15), n),
        np.random.choice(range(1, 30), n)  # uniform for dropped users
    )

    onboarding_completed = np.where(
        converted == 1,
        np.random.choice([0, 1], n, p=[0.05, 0.95]),
        np.random.choice([0, 1], n, p=[0.55, 0.45])
    )

    device_type = np.random.choice(["mobile", "desktop", "tablet"], n, p=[0.5, 0.38, 0.12])

    course_category = np.random.choice(
        ["coding", "data_science", "design", "marketing", "language"],
        n, p=[0.30, 0.25, 0.20, 0.15, 0.10]
    )

    support_tickets = np.where(
        converted == 1,
        np.random.poisson(0.3, n),
        np.random.poisson(0.8, n)
    ).clip(0, 5)

    notifications_enabled = np.where(
        converted == 1,
        np.random.choice([0, 1], n, p=[0.2, 0.8]),
        np.random.choice([0, 1], n, p=[0.6, 0.4])
    )

    df = pd.DataFrame({
        "user_id": user_ids,
        "sessions": sessions,
        "time_spent_mins": time_spent,
        "lessons_completed": lessons_completed,
        "last_active_day": last_active_day,
        "onboarding_completed": onboarding_completed,
        "device_type": device_type,
        "course_category": course_category,
        "support_tickets": support_tickets,
        "notifications_enabled": notifications_enabled,
        "conversion_status": converted
    })

    return df


if __name__ == "__main__":
    df = simulate_students(750)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/students.csv", index=False)
    print(f"✅ Dataset saved: {len(df)} students")
    print(f"   Converted: {df['conversion_status'].sum()} ({df['conversion_status'].mean()*100:.1f}%)")
    print(df.describe())
