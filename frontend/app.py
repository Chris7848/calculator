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
    page_icon="🧮",
    layout="centered"
)

# =========================
# TITLE & HEADER
# =========================
st.title("🧮 8-Bit Calculator")
st.markdown("A real-time VHDL hardware simulation running on GHDL + FastAPI.")
st.divider()

# =========================
# SESSION STATE
# =========================
if "result" not in st.session_state:
    st.session_state.result = "Waiting for simulation..."

if "status" not in st.session_state:
    st.session_state.status = "Idle"

if "cached_inputs" not in st.session_state:
    st.session_state.cached_inputs = None

if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# =========================
# UI: CONTROLS
# =========================
with st.container(border=True):
    st.subheader("⚙️ Inputs & Operations")
    
    # Numbers
    col1, col2 = st.columns(2)
    with col1:
        A = st.number_input(
            "Input A (8-bit)",
            min_value=0,
            max_value=255,
            value=10,
            step=1
        )
    with col2:
        B = st.number_input(
            "Input B (8-bit)",
            min_value=0,
            max_value=255,
            value=5,
            step=1
        )

    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    
    # Operators
    op_col1, op_col2 = st.columns(2)
    with op_col1:
        op_map = {
            "ADD (+)": 0,
            "SUB (-)": 1,
            "MUL (*)": 2,
            "DIV (/)": 3
        }
        operation = st.selectbox("Operation", list(op_map.keys()))
        Op = op_map[operation]

    with op_col2:
        display_mode = st.selectbox(
            "Display Mode",
            ["Result", "Remainder / Overflow"]
        )
        Display_val = 0 if display_mode == "Result" else 1

# =========================
# CURRENT INPUT PACKAGE
# =========================
current_inputs = (A, B, Op, Display_val)

# =========================
# BACKEND CALL LOGIC
# =========================
def call_backend():
    payload = {
        "A": int(A),
        "B": int(B),
        "Op": int(Op),
        "Display": int(Display_val)
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=15)

        if response.status_code != 200:
            st.session_state.result = f"HTTP ERROR {response.status_code}"
            st.session_state.status = response.text
            return

        data = response.json()

        if data.get("status") == "success":
            st.session_state.result = data.get("result", "No Result")
            st.session_state.status = "Simulation Successful ✅"
        else:
            st.session_state.result = "Simulation Failed ❌"
            st.session_state.status = str(data)

    except requests.exceptions.Timeout:
        st.session_state.result = "Request Timed Out"
        st.session_state.status = "Render backend took too long to respond."
    except Exception as e:
        st.session_state.result = "Connection Failed"
        st.session_state.status = str(e)

# =========================
# AUTO UPDATE (DEBOUNCED)
# =========================
now = time.time()

if (
    current_inputs != st.session_state.cached_inputs
    and now - st.session_state.last_call > 0.7
):
    with st.spinner("Simulating..."):
        call_backend()
    
    st.session_state.cached_inputs = current_inputs
    st.session_state.last_call = now

# =========================
# UI: OUTPUT DISPLAY
# =========================
st.divider()

with st.container(border=True):
    st.subheader("📤 Output")
    
    # Display the result prominently
    st.markdown(
        f"""
        <div style="background-color:#1E1E1E; padding: 20px; border-radius: 8px; text-align: center;">
            <h1 style="color:#00FFAA; margin: 0; font-family: monospace;">{st.session_state.result}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Small status indicator at the bottom
    st.caption(f"**Backend Status:** {st.session_state.status}")
