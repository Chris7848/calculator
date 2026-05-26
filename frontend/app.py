import streamlit as st
import requests
import time

# =========================
# BACKEND URL
# =========================
API_URL = "https://calculator-1-8alq.onrender.com"

st.set_page_config(page_title="VHDL ALU Simulator", layout="centered")

st.title("⚡ LIVE VHDL ALU SIMULATOR")
st.write("Change inputs and results update automatically (debounced).")

# =========================
# SESSION STATE INIT
# =========================
if "result" not in st.session_state:
    st.session_state.result = ""

if "last_call" not in st.session_state:
    st.session_state.last_call = 0

if "cached_inputs" not in st.session_state:
    st.session_state.cached_inputs = None

# =========================
# INPUTS
# =========================
A = st.number_input("Input A", min_value=0, max_value=255, value=10)
B = st.number_input("Input B", min_value=0, max_value=255, value=5)

op_map = {
    "ADD (+)": 0,
    "SUB (-)": 1,
    "MUL (*)": 2,
    "DIV (/)": 3
}

op_label = st.selectbox("Operation", list(op_map.keys()))
Op = op_map[op_label]

Display = st.selectbox("Display Mode", ["Result", "Remainder/Overflow"])
Display_val = 0 if Display == "Result" else 1

# =========================
# CURRENT INPUT PACKAGE
# =========================
current_inputs = (A, B, Op, Display_val)

# =========================
# BACKEND CALL FUNCTION
# =========================
def call_backend():
    payload = {
        "A": int(A),
        "B": int(B),
        "Op": int(Op),
        "Display": int(Display_val)
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            st.session_state.result = data.get("stdout", "No output")
        else:
            st.session_state.result = f"Backend error: {response.text}"

    except Exception as e:
        st.session_state.result = f"Connection failed: {str(e)}"


# =========================
# DEBOUNCED AUTO RUN LOGIC
# =========================
now = time.time()

# Only run if:
# 1. inputs changed OR
# 2. first run OR
# 3. enough time passed (0.7s debounce)
if (
    st.session_state.cached_inputs != current_inputs
    or now - st.session_state.last_call > 0.7
):

    call_backend()

    st.session_state.cached_inputs = current_inputs
    st.session_state.last_call = now


# =========================
# OUTPUT DISPLAY
# =========================
st.subheader("📤 ALU Output")
st.code(st.session_state.result)
