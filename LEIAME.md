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
- **No card (Z:)**, o script altera apenas o `shared-*.js` (2 trechos: referência ao idioma e
  função de rótulos) e cria `lang-pt-BR-LUCAR<n>.js`. O arquivo de idioma original do card
  não é alterado. Backups: `shared-*.js.bak-original` e `.gz.bak-original`.

## Como aplicar / refazer após atualizar o card (HACS)
```
python aplicar_ptbr.py "Z:/www/community/advanced-camera-card"
```
- Pode rodar quantas vezes quiser. A cada execução o arquivo de idioma ganha um número novo
  (LUCAR1, LUCAR2…), o que obriga o navegador a baixar a versão nova.
- Os `.gz` são regenerados (o Home Assistant entrega o `.gz` no lugar do `.js`).
- **Não precisa reiniciar o Home Assistant.** Basta recarregar o painel (Ctrl+F5). No app,
  ou se ainda aparecer texto antigo: limpar dados do site / "Limpar cache do frontend".
- Se o card ganhar textos novos, eles aparecem em inglês até a tradução ser atualizada.
- Se o script avisar "função de rótulos não encontrada", o código do card mudou e precisa de ajuste.

## Recurso do painel
Configurações → Painéis → Recursos, tipo "Módulo JavaScript". Se o HACS já registrou
`/hacsfiles/advanced-camera-card/advanced-camera-card.js?hacstag=...`, não duplique. Remova
`frigate-hass-card.js` se aparecer (legado).
