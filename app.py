import streamlit as st
import numpy as np

st.set_page_config(page_title="Спаси реколтата", page_icon="🌱")

st.title("🌱 СПАСИ РЕКОЛТАТА – STEM ИГРА")

# -----------------------
# 1. ВХОДНИ ДАННИ
# -----------------------
st.header("📊 Данни за региона")

temp = st.number_input("🌡 Средна температура", 0, 45, 25)
rain = st.number_input("🌧 Валежи", 0, 200, 40)
soil = st.selectbox("🧪 Почва", ["Чернозем", "Пясъчна", "Глинеста"])
sun = st.number_input("☀ Слънчеви дни", 0, 30, 10)

# Анализ
st.header("🧠 Анализ на климата")

score = 0

if 20 <= temp <= 30:
    st.success("Температурата е подходяща")
    score += 30
else:
    st.warning("Температурата е рискова")
    score -= 20

if rain > 30:
    st.info("Добри валежи")
    score += 20
else:
    st.warning("Суша риск")
    score -= 20

if sun > 8:
    score += 20

# -----------------------
# 2. ЗАСАЖДАНЕ
# -----------------------
st.header("🌱 Засаждане")

plant_time = st.radio("Кога засаждаш?", ["Април", "Май", "Юни"])

if plant_time == "Април":
    score += 10
elif plant_time == "Юни":
    score -= 15

# -----------------------
# 3. РАЗХОДИ
# -----------------------
st.header("💰 Разходи")

seed_cost = st.slider("🌱 Разсад (лв)", 0, 500, 100)
fert = st.slider("🧪 Тор (лв)", 0, 1000, 300)
water = st.slider("💧 Вода (лв)", 0, 1000, 200)

budget_loss = seed_cost + fert + water

# -----------------------
# 4. ПОЧВА
# -----------------------
st.header("🧪 Почва анализ")

if soil == "Чернозем":
    score += 40
    yield_base = 7000
elif soil == "Глинеста":
    score += 20
    yield_base = 5000
else:
    score -= 10
    yield_base = 4000

# -----------------------
# 5. СЛУЧАЙНО СЪБИТИЕ
# -----------------------
st.header("⚠ Събитие")

event = np.random.choice([
    "☀ Гореща вълна",
    "🌩 Градушка",
    "🐛 Вредители",
    "🌧 Дъждовно лято"
])

st.info(event)

if event == "☀ Гореща вълна":
    score -= 20
elif event == "🌩 Градушка":
    score -= 50
elif event == "🐛 Вредители":
    score -= 30
else:
    score += 10

# -----------------------
# 6. ДОБИВ
# -----------------------
yield_final = yield_base * (1 + score / 100)

# -----------------------
# 7. ФИНАЛ
# -----------------------
st.header("🏁 РЕЗУЛТАТ")

profit = yield_final * 2 - budget_loss

st.success(f"🥒 Добив: {int(yield_final)} kg")

st.write(f"💰 Разходи: {budget_loss} лв")
st.write(f"📈 Печалба: {int(profit)} лв")

if profit > 5000:
    st.balloons()
    st.success("🏆 Поздравления! Спаси реколтата!")
elif profit > 0:
    st.info("🙂 Добър резултат")
else:
    st.error("📉 Провал – реколтата е загубена")
