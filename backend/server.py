from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ALURequest(BaseModel):
    A: int
    B: int
    Op: int
    Display: int = 0


INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/run")
def run_alu(req: ALURequest):

    # =========================
    # 1. WRITE INPUT FILE
    # =========================
    with open(INPUT_FILE, "w") as f:
        f.write(f"{req.A}\n{req.B}\n{req.Op}\n{req.Display}\n")

    # =========================
    # 2. CLEAN
    # =========================
    subprocess.run(["ghdl", "--clean"], capture_output=True)

    # =========================
    # 3. COMPILE
    # =========================
    files = [
        "alu.vhdl",
        "register.vhdl",
        "calc_top.vhdl",
        "calc_tb.vhdl"
    ]

    for f in files:
        if not os.path.exists(f):
            return {"status": "missing_file", "file": f}

        res = subprocess.run(["ghdl", "-a", f], capture_output=True, text=True)
        if res.returncode != 0:
            return {"status": "compile_error", "file": f, "error": res.stderr}

    # =========================
    # 4. ELABORATE
    # =========================
    elab = subprocess.run(["ghdl", "-e", "calculator_tb"], capture_output=True, text=True)

    if elab.returncode != 0:
        return {"status": "elaboration_error", "error": elab.stderr}

    # =========================
    # 5. RUN SIM
    # =========================
    run = subprocess.run(
        ["ghdl", "-r", "calculator_tb"],
        capture_output=True,
        text=True,
        timeout=5
    )

    # =========================
    # 6. READ OUTPUT FILE
    # =========================
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            result = f.read().strip()
    else:
        result = "no_output_file"

    return {
        "status": "success",
        "result": result,
        "stdout": run.stdout,
        "stderr": run.stderr
    }
