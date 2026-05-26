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
    page_title="VHDL ALU Simulator",
    layout="centered"
)

# =========================
# TITLE
# =========================
st.title("⚡ LIVE VHDL ALU SIMULATOR")
st.write("Real-time VHDL hardware simulation running on GHDL + FastAPI.")

# =========================
# SESSION STATE
# =========================
if "result" not in st.session_state:
    st.session_state.result = "Waiting for simulation..."

if "status" not in st.session_state:
    st.session_state.status = ""

if "cached_inputs" not in st.session_state:
    st.session_state.cached_inputs = None

if "last_call" not in st.session_state:
    st.session_state.last_call = 0

# =========================
# INPUTS
# =========================
col1, col2 = st.columns(2)

with col1:
    A = st.number_input(
        "Input A",
        min_value=0,
        max_value=255,
        value=10,
        step=1
    )

with col2:
    B = st.number_input(
        "Input B",
        min_value=0,
        max_value=255,
        value=5,
        step=1
    )

# =========================
# OPERATION SELECT
# =========================
op_map = {
    "ADD (+)": 0,
    "SUB (-)": 1,
    "MUL (*)": 2,
    "DIV (/)": 3
}

operation = st.selectbox(
    "Operation",
    list(op_map.keys())
)

Op = op_map[operation]

# =========================
# DISPLAY MODE
# =========================
display_mode = st.selectbox(
    "Display Mode",
    ["Result", "Remainder / Overflow"]
)

Display_val = 0 if display_mode == "Result" else 1

# =========================
# CURRENT INPUT PACKAGE
# =========================
current_inputs = (
    A,
    B,
    Op,
    Display_val
)

# =========================
# BACKEND CALL
# =========================
def call_backend():

    payload = {
        "A": int(A),
        "B": int(B),
        "Op": int(Op),
        "Display": int(Display_val)
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=15
        )

        # =========================
        # RESPONSE ERROR
        # =========================
        if response.status_code != 200:

            st.session_state.result = (
                f"HTTP ERROR {response.status_code}"
            )

            st.session_state.status = response.text

            return

        # =========================
        # PARSE JSON
        # =========================
        data = response.json()

        # =========================
        # SUCCESS
        # =========================
        if data.get("status") == "success":

            st.session_state.result = data.get(
                "result",
                "No Result"
            )

            st.session_state.status = "Simulation Successful"

        # =========================
        # BACKEND ERROR
        # =========================
        else:

            st.session_state.result = "Simulation Failed"

            st.session_state.status = str(data)

    # =========================
    # CONNECTION ERROR
    # =========================
    except requests.exceptions.Timeout:

        st.session_state.result = "Request Timed Out"

        st.session_state.status = (
            "Render backend took too long to respond."
        )

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

    call_backend()

    st.session_state.cached_inputs = current_inputs

    st.session_state.last_call = now

# =========================
# OUTPUT DISPLAY
# =========================
st.divider()

st.subheader("📤 ALU Output")

st.code(
    str(st.session_state.result),
    language=None
)

# =========================
# STATUS
# =========================
st.subheader("📡 Backend Status")

st.info(st.session_state.status)

# =========================
# DEBUG SECTION
# =========================
with st.expander("Debug Info"):

    st.write("API URL:")
    st.code(API_URL)

    st.write("Payload Sent:")

    st.json({
        "A": int(A),
        "B": int(B),
        "Op": int(Op),
        "Display": int(Display_val)
    })
