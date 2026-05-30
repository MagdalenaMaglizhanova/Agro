import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AgroPredict",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AgroPredict")
st.subheader("Прогнозиране на добив от краставици")

# Зареждане на данните
data = pd.read_csv("cucumber_data.csv")

# Обучение на модела
X = data[["temp", "rain", "sun", "ph"]]
y = data["yield"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Sidebar
st.sidebar.header("Входни данни")

temp = st.sidebar.slider(
    "Средна температура (°C)",
    10,
    40,
    25
)

rain = st.sidebar.slider(
    "Валежи (мм)",
    0,
    100,
    30
)

sun = st.sidebar.slider(
    "Слънчеви часове",
    0,
    15,
    8
)

ph = st.sidebar.slider(
    "pH на почвата",
    4.0,
    8.0,
    6.5
)

# Прогноза
prediction = model.predict([[temp, rain, sun, ph]])[0]

st.metric(
    label="Очакван добив",
    value=f"{prediction:.0f} кг/декар"
)

# Биологична интерпретация
st.header("🧬 Анализ")

if temp < 18:
    st.warning("Температурата е ниска за оптимален растеж.")
elif temp > 30:
    st.warning("Температурата е твърде висока.")
else:
    st.success("Температурата е подходяща.")

if ph < 6:
    st.warning("Почвата е прекалено кисела.")
elif ph > 7:
    st.warning("Почвата е прекалено алкална.")
else:
    st.success("pH е подходящо за краставици.")

# Графика
st.header("📈 Исторически данни")

fig, ax = plt.subplots(figsize=(8, 4))

ax.scatter(data["temp"], data["yield"])

ax.set_xlabel("Температура")
ax.set_ylabel("Добив (кг/декар)")
ax.set_title("Температура срещу добив")

st.pyplot(fig)

# Данни
st.header("📊 Данни")

st.dataframe(data)

st.header("⚛️ Физика")

solar_energy = sun * 100

st.write(
    f"Оценена слънчева енергия: {solar_energy} условни единици"
)
