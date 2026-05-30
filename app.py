import streamlit as st
import random

st.set_page_config(page_title="Спаси реколтата!", page_icon="🌱")

st.title("🌱 СПАСИ РЕКОЛТАТА!")
st.write("СТЕМ игра: фермерска симулация")

# STATE
if "budget" not in st.session_state:
    st.session_state.budget = 5000
if "yield_score" not in st.session_state:
    st.session_state.yield_score = 5000
if "event" not in st.session_state:
    st.session_state.event = None
if "log" not in st.session_state:
    st.session_state.log = []

def event():
    return random.choice([
        "☀ Гореща вълна",
        "🌧 Порой",
        "❄ Слана",
        "🐛 Вредители",
        "🌤 Добро време"
    ])

# RESET
if st.button("🔄 Нов сезон"):
    st.session_state.budget = 5000
    st.session_state.yield_score = 5000
    st.session_state.event = None
    st.session_state.log = []
    st.success("Нов сезон започна!")

st.sidebar.title("📊 Статус")
st.sidebar.write("💰 Бюджет:", st.session_state.budget)
st.sidebar.write("🥒 Добив:", st.session_state.yield_score)

# PLANTING
st.header("1️⃣ Засаждане")
plant = st.radio("Кога садиш?", ["1 април", "15 април", "1 май"])

if st.button("Потвърди засаждане"):
    if plant == "1 април":
        st.session_state.yield_score -= 300
        st.session_state.log.append("❄ Ранно засаждане")
    elif plant == "1 май":
        st.session_state.yield_score -= 200
        st.session_state.log.append("☀ Късно засаждане")
    else:
        st.session_state.yield_score += 200
        st.session_state.log.append("🌱 Оптимално засаждане")

# WATER
st.header("2️⃣ Поливане")
water = st.radio("Поливане:", ["Малко", "Средно", "Много"])

if st.button("Полей"):
    if water == "Средно":
        st.session_state.yield_score += 300
        st.session_state.budget -= 300
    elif water == "Много":
        st.session_state.yield_score -= 100
        st.session_state.budget -= 600
    else:
        st.session_state.yield_score -= 200

# EVENT
st.header("3️⃣ Събитие")

if st.button("Генерирай събитие"):
    st.session_state.event = event()

if st.session_state.event:
    st.warning(st.session_state.event)

    if "Гореща" in st.session_state.event:
        st.session_state.yield_score -= 400
    elif "Слана" in st.session_state.event:
        st.session_state.yield_score -= 600
    elif "Вредители" in st.session_state.event:
        st.session_state.yield_score -= 500
    else:
        st.session_state.yield_score += 200

# RESULT
st.header("🏁 Край")

if st.button("Финализирай сезона"):
    revenue = st.session_state.yield_score * 2
    profit = revenue - (5000 - st.session_state.budget)

    st.success(f"🥒 Добив: {st.session_state.yield_score} кг")
    st.info(f"💰 Печалба: {profit} лв")

    if profit > 0:
        st.balloons()
        st.success("🏆 УСПЕХ!")
    else:
        st.error("📉 Загуба")
