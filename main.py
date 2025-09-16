import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
# Add a comment here
# Load .env if present (local dev)
load_dotenv()

app = FastAPI()
DATA_FILE = Path("data.txt")

def masked_len(s: str | None) -> str:
    if not s:
        return "0 (missing)"
    return f"{len(s)}"

def ensure_file() -> None:
    if not DATA_FILE.exists():
        DATA_FILE.write_text("", encoding="utf-8")

@app.get("/", response_class=PlainTextResponse)
def read_file() -> str:
    """Return the data file contents and the length of the OPENAI_API_KEY (masked)."""
    ensure_file()
    contents = DATA_FILE.read_text(encoding="utf-8")
    key_len = masked_len(os.getenv("OPENAI_API_KEY"))
    return (
        "CICDLearn demo\n"
        f"OPENAI_API_KEY length: {key_len}\n"
        "---- data.txt ----\n"
        f"{contents}"
    )

@app.post("/write", response_class=PlainTextResponse)
def write_value(value: str | None = None) -> str:
    """Append a line to data.txt. Call: POST /write?value=hello"""
    if value is None or value.strip() == "":
        raise HTTPException(status_code=400, detail="Query param 'value' is required")
    ensure_file()
    with DATA_FILE.open("a", encoding="utf-8") as f:
        f.write(value + "\n")
    return f"Appended: {value}"
