import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Agro Climate Lab", page_icon="🌱")

st.title("🌱 Agro Climate Lab – Реални климатични статистики")

# -----------------------------
# 1. РЕГИОН (FIXED)
# -----------------------------
st.header("🗺 Избор на регион")

regions = {
    "Село Труд": (42.25, 24.78),
    "Пловдив": (42.14, 24.75),
    "София": (42.70, 23.32),
    "Варна": (43.21, 27.91)
}

region_name = st.selectbox("Избери място", list(regions.keys()))
lat, lon = regions[region_name]

st.info(f"📍 Избран регион: {region_name}")

# -----------------------------
# 2. API ЗА ДАННИ
# -----------------------------
st.header("🌦 Данни за месец (Юли)")

url = (
    "https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={lat}&longitude={lon}"
    "&start_date=2025-07-01"
    "&end_date=2025-07-31"
    "&daily=temperature_2m_mean,precipitation_sum"
    "&timezone=Europe%2FSofia"
)

try:
    response = requests.get(url, timeout=10)
    data_json = response.json()

    if "daily" not in data_json:
        st.error("❌ Няма данни от API")
        st.stop()

    temps = data_json["daily"]["temperature_2m_mean"]
    rain = data_json["daily"]["precipitation_sum"]
    dates = data_json["daily"]["time"]

    df = pd.DataFrame({
        "date": dates,
        "temp": temps,
        "rain": rain
    })

    st.dataframe(df)

except Exception as e:
    st.error(f"❌ Грешка при зареждане на данни: {e}")
    st.stop()

# -----------------------------
# 3. СТАТИСТИКА
# -----------------------------
avg_temp = float(np.mean(temps))
total_rain = float(np.sum(rain))

st.header("📈 Статистика")

st.metric("Средна температура", f"{avg_temp:.1f} °C")
st.metric("Общи валежи", f"{total_rain:.1f} mm")

# -----------------------------
# 4. AI МОДЕЛ (STABLE)
# -----------------------------
train = pd.DataFrame({
    "temp": [18, 22, 25, 30, 33, 15],
    "rain": [80, 50, 30, 10, 5, 90],
    "good_month": [1, 1, 1, 0, 0, 1]
})

X = train[["temp", "rain"]]
y = train["good_month"]

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

prediction = model.predict(np.array([[avg_temp, total_rain]]))[0]

# -----------------------------
# 5. AI ЗАКЛЮЧЕНИЕ
# -----------------------------
st.header("🤖 AI анализ")

if prediction == 1:
    st.success("🌱 Месецът е ПОДХОДЯЩ за краставици")
else:
    st.error("⚠ Месецът НЕ е подходящ за оптимален добив")

# -----------------------------
# 6. STEM ОБЯСНЕНИЕ
# -----------------------------
st.header("🧠 Обяснение (Биология + Физика)")

if avg_temp > 30:
    st.write("🔥 Висока температура → повече изпарение → нужда от напояване")

elif avg_temp < 18:
    st.write("❄ Ниска температура → забавен растеж")

else:
    st.write("🌱 Температурата е в оптимален диапазон за фотосинтеза")

if total_rain < 20:
    st.write("🌧 Засушаване → риск за растенията")
elif total_rain > 100:
    st.write("🌊 Прекалено много валежи → риск от загниване")

st.write("⚛ Данните са реални исторически климатични наблюдения (Open-Meteo API).")
