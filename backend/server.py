from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import os
import re

app = FastAPI()

# =========================
# ENABLE CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODEL
# =========================
class ALURequest(BaseModel):
    A: int
    B: int
    Op: int
    Display: int = 0


# =========================
# ROOT ROUTE
# =========================
@app.get("/")
def home():
    return {
        "status": "online",
        "message": "VHDL ALU Backend Running"
    }


# =========================
# RUN ALU
# =========================
@app.post("/run")
def run_alu(req: ALURequest):

    try:

        # =========================
        # DEBUG FILES
        # =========================
        files = os.listdir(".")

        # =========================
        # CLEAN PREVIOUS BUILD
        # =========================
        subprocess.run(
            ["ghdl", "--clean"],
            capture_output=True
        )

        # =========================
        # COMPILE FILES
        # =========================
        compile_files = [
            "alu.vhdl",
            "register.vhdl",
            "calc_top.vhdl",
            "calc_tb.vhdl"
        ]

        for file in compile_files:

            if not os.path.exists(file):
                return {
                    "status": "missing_file",
                    "missing": file,
                    "available_files": files
                }

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
        # ELABORATE TESTBENCH
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
        # PASS INPUTS TO TESTBENCH
        # =========================
        env = os.environ.copy()

        env["A_VAL"] = str(req.A)
        env["B_VAL"] = str(req.B)
        env["OP_VAL"] = str(req.Op)
        env["DISP_VAL"] = str(req.Display)

        # =========================
        # RUN SIMULATION
        # =========================
        run = subprocess.run(
            ["ghdl", "-r", "calculator_tb"],
            capture_output=True,
            text=True,
            env=env,
            timeout=5
        )

        # =========================
        # CHECK RUNTIME ERROR
        # =========================
        if run.returncode != 0:
            return {
                "status": "runtime_error",
                "stderr": run.stderr,
                "stdout": run.stdout
            }

        # =========================
        # EXTRACT RESULT
        # =========================
        output = run.stdout.strip()

        # Try extracting integer result
        numbers = re.findall(r'\d+', output)

        result_value = numbers[-1] if numbers else "0"

        # =========================
        # SUCCESS RESPONSE
        # =========================
        return {
            "status": "success",
            "result": result_value,
            "raw_output": output
        }

    except subprocess.TimeoutExpired:

        return {
            "status": "timeout",
            "error": "Simulation took too long"
        }

    except Exception as e:

        return {
            "status": "server_error",
            "error": str(e)
        }
