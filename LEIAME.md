# Advanced Camera Card — tradução PT-BR completa e rótulos em português

**Base usada:** Advanced Camera Card (HACS), pasta `/config/www/community/advanced-camera-card`,
build de 08/11/2026, versão aparente 8.2.0 (detectada no código; confirme na tela do card).
Arquivo de idioma original: `lang-pt-BR-dQc_pOO8.js` (275 de 705 textos traduzidos; o resto aparecia em inglês).

## O que foi modificado
- **Tradução** (`lang-pt-BR.traduzido.js`): 705 de 705 textos em PT-BR. 430 novos e 62 antigos
  corrigidos (ex.: "Casa" → "Posição inicial" no PTZ, "Duplique o ID" → "ID duplicado",
  "provedor ativo" → "provedor ao vivo", "Upgrade" → "Atualizar", "Snapshot" → "Instantâneo").
  Nomes próprios e siglas (Frigate, PTZ, go2rtc, Ctrl…) ficam como estão.
- **Rótulos do Frigate** (só na exibição; Frigate e automações não mudam):
  car → Carro, motorcycle → Moto, dog → Cachorro, cat → Gato. Outros rótulos aparecem
  em inglês com inicial maiúscula (ex.: "Person"). Para incluir mais, edite `ROTULOS` no script.
- **Idioma "pt" (Português de Portugal)** também usa esta tradução. Se um navegador estiver
  com o HA em "Português" em vez de "Português (Brasil)", o card não fica mais pela metade.
- **Card sempre em PT-BR** (`SO_PTBR = True` no script): o card ignora o idioma do perfil,
  do navegador e do app e usa sempre a tradução PT-BR (o app iOS pelo acesso externo chegou a
  mostrar inglês). Com `False`, volta a seguir o idioma do Home Assistant.
- **Editor visual corrigido para o HA 2026.10**: o card usa `ha-md-list`/`ha-md-list-item`,
  que o HA 2026.10 não tem mais, e a lista de câmeras/pastas no editor aparecia empilhada
  (quebrada). A versão oficial tem o mesmo defeito (o `editor-*.js` é idêntico ao zip do HACS).
  O script injeta um CSS que só vale quando esses componentes não existem (`:not(:defined)`) e
  alinha o ícone de "Editor completo". "Título/Ícone (detectado automaticamente)" virou
  "(automático)", para não quebrar a linha.
- **No card (Z:)**, o script altera `shared-*.js` (referência ao idioma, idioma "pt" e
  função de rótulos) e `editor-*.js` (CSS da lista), e cria `lang-pt-BR.js` (nome fixo). Os
  arquivos de idioma originais do card não mudam. Backups: `*.bak-original` (.js e .gz).

## Como aplicar / refazer após atualizar o card (HACS)
```
python aplicar_ptbr.py "Z:/www/community/advanced-camera-card"
```
- Pode rodar quantas vezes quiser. A tradução fica sempre em `lang-pt-BR.js`, e o card a
  importa como `lang-pt-BR.js?v=<hora>`: o endereço muda a cada abertura do painel, então o
  navegador **sempre baixa a tradução do servidor** (arquivo leve, ~30 KB) e nunca usa o cache.
  Correções de texto aparecem só com um recarregar do painel.
- Os `.gz` são regenerados (o Home Assistant entrega o `.gz` no lugar do `.js`).
- **Não precisa reiniciar o Home Assistant.** Os outros arquivos do card (`shared`, `editor`)
  o HA manda o navegador guardar por **31 dias** (`Cache-Control: max-age=2678400`). Depois de
  rodar o script, se um navegador ou celular continuar antigo (ex.: rótulos ou editor), limpe o
  cache uma vez: Edge/Chrome Ctrl+Shift+Del → "Imagens e arquivos em cache"; app iOS/Android:
  Configurações → Companion App → Depuração → "Redefinir cache do frontend".
- Versões antigas do script usavam `lang-pt-BR-LUCAR1..5.js`. O script tem a opção `ATALHOS`
  (hoje `True`): esses nomes e o idioma original do card viram atalhos para o `lang-pt-BR.js`.
  Deixe `True`: pelo acesso externo (Cloudflare), aparelhos com o `shared` antigo em cache
  pedem o arquivo de idioma original e mostravam o card metade em inglês. Com `False`, ficam
  só os arquivos originais do card.
- Se o card ganhar textos novos, eles aparecem em inglês até a tradução ser atualizada.
- Se o script avisar "função de rótulos não encontrada", o código do card mudou e precisa de ajuste.

## Recurso do painel
Configurações → Painéis → Recursos, tipo "Módulo JavaScript". Se o HACS já registrou
`/hacsfiles/advanced-camera-card/advanced-camera-card.js?hacstag=...`, não duplique. Remova
`frigate-hass-card.js` se aparecer (legado).
