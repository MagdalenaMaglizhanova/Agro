import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Agro Climate Lab", page_icon="🌱")

st.title("🌱 Agro Climate Lab – Реални климатични статистики")

# -----------------------------
# 1. РЕГИОН
# -----------------------------
st.header("🗺 Избор на регион")

region = st.selectbox(
    "Избери място",
    {
        "Село Труд": (42.25, 24.78),
        "Пловдив": (42.14, 24.75),
        "София": (42.70, 23.32),
        "Варна": (43.21, 27.91)
    }
)

lat, lon = region

# -----------------------------
# 2. ВЗИМАНЕ НА ДАННИ (OPEN-METEO)
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

response = requests.get(url)
data_json = response.json()

temps = data_json["daily"]["temperature_2m_mean"]
rain = data_json["daily"]["precipitation_sum"]
dates = data_json["daily"]["time"]

df = pd.DataFrame({
    "date": dates,
    "temp": temps,
    "rain": rain
})

st.write("📊 Данни за юли:")
st.dataframe(df)

# -----------------------------
# 3. СТАТИСТИКА
# -----------------------------
avg_temp = np.mean(temps)
total_rain = np.sum(rain)

st.header("📈 Статистика")

st.metric("Средна температура", f"{avg_temp:.1f} °C")
st.metric("Общи валежи", f"{total_rain:.1f} mm")

# -----------------------------
# 4. AI МОДЕЛ (прост пример)
# -----------------------------
train = pd.DataFrame({
    "temp": [18, 22, 25, 30, 33, 15],
    "rain": [80, 50, 30, 10, 5, 90],
    "good_month": [1, 1, 1, 0, 0, 1]
})

X = train[["temp", "rain"]]
y = train["good_month"]

model = RandomForestClassifier()
model.fit(X, y)

prediction = model.predict([[avg_temp, total_rain]])[0]

# -----------------------------
# 5. AI ЗАКЛЮЧЕНИЕ
# -----------------------------
st.header("🤖 AI анализ на сезона")

if prediction == 1:
    st.success("🌱 Юли е ПОДХОДЯЩ за краставици в този регион")
else:
    st.error("⚠ Юли НЕ е подходящ за оптимален добив")

# -----------------------------
# 6. БИОЛОГИЯ + ФИЗИКА
# -----------------------------
st.header("🧠 Обяснение")

if avg_temp > 30:
    st.write("🔥 Високата температура увеличава изпарението → нужда от повече вода")

if total_rain < 20:
    st.write("🌧 Засушаване → риск за растежа")

if 20 <= avg_temp <= 28:
    st.write("🌱 Оптимална температура за фотосинтеза")

st.write("⚛ Данните са реални метеорологични наблюдения (Open-Meteo API).")
