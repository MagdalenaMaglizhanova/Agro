import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

st.set_page_config(page_title="AgroLab", page_icon="🌱")

st.title("🌱 AgroLab: Спаси реколтата чрез данни")

# -----------------------------
# 1. DATA (учениците го попълват)
# -----------------------------
st.header("📊 Данни за времето и почвата")

data = pd.read_csv("cucumber_data.csv")

st.write("📄 Вашият dataset:")
st.dataframe(data)

# -----------------------------
# 2. ML MODEL
# -----------------------------
X = data[["temp", "rain", "sun", "ph", "irrigation", "fertilizer"]]
y = data["yield"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# -----------------------------
# 3. INPUT (решения на ученика)
# -----------------------------
st.header("🎮 Вземи решения като фермер")

temp = st.slider("🌡 Температура", 10, 40, 25)
rain = st.slider("🌧 Валежи", 0, 100, 30)
sun = st.slider("☀ Слънце", 0, 12, 8)
ph = st.slider("🧪 pH на почвата", 4.0, 8.0, 6.5)

irrigation = st.slider("💧 Вода (литра/декар)", 0, 5000, 2000)
fertilizer = st.slider("🧪 Тор (кг/декар)", 0, 200, 50)

# -----------------------------
# 4. AI PREDICTION
# -----------------------------
input_data = np.array([[temp, rain, sun, ph, irrigation, fertilizer]])
yield_pred = model.predict(input_data)[0]

# -----------------------------
# 5. ECONOMIC MODEL (ФИЗИКА + РЕАЛЕН ЖИВОТ)
# -----------------------------
water_cost = irrigation * 0.002   # цена на вода
fert_cost = fertilizer * 2         # цена на тор

total_cost = water_cost + fert_cost

revenue = yield_pred * 2.2
profit = revenue - total_cost - 2000

# -----------------------------
# 6. RANDOM EVENT
# -----------------------------
events = [
    "☀ Гореща вълна",
    "🌧 Суша",
    "🐛 Вредители",
    "🌤 Перфектен сезон"
]

event = np.random.choice(events)
st.header("⚠ Събитие")
st.info(event)

if event == "☀ Гореща вълна":
    yield_pred *= 0.8
elif event == "🌧 Суша":
    yield_pred *= 0.7
elif event == "🐛 Вредители":
    yield_pred *= 0.6
else:
    yield_pred *= 1.1

# -----------------------------
# 7. RESULT
# -----------------------------
st.header("🏁 Резултат")

st.success(f"🥒 Добив: {int(yield_pred)} kg/decare")
st.write(f"💰 Приход: {int(revenue)} лв")
st.write(f"💸 Разходи: {int(total_cost)} лв")

if profit > 0:
    st.balloons()
    st.success(f"🏆 Поздравления! Печалба: {int(profit)} лв")
else:
    st.error(f"📉 Провал! Загуба: {int(profit)} лв")

# -----------------------------
# 8. EXPLANATION (БИОЛОГИЯ + ФИЗИКА)
# -----------------------------
st.header("🧠 Анализ")

if temp < 18:
    st.write("❄ Ниска температура забавя растежа")
elif temp > 30:
    st.write("🔥 Висока температура причинява стрес")

if ph < 6:
    st.write("🧪 Кисела почва → слаб растеж")
else:
    st.write("🌱 Подходяща почва")

# -----------------------------
# 9. GRAPH
# -----------------------------
st.header("📈 Анализ на данни")

fig, ax = plt.subplots()
ax.scatter(data["temp"], data["yield"])
ax.set_xlabel("Температура")
ax.set_ylabel("Добив")

st.pyplot(fig)
