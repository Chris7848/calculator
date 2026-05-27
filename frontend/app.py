import streamlit as st
import requests
import time

# =========================
# BACKEND URL
# =========================
API_URL = "https://calculator-2-18ph.onrender.com/run"

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="8-Bit Calculator",
    layout="centered"
)

# =========================
# TITLE
# =========================
st.title("🧮 8-Bit Calculator")
st.divider()

# =========================
# SESSION STATE
# =========================
if "result" not in st.session_state:
    st.session_state.result = "0"

if "cached_inputs" not in st.session_state:
    st.session_state.cached_inputs = None

if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# =========================
# INPUTS
# =========================
col1, col2 = st.columns(2)

with col1:
    A = st.number_input("Input A", min_value=0, max_value=255, value=10, step=1)
    operation = st.selectbox("Operation", ["ADD (+)", "SUB (-)", "MUL (*)", "DIV (/)"])

with col2:
    B = st.number_input("Input B", min_value=0, max_value=255, value=5, step=1)
    display_mode = st.selectbox("Display Mode", ["Result", "Remainder / Overflow"])

# =========================
# MAPPING
# =========================
op_map = {"ADD (+)": 0, "SUB (-)": 1, "MUL (*)": 2, "DIV (/)": 3}
Op = op_map[operation]
Display_val = 0 if display_mode == "Result" else 1

current_inputs = (A, B, Op, Display_val)

# =========================
# BACKEND CALL
# =========================
def call_backend():
    payload = {"A": int(A), "B": int(B), "Op": int(Op), "Display": int(Display_val)}
    try:
        response = requests.post(API_URL, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                st.session_state.result = data.get("result", "0")
            else:
                st.session_state.result = "Error"
        else:
            st.session_state.result = "Offline"
    except:
        st.session_state.result = "Offline"

# Auto-update logic
now = time.time()
if current_inputs != st.session_state.cached_inputs and now - st.session_state.last_call > 0.7:
    call_backend()
    st.session_state.cached_inputs = current_inputs
    st.session_state.last_call = now

# =========================
# OUTPUT DISPLAY
# =========================
st.divider()
st.subheader("Result")
st.markdown(f"## {st.session_state.result}")
