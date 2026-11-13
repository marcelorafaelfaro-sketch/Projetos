#!/usr/bin/env python3
"""
TRIAD - prova de conceito, etapa 1.

O que este script testa:
  Degrau 1: chamar cada CLI por programa (sem digitar).
  Degrau 2: chamar as tres ao mesmo tempo e guardar as respostas.
  Degrau 3 (--revisar): mandar as respostas para o Claude criticar.

Uso:
  python3 triad_poc.py ~/triad-lab
  python3 triad_poc.py ~/triad-lab --revisar

ATENCAO:
  - Cada chamada consome a cota da sua assinatura. O prompt padrao e pequeno.
  - As flags do 'agy' NAO foram confirmadas. Rode 'agy --help' e ajuste CLIS.
  - Nao use --bare no claude (exige chave de API = cobranca fora da assinatura).
"""
import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(next((a for a in sys.argv[1:] if not a.startswith("--")), "~/triad-lab")).expanduser()
REVISAR = "--revisar" in sys.argv
TIMEOUT = 180  # segundos por chamada

PROMPT = "Ache o bug em calc.py. Nao edite nenhum arquivo. Responda em ate 5 linhas."

# AJUSTE AQUI depois de rodar `<cli> --help`.
def comandos(prompt: str) -> dict:
    return {
        "codex": ["codex", "exec", "--sandbox", "read-only", prompt],
        "claude": ["claude", "-p", prompt, "--output-format", "json"],
        "agy": ["agy", "-p", prompt],  # hipotese: confirmar com `agy --help`
    }

# Chaves de API podem tirar a CLI da assinatura e passar a cobrar. Removemos.
CHAVES_PROIBIDAS = [
    "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY",
]


def ambiente_limpo() -> dict:
    env = dict(os.environ)
    removidas = [k for k in CHAVES_PROIBIDAS if env.pop(k, None) is not None]
    if removidas:
        print(f"[aviso] chaves removidas do ambiente desta execucao: {removidas}")
    return env


def git_status() -> str:
    r = subprocess.run(["git", "status", "--porcelain"], cwd=REPO,
                       capture_output=True, text=True)
    return r.stdout.strip()


def extrair_texto(nome: str, saida: str) -> str:
    """O claude com --output-format json devolve um objeto com campo 'result'."""
    if nome == "claude":
        try:
            return json.loads(saida).get("result", saida)
        except (json.JSONDecodeError, AttributeError):
            return saida
    return saida


async def rodar(nome: str, cmd: list, env: dict) -> dict:
    inicio = time.time()
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd, cwd=REPO, env=env,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=TIMEOUT)
        except asyncio.TimeoutError:
            proc.kill()
            return {"cli": nome, "ok": False, "erro": f"timeout {TIMEOUT}s",
                    "segundos": round(time.time() - inicio, 1)}
        saida = out.decode(errors="replace").strip()
        return {
            "cli": nome,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "texto": extrair_texto(nome, saida),
            "stderr": err.decode(errors="replace").strip()[-500:],
            "segundos": round(time.time() - inicio, 1),
        }
    except FileNotFoundError:
        return {"cli": nome, "ok": False, "erro": "comando nao encontrado (nao instalado?)",
                "segundos": 0}


async def main():
    if not (REPO / ".git").exists():
        sys.exit(f"{REPO} nao e um repositorio git. Rode 'git init' la antes.")
    if git_status():
        sys.exit("O repositorio de teste tem alteracoes nao commitadas. Faca commit antes.")

    env = ambiente_limpo()

    print("== Degrau 2: as tres CLIs em paralelo ==")
    cmds = comandos(PROMPT)
    resultados = await asyncio.gather(*[rodar(n, c, env) for n, c in cmds.items()])

    # Checagem de seguranca: alguem editou arquivo mesmo sendo 'somente leitura'?
    alterado = git_status()
    print("[git] arquivos alterados apos a execucao:", alterado or "nenhum (ok)")

    for r in resultados:
        status = "OK " if r["ok"] else "ERRO"
        print(f"\n[{status}] {r['cli']} ({r.get('segundos')}s)")
        print(r.get("texto") or r.get("erro") or r.get("stderr"))

    revisao = None
    if REVISAR:
        print("\n== Degrau 3: Claude revisa as analises dos outros ==")
        analises = "\n\n".join(
            f"--- Analise do {r['cli']} ---\n{r.get('texto')}"
            for r in resultados if r["ok"] and r["cli"] != "claude"
        )
        if not analises:
            print("Nenhuma analise valida para revisar.")
        else:
            pedido = ("Revise criticamente estas analises do bug em calc.py. "
                      "Diga quem acertou, quem errou e por que. Max 6 linhas.\n\n" + analises)
            revisao = await rodar("claude", comandos(pedido)["claude"], env)
            print(revisao.get("texto") or revisao.get("erro") or revisao.get("stderr"))

    pasta = Path(__file__).parent / "runs"
    pasta.mkdir(exist_ok=True)
    arq = pasta / f"run_{time.strftime('%Y%m%d_%H%M%S')}.json"
    arq.write_text(json.dumps(
        {"prompt": PROMPT, "resultados": resultados, "revisao": revisao,
         "git_alterado": alterado}, ensure_ascii=False, indent=2))
    print(f"\nLog salvo em: {arq}")


if __name__ == "__main__":
    asyncio.run(main())