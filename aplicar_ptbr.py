"""Reaplica a tradução PT-BR e os rótulos (Carro/Moto/Cachorro/Gato) no Advanced Camera Card.

Uso (depois de atualizar o card pelo HACS, ou depois de mudar a tradução):
    python aplicar_ptbr.py "Z:/www/community/advanced-camera-card"

O que faz (pode rodar quantas vezes quiser):
 1. Grava a tradução desta pasta (lang-pt-BR.traduzido.js) como lang-pt-BR-LUCAR<n>.js,
    com <n> novo a cada execução, e aponta o shared-*.js para ele. O nome novo obriga o
    navegador a baixar o arquivo de novo (sem cache). O arquivo original do card não é alterado.
 2. Troca no shared-*.js a função que formata rótulos por uma versão que traduz
    car/motorcycle/dog/cat (edite ROTULOS abaixo para incluir outros).
 3. Regenera os .gz, que o Home Assistant serve no lugar do .js.
Backup *.bak-original do shared é feito só na 1ª vez.
Não precisa reiniciar o Home Assistant: basta recarregar o painel (Ctrl+F5).
"""
import glob, gzip, os, re, shutil, sys

ROTULOS = {"car": "Carro", "motorcycle": "Moto", "dog": "Cachorro", "cat": "Gato"}
AQUI = os.path.dirname(os.path.abspath(__file__))
pasta = sys.argv[1] if len(sys.argv) > 1 else "Z:/www/community/advanced-camera-card"


def grava(p, texto):
    with open(p, "w", encoding="utf8", newline="") as f:
        f.write(texto)
    with open(p, "rb") as f, gzip.open(p + ".gz", "wb", 9) as g:
        g.write(f.read())


shareds = glob.glob(os.path.join(pasta, "shared-*.js"))
if len(shareds) != 1:
    sys.exit(f"Esperava 1 shared-*.js, achei {shareds}")
sp = shareds[0]
s = open(sp, encoding="utf8").read()
for ext in (sp, sp + ".gz"):
    if os.path.exists(ext) and not os.path.exists(ext + ".bak-original"):
        shutil.copy2(ext, ext + ".bak-original")

# 1) idioma: descobre o arquivo referenciado e grava a tradução com nome novo
m = re.search(r"\./(lang-pt-BR-[\w-]+\.js)", s)
if not m:
    sys.exit("Referência ao idioma pt-BR não encontrada no shared; o código mudou nesta versão.")
atual = m.group(1)
mn = re.fullmatch(r"lang-pt-BR-LUCAR(\d+)\.js", atual)
novo = f"lang-pt-BR-LUCAR{int(mn.group(1)) + 1 if mn else 1}.js"
grava(os.path.join(pasta, novo), open(os.path.join(AQUI, "lang-pt-BR.traduzido.js"), encoding="utf8").read())
s = s.replace("./" + atual, "./" + novo)
if mn:  # remove a cópia anterior feita por este script (nunca o original do card)
    for ext in ("", ".gz"):
        p = os.path.join(pasta, atual + ext)
        if os.path.exists(p):
            os.remove(p)
print(f"idioma OK: {atual} -> {novo}")

# 2) rótulos
mapa = ",".join(f"{k}:`{v}`" for k, v in ROTULOS.items())
nova = ("function NOME(e){if(e){let m={%s};return e.trim().split(/[_\\s]+/).map(e=>{let t=e.match(/^(.*?)(,?)$/),"
        "n=m[t[1].toLowerCase()];return n?n+t[2]:e[0].toUpperCase()+e.substring(1)}).join(` `)}}") % mapa
orig = re.compile(r"function (\w+)\(e\)\{if\(e\)return e\.trim\(\)\.split\(/\[_\\s\]\+/\)\.map\(e=>e\[0\]\.toUpperCase\(\)\+e\.substring\(1\)\)\.join\(` `\)\}")
jaaplicado = re.compile(r"function (\w+)\(e\)\{if\(e\)\{let m=\{[^}]*\};return e\.trim\(\)\.split\(/\[_\\s\]\+/\)\.map\(e=>\{let t=e\.match\(/\^\(\.\*\?\)\(,\?\)\$/\),n=m\[t\[1\]\.toLowerCase\(\)\];return n\?n\+t\[2\]:e\[0\]\.toUpperCase\(\)\+e\.substring\(1\)\}\)\.join\(` `\)\}\}")
m = orig.search(s) or jaaplicado.search(s)
if m:
    s = s[:m.start()] + nova.replace("NOME", m.group(1), 1) + s[m.end():]
    print("rótulos OK (função", m.group(1) + ")")
else:
    print("ATENÇÃO: função de rótulos não encontrada; o código mudou nesta versão. Peça ajuste ao Claude.")

grava(sp, s)
print("shared OK:", os.path.basename(sp), "(+ .gz)")
print("Pronto. Recarregue o painel com Ctrl+F5 (não precisa reiniciar o Home Assistant).")
