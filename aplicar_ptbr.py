"""Reaplica a tradução PT-BR e os rótulos (Carro/Moto/Cachorro/Gato) no Advanced Camera Card.

Uso (depois de atualizar o card pelo HACS, ou depois de mudar a tradução):
    python aplicar_ptbr.py "Z:/www/community/advanced-camera-card"

O que faz (pode rodar quantas vezes quiser):
 1. Grava a tradução desta pasta (lang-pt-BR.traduzido.js) como lang-pt-BR.js e aponta o
    shared-*.js para ele com "?v=<hora>", para o navegador sempre baixar a versão do servidor
    (sem cache). O arquivo de idioma original do card não é alterado.
 2. Troca no shared-*.js a função que formata rótulos por uma versão que traduz
    car/motorcycle/dog/cat (edite ROTULOS abaixo para incluir outros).
 3. Corrige no editor-*.js a lista de câmeras/pastas do editor visual (quebrada no HA 2026.10).
 4. Regenera os .gz, que o Home Assistant serve no lugar do .js.
Backup *.bak-original do shared e do editor é feito só na 1ª vez.
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

# 1) idioma: grava a tradução como lang-pt-BR.js (nome fixo) e faz o shared importá-la com
#    "?v=<hora atual>". A cada abertura do painel o endereço muda, então o navegador sempre baixa
#    o arquivo do servidor em vez de usar o cache (o arquivo é leve).
NOVO = "lang-pt-BR.js"
IMPORT = "./" + NOVO + "?v=${Date.now()}"
ref = re.compile(r"\./lang-pt-BR(?:-[\w-]+)?\.js(?:\?v=\$\{Date\.now\(\)\})?")
# "pt" (Português de Portugal, escolhido por engano em algum navegador) também usa a tradução PT-BR
s = re.sub(r"(t===`pt`\?\w+\[t\]=await import\(`)\./lang-pt-PT-[\w-]+\.js", r"\g<1>" + IMPORT.replace("\\", "\\\\"), s)
s, n = ref.subn(lambda _: IMPORT, s)
if not re.search(r"t===`pt_BR`\?\w+\[t\]=await import\(`" + re.escape(IMPORT) + "`", s):
    sys.exit("Referência ao idioma pt-BR não encontrada no shared; o código mudou nesta versão.")
if not re.search(r"t===`pt`\?\w+\[t\]=await import\(`" + re.escape(IMPORT) + "`", s):
    print("aviso: mapeamento do idioma 'pt' não encontrado (só afeta quem usa Português de Portugal).")
# Card sempre em PT-BR: ignora o idioma do perfil/navegador/app (que no app iOS pelo acesso
# externo pode vir como inglês). Com False, o card volta a seguir o idioma do Home Assistant.
SO_PTBR = True
sel = re.compile(r"(function \w+\(e\)\{)(?:return`pt_BR`;)?(let t=e=>e\.replace\(`-`,`_`\),n=e\?\.language\?\?e\?\.selectedLanguage;)")
if not sel.search(s):
    print("ATENÇÃO: função de idioma não encontrada; 'sempre PT-BR' não aplicado.")
else:
    s = sel.sub(lambda m: m.group(1) + ("return`pt_BR`;" if SO_PTBR else "") + m.group(2), s, count=1)
    print("idioma fixo em PT-BR:", "sim" if SO_PTBR else "não (segue o Home Assistant)")
traducao = open(os.path.join(AQUI, "lang-pt-BR.traduzido.js"), encoding="utf8").read()
grava(os.path.join(pasta, NOVO), traducao)
# Atalhos LUCAR1..5: versões antigas do script usavam esses nomes, e um navegador/app que ainda
# guarde o shared antigo no cache (até 31 dias) os procura. Cada atalho só busca o lang-pt-BR.js
# atual, sem cache. Quando não precisar mais (a partir de ~22/12/2026), troque para False:
# o script então apaga os atalhos.
ATALHOS = True  # necessário com a Cloudflare na frente: celulares guardam o shared antigo
for p in glob.glob(os.path.join(pasta, "lang-pt-BR-LUCAR*.js*")):
    os.remove(p)
# O arquivo de idioma original do card (lang-pt-BR-<hash>.js, tradução incompleta) também vira
# atalho: um navegador com o shared ORIGINAL em cache (de antes deste script) o procura e
# mostraria o card metade em inglês. Backup .bak-original; com ATALHOS = False ele é restaurado.
originais = [p for p in glob.glob(os.path.join(pasta, "lang-pt-BR-*.js"))
             if not os.path.basename(p).startswith("lang-pt-BR-LUCAR")]
for p in originais:
    for ext in (p, p + ".gz"):
        if os.path.exists(ext) and not os.path.exists(ext + ".bak-original"):
            shutil.copy2(ext, ext + ".bak-original")
if ATALHOS:
    nomes = [n for n in re.findall(r" as (\w+)", re.search(r"export\{(.*)\}", traducao).group(1)) if n != "default"]
    atalho = ("const m=await import(`" + IMPORT + "`);export const {" + ",".join(nomes) + "}=m;"
              "export default m.default;\n")
    for i in range(1, 6):
        grava(os.path.join(pasta, f"lang-pt-BR-LUCAR{i}.js"), atalho)
    for p in originais:
        grava(p, atalho)
    print("atalhos OK: LUCAR1-5 e", ", ".join(os.path.basename(p) for p in originais), "->", NOVO)
else:
    for p in originais:
        for ext in (p, p + ".gz"):
            if os.path.exists(ext + ".bak-original"):
                shutil.copy2(ext + ".bak-original", ext)
    print("atalhos removidos; idioma original do card restaurado")
print("idioma OK:", NOVO, "(sempre baixado do servidor, sem cache)")

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

# 3) editor visual: o HA 2026.10 não tem mais ha-md-list/ha-md-list-item, e a lista de
#    câmeras/pastas do editor aparece empilhada (quebrada). Este CSS só vale quando esses
#    componentes não existem (:not(:defined)); se o HA ou o card corrigirem, não interfere.
LISTA = ("ha-md-list:not(:defined){display:flex;flex-direction:column}"
         "ha-md-list-item:not(:defined){display:grid;grid-template-columns:auto auto minmax(0,1fr) auto auto;"
         "align-items:center;align-content:center;column-gap:8px;min-height:48px;padding:0 4px 0 12px;box-sizing:border-box}"
         "ha-md-list-item:not(:defined)>.handle{grid-column:1;grid-row:1/3}"
         "ha-md-list-item:not(:defined)>advanced-camera-card-icon:not(.handle){grid-column:2;grid-row:1/3}"
         "ha-md-list-item:not(:defined)>.title{grid-column:3;grid-row:1}"
         "ha-md-list-item:not(:defined)>.title:last-of-type{grid-row:1/3}"
         "ha-md-list-item:not(:defined)>.description{grid-column:3;grid-row:2;font-size:.85em;"
         "color:var(--advanced-camera-card-editor-secondary-text-color)}"
         "ha-md-list-item:not(:defined)>ha-icon-button:nth-of-type(1){grid-column:4;grid-row:1/3}"
         "ha-md-list-item:not(:defined)>ha-icon-button:nth-of-type(2){grid-column:5;grid-row:1/3}")
MARCA = "/*LUCAR-editor*/"
eds = glob.glob(os.path.join(pasta, "editor-*.js"))
if len(eds) != 1:
    print("ATENÇÃO: esperava 1 editor-*.js, achei", eds, "- ajuste do editor não aplicado.")
else:
    ep = eds[0]
    e = open(ep, encoding="utf8").read()
    for ext in (ep, ep + ".gz"):
        if os.path.exists(ext) and not os.path.exists(ext + ".bak-original"):
            shutil.copy2(ext, ext + ".bak-original")
    ok = True
    ancora = "ha-md-list{gap:8px;padding:0 10px}"
    # remove o bloco de uma execução anterior (se houver) e insere o atual
    e = re.sub(re.escape(MARCA) + ".*?(?=" + re.escape(ancora) + ")", "", e, count=1, flags=re.S)
    if ancora in e:
        e = e.replace(ancora, MARCA + LISTA + ancora, 1)
    else:
        ok = False
        print("ATENÇÃO: CSS da lista do editor não encontrado; o código mudou nesta versão.")
    # ícone do "Editor completo" alinhado com o texto (o interruptor do HA 2026.10 ficou mais alto)
    e = e.replace(".mode advanced-camera-card-icon{color:", ".mode advanced-camera-card-icon{align-self:flex-start;color:", 1)
    if ok:
        grava(ep, e)
        print("editor OK:", os.path.basename(ep), "(+ .gz)")
print("Pronto. Recarregue o painel com Ctrl+F5 (não precisa reiniciar o Home Assistant).")
