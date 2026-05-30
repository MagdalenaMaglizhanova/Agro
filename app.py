import streamlit as st
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Спаси реколтата AI", page_icon="🌱", layout="centered")

st.title("🌱🤖 СПАСИ РЕКОЛТАТА AI")
st.write("СТЕМ игра: фермерска симулация с изкуствен интелект")

# ---------------------------
# MINI DATASET (вграден)
# ---------------------------
data = pd.DataFrame({
    "temp": [25, 22, 18, 28, 30, 20, 24, 19, 27, 26],
    "rain": [30, 40, 15, 25, 20, 35, 28, 18, 32, 30],
    "sun":  [8, 7, 5, 10, 11, 6, 8, 5, 9, 8],
    "ph":   [6.5, 6.7, 5.8, 6.6, 6.5, 6.2, 6.3, 5.9, 6.7, 6.4],
    "yield":[6200,5900,3800,6800,7000,5000,6100,4200,6900,6500]
})

# ---------------------------
# ML MODEL (AI)
# ---------------------------
X = data[["temp", "rain", "sun", "ph"]]
y = data["yield"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# ---------------------------
# SESSION STATE
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "budget" not in st.session_state:
    st.session_state.budget = 5000

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("📊 Статус на фермата")
st.sidebar.write(f"💰 Бюджет: {st.session_state.budget} лв")
st.sidebar.write(f"📈 Сезони: {len(st.session_state.history)}")

# ---------------------------
# INPUTS (игра)
# ---------------------------
st.header("🎮 Настрой условията на сезона")

temp = st.slider("🌡 Температура (°C)", 10, 40, 25)
rain = st.slider("🌧 Валежи", 0, 100, 30)
sun = st.slider("☀ Слънчеви часове", 0, 12, 8)
ph = st.slider("🧪 pH на почвата", 4.0, 8.0, 6.5)

# ---------------------------
# EVENT SYSTEM
# ---------------------------
events = [
    "☀ Гореща вълна",
    "🌧 Силен дъжд",
    "🐛 Вредители",
    "🌤 Перфектно време",
    "❄ Слана"
]

event = random.choice(events)

st.header("⚠ Събитие за сезона")
st.info(event)

# ---------------------------
# AI PREDICTION
# ---------------------------
input_data = np.array([[temp, rain, sun, ph]])
prediction = model.predict(input_data)[0]

# event effects
if event == "☀ Гореща вълна":
    prediction *= 0.8
    st.warning("Жегата намалява добива")
elif event == "🌧 Силен дъжд":
    prediction *= 0.9
    st.warning("Прекалено много вода")
elif event == "🐛 Вредители":
    prediction *= 0.7
    st.error("Вредители унищожават част от реколтата")
elif event == "❄ Слана":
    prediction *= 0.6
    st.error("Сланата сериозно вреди на растенията")
else:
    st.success("Идеални условия за растеж!")

# ---------------------------
# RESULT
# ---------------------------
st.header("📊 AI ПРОГНОЗА")

st.success(f"🥒 Очакван добив: {int(prediction)} кг/декар")

revenue = prediction * 2
profit = revenue - 2000

st.write(f"💰 Очакван приход: {int(revenue)} лв")
st.write(f"📉 Печалба: {int(profit)} лв")

# ---------------------------
# BIOLOGY + PHYSICS EXPLANATION
# ---------------------------
st.header("🧠 Обяснение (Биология + Физика)")

if temp < 18:
    st.write("❄ Ниска температура забавя растежа на растенията.")
elif temp > 30:
    st.write("🔥 Висока температура причинява стрес и изпарение на вода.")
else:
    st.write("🌱 Оптимална температура за фотосинтеза.")

if ph < 6:
    st.write("🧪 Кисела почва намалява усвояването на хранителни вещества.")
elif ph > 7:
    st.write("🧪 Алкална почва също влияе негативно.")
else:
    st.write("🌱 Почвата е идеална за краставици.")

# Physics formula (simple energy idea)
energy = sun * 100
st.write(f"⚛ Слънчева енергия (модел): {energy} единици")

# ---------------------------
# SAVE HISTORY
# ---------------------------
st.session_state.history.append(prediction)

# ---------------------------
# GRAPH
# ---------------------------
st.header("📈 История на реколтата")

fig, ax = plt.subplots()
ax.plot(st.session_state.history, marker="o")
ax.set_title("Добив по сезони")
ax.set_xlabel("Сезон")
ax.set_ylabel("Кг/декар")

st.pyplot(fig)

# ---------------------------
# RESET
# ---------------------------
if st.button("🔄 Нов сезон"):
    st.session_state.history = []
    st.session_state.budget = 5000
    st.success("Започва нова фермерска игра!")
