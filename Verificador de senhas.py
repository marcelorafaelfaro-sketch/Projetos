import hashlib, requests



senha = "cu12435"
h = hashlib.sha1(senha.encode())
h = h.hexdigest().upper()
r = requests.get(
    "https://api.pwnedpasswords.com"
                 f"/range/{h[:5]}"
)
vezes = 0
for linha in r.text.splitlines():
    fim, qtd = linha.split(":")
    if fim == h[5:]:
        vezes = int(qtd)
print(f"Essa senha vazou {vezes} vezes")
