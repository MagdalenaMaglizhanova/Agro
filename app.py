import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Agro Data Lab", page_icon="🌱")

st.title("🌱 Agro Data Lab – Събиране и анализ на климатични данни")

# -----------------------------
# 1. ИЗБОР НА РЕГИОН
# -----------------------------
st.header("🗺 Избор на регион")

region = st.selectbox(
    "Избери район за изследване",
    ["Село Труд", "Пловдив", "София", "Варна", "Русе"]
)

st.info(f"Избран регион: {region}")

# -----------------------------
# 2. СЪБИРАНЕ НА ДАННИ
# -----------------------------
st.header("📊 Климатични данни (въведени от ученици)")

temp = st.slider("🌡 Температура (°C)", -10, 45, 25)
rain = st.slider("🌧 Валежи (мм)", 0, 200, 40)
sun = st.slider("☀ Слънчеви часове", 0, 15, 8)
humidity = st.slider("🌫 Влажност (%)", 0, 100, 60)

# -----------------------------
# 3. СЪЗДАВАНЕ НА DATASET
# -----------------------------
data = pd.DataFrame({
    "region": [region],
    "temp": [temp],
    "rain": [rain],
    "sun": [sun],
    "humidity": [humidity]
})

st.header("📄 Вашите статистически данни")
st.dataframe(data)

# -----------------------------
# 4. ML МОДЕЛ (AI)
# -----------------------------
# мини обучителен dataset (симулация)
train = pd.DataFrame({
    "temp": [20, 25, 30, 15, 10, 35],
    "rain": [40, 30, 20, 60, 80, 10],
    "sun": [8, 9, 10, 5, 4, 11],
    "humidity": [60, 55, 50, 70, 80, 40],
    "good_season": [1, 1, 0, 1, 0, 0]
})

X = train[["temp", "rain", "sun", "humidity"]]
y = train["good_season"]

model = RandomForestClassifier()
model.fit(X, y)

# -----------------------------
# 5. AI PREDICTION
# -----------------------------
input_data = np.array([[temp, rain, sun, humidity]])
prediction = model.predict(input_data)[0]

# -----------------------------
# 6. РЕЗУЛТАТ
# -----------------------------
st.header("🤖 AI анализ")

if prediction == 1:
    st.success("🌱 Условията са ПОДХОДЯЩИ за краставици")
else:
    st.error("⚠ Условията НЕ са подходящи")

# -----------------------------
# 7. ОБЯСНЕНИЕ (БИОЛОГИЯ + ФИЗИКА)
# -----------------------------
st.header("🧠 Обяснение")

if temp > 30:
    st.write("🔥 Висока температура → стрес за растенията")
elif temp < 15:
    st.write("❄ Ниска температура → забавен растеж")
else:
    st.write("🌱 Оптимална температура")

if humidity > 80:
    st.write("🌫 Висока влажност → риск от болести")

if rain < 20:
    st.write("🌧 Суша → нужда от напояване")

st.write("⚛ Това е базиран на статистически модел AI анализ.")
