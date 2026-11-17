import asyncio
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

BASE_DIR = Path.home() / "triad-lab"

def resolve_bin(name: str) -> str:
    found = shutil.which(name)
    if found:
        return found
    candidates = [
        Path.home() / ".opencode" / "bin" / name,
        Path.home() / ".local" / "bin" / name,
        Path.home() / "bin" / name,
    ]
    for path in candidates:
        if path.exists() and os.access(path, os.X_OK):
            return str(path)
    return name

WORKTREES = {
    "agy": {
        "path": Path.home() / "triad-wt-agy",
        "cmd": [resolve_bin("agy"), "-p", "Corrija o bug da função soma em calc.py para retornar a + b."],
    },
    "opencode": {
        "path": Path.home() / "triad-wt-opencode",
        "cmd": [resolve_bin("opencode"), "run", "--auto", "Corrija o bug da função soma em calc.py para retornar a + b."],
    },
}

def clean_env():
    env = os.environ.copy()
    extra_paths = [
        str(Path.home() / ".opencode" / "bin"),
        str(Path.home() / ".local" / "bin"),
    ]
    env["PATH"] = ":".join(extra_paths + [env.get("PATH", "")])
    for k in list(env.keys()):
        if any(p in k.upper() for p in ("ANTHROPIC", "OPENAI", "GEMINI", "GOOGLE_API")):
            env.pop(k, None)
    return env

def run_independent_test(wt_path: Path) -> dict:
    res = subprocess.run(
        ["python3", "-c", "import calc; assert calc.soma(2, 3) == 5, f'Esperado 5, veio {calc.soma(2, 3)}'; print('OK: soma(2,3)==5')"],
        cwd=wt_path,
        capture_output=True,
        text=True,
    )
    diff = subprocess.run(["git", "diff"], cwd=wt_path, capture_output=True, text=True).stdout
    return {
        "test_passed": res.returncode == 0,
        "test_output": (res.stdout + res.stderr).strip(),
        "git_diff": diff.strip(),
    }

async def run_executor(name: str, cfg: dict, env: dict) -> dict:
    t0 = time.perf_counter()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cfg["cmd"],
            cwd=cfg["path"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )
    except FileNotFoundError as exc:
        return {
            "executor": name,
            "error": f"Binário não encontrado: {exc}",
            "cmd_tentado": cfg["cmd"][0],
            "elapsed_s": round(time.perf_counter() - t0, 2),
        }

    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
    except asyncio.TimeoutError:
        proc.kill()
        return {"executor": name, "error": "TIMEOUT (120s)", "elapsed_s": round(time.perf_counter() - t0, 2)}

    elapsed = round(time.perf_counter() - t0, 2)
    out_str = stdout.decode("utf-8", errors="replace").strip()
    err_str = stderr.decode("utf-8", errors="replace").strip()
    validation = run_independent_test(cfg["path"])

    return {
        "executor": name,
        "bin_resolved": cfg["cmd"][0],
        "returncode": proc.returncode,
        "elapsed_s": elapsed,
        "stdout_empty": len(out_str) == 0,
        "stdout_preview": out_str[:400],
        "stderr_preview": err_str[:300],
        **validation,
    }

async def main():
    env = clean_env()
    t_total = time.perf_counter()
    results = await asyncio.gather(
        *(run_executor(name, cfg, env) for name, cfg in WORKTREES.items())
    )
    main_status = subprocess.run(["git", "status", "--short"], cwd=BASE_DIR, capture_output=True, text=True).stdout.strip()
    report = {
        "total_parallel_time_s": round(time.perf_counter() - t_total, 2),
        "main_repo_dirty": bool(main_status),
        "results": results,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())