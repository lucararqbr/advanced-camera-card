"""Reaplica a tradução PT-BR e os rótulos (Carro/Moto/Cachorro/Gato) no Advanced Camera Card.

Uso (depois de atualizar o card pelo HACS):
    python aplicar_ptbr.py "Z:/www/community/advanced-camera-card"

O que faz (idempotente, com backup *.bak-original só na 1ª vez):
 1. Substitui o conteúdo de lang-pt-BR-*.js pelo arquivo traduzido desta pasta
    (lang-pt-BR.traduzido.js). Chaves novas da versão nova que não existirem nele
    continuam aparecendo em inglês.
 2. Troca no shared-*.js a função que formata rótulos por uma versão que traduz
    car/motorcycle/dog/cat. Edite RUTULOS abaixo para incluir outros.
 3. Regenera os .gz, que o Home Assistant serve no lugar do .js.
Depois: Ctrl+F5 no painel (ou limpar dados do site) para furar o cache.
"""
import glob, gzip, os, re, shutil, sys

RUTULOS = {"car": "Carro", "motorcycle": "Moto", "dog": "Cachorro", "cat": "Gato"}
AQUI = os.path.dirname(os.path.abspath(__file__))
pasta = sys.argv[1] if len(sys.argv) > 1 else "Z:/www/community/advanced-camera-card"


def backup(p):
    for ext in (p, p + ".gz"):
        if os.path.exists(ext) and not os.path.exists(ext + ".bak-original"):
            shutil.copy2(ext, ext + ".bak-original")


def grava(p, texto):
    with open(p, "w", encoding="utf8", newline="") as f:
        f.write(texto)
    with open(p, "rb") as f, gzip.open(p + ".gz", "wb", 9) as g:
        g.write(f.read())


# 1) idioma
langs = [p for p in glob.glob(os.path.join(pasta, "lang-pt-BR-*.js"))]
if len(langs) != 1:
    sys.exit(f"Esperava 1 arquivo lang-pt-BR-*.js, achei {len(langs)}: {langs}")
backup(langs[0])
grava(langs[0], open(os.path.join(AQUI, "lang-pt-BR.traduzido.js"), encoding="utf8").read())
print("idioma OK:", os.path.basename(langs[0]))

# 2) rótulos
shareds = glob.glob(os.path.join(pasta, "shared-*.js"))
if len(shareds) != 1:
    sys.exit(f"Esperava 1 shared-*.js, achei {shareds}")
p = shareds[0]
s = open(p, encoding="utf8").read()
mapa = ",".join(f"{k}:`{v}`" for k, v in RUTULOS.items())
nova = ("function Gy(e){if(e){let m={%s};return e.trim().split(/[_\\s]+/).map(e=>{let t=e.match(/^(.*?)(,?)$/),"
        "n=m[t[1].toLowerCase()];return n?n+t[2]:e[0].toUpperCase()+e.substring(1)}).join(` `)}}") % mapa
orig = re.compile(r"function (\w+)\(e\)\{if\(e\)return e\.trim\(\)\.split\(/\[_\\s\]\+/\)\.map\(e=>e\[0\]\.toUpperCase\(\)\+e\.substring\(1\)\)\.join\(` `\)\}")
jaaplicado = re.compile(r"function (\w+)\(e\)\{if\(e\)\{let m=\{[^}]*\};return e\.trim\(\)")
m = orig.search(s)
if m:
    backup(p)
    s = s[:m.start()] + nova.replace("function Gy", "function " + m.group(1), 1) + s[m.end():]
    grava(p, s)
    print("rótulos OK (função", m.group(1) + ")")
elif jaaplicado.search(s):
    print("rótulos: já aplicado (nada a fazer)")
else:
    print("ATENÇÃO: função de rótulos não encontrada; o código mudou nesta versão. Peça ajuste ao Claude.")
