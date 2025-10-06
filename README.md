## Setting up environment

### 1. Create a virtual environment (venv)

### 2. Open and use venv

```bash
# If no admin rights
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Activate venv
.venv/Scripts/activate
```

### 3. Install libraries

```bash
pip install -r requirements.txt
```

### 4. Run uvicorn

```bash
uvicorn server:app --reload
```
