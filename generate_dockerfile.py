import os
import sys
import requests
import re

# -------- Inputs --------
language = sys.argv[1] if len(sys.argv) > 1 else "python"
ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# -------- Paths --------
output_dir = "Dockerfile-Generated"
os.makedirs(output_dir, exist_ok=True)
dockerfile_path = os.path.join(output_dir, "Dockerfile")

# -------- Ollama API --------
OLLAMA_URL = "http://localhost:11434/api/generate"

prompt = f"""
You are a senior DevOps engineer.

Generate ONLY a clean, production-ready Dockerfile for a {language} application.

Rules:
- Output ONLY Dockerfile content
- NO explanations
- NO markdown
- NO backticks
- Use best practices
"""

payload = {
    "model": ollama_model,
    "prompt": prompt,
    "stream": False
}

print(f"Using Ollama model: {ollama_model}")

response = requests.post(OLLAMA_URL, json=payload, timeout=300)
response.raise_for_status()

result = response.json()
raw_output = result.get("response", "").strip()

if not raw_output:
    raise RuntimeError("Empty response from Ollama")

# -------- Cleanup / Extract --------
dockerfile_content = re.sub(r"```.*?```", "", raw_output, flags=re.DOTALL).strip()

if "FROM" not in dockerfile_content:
    raise RuntimeError("Ollama output does not look like a Dockerfile")

# -------- Write Dockerfile --------
with open(dockerfile_path, "w") as f:
    f.write(dockerfile_content + "\n")

print(f"Dockerfile generated successfully at {dockerfile_path}")
