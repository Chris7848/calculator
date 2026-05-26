from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import os

app = FastAPI()

# INPUT MODEL FROM STREAMLIT
class ALURequest(BaseModel):
    A: int
    B: int
    Op: int
    Display: int = 0


@app.post("/run")
def run_alu(req: ALURequest):

    # =========================
    # 1. CLEAN PREVIOUS BUILD
    # =========================
    subprocess.run(["ghdl", "--clean"], capture_output=True)

    # =========================
    # 2. COMPILE VHDL FILES
    # =========================
    compile_files = [
        "alu.vhdl",
        "calculator_top.vhdl",
        "calculator_tb.vhdl"
    ]

    for file in compile_files:
        result = subprocess.run(
            ["ghdl", "-a", file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return {
                "status": "compile_error",
                "file": file,
                "error": result.stderr
            }

    # =========================
    # 3. ELABORATE TESTBENCH
    # =========================
    elab = subprocess.run(
        ["ghdl", "-e", "calculator_tb"],
        capture_output=True,
        text=True
    )

    if elab.returncode != 0:
        return {
            "status": "elaboration_error",
            "error": elab.stderr
        }

    # =========================
    # 4. RUN SIMULATION
    # =========================
    # IMPORTANT: we pass values via environment variables
    # (your TB must read these OR be adapted for generics)

    env = os.environ.copy()
    env["A_VAL"] = str(req.A)
    env["B_VAL"] = str(req.B)
    env["OP_VAL"] = str(req.Op)
    env["DISP_VAL"] = str(req.Display)

    run = subprocess.run(
        ["ghdl", "-r", "calculator_tb"],
        capture_output=True,
        text=True,
        env=env,
        timeout=5
    )

    # =========================
    # 5. RETURN RESULT
    # =========================
    return {
        "status": "ok",
        "stdout": run.stdout,
        "stderr": run.stderr
    }