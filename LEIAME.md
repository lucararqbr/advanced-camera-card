# Advanced Camera Card — tradução PT-BR completa

**Base usada:** Advanced Camera Card (HACS), pasta `/config/www/community/advanced-camera-card`,
build de 08/11/2026, versão aparente 8.2.0 (detectada no código; confirme na tela do card).
Arquivo original: `lang-pt-BR-dQc_pOO8.js` (275 de 705 textos traduzidos; o resto aparecia em inglês).

**Modificação:** `lang-pt-BR-dQc_pOO8.js` desta pasta traz os 705 textos em PT-BR
(432 novos, todos os existentes preservados; "Automatico" não ocorre mais; chaves obsoletas
`editor.overrides*` removidas). Seções novas: actions, display_modes, key_assigner, media_viewer.

**Instalação:** copiar este arquivo por cima do de mesmo nome em
`/config/www/community/advanced-camera-card/` (Samba/SSH), limpar o cache do navegador
(Ctrl+F5 / reiniciar o app) e recarregar o painel.

**Atenção:** o nome do arquivo tem hash. Se o HACS atualizar o card, o nome muda e esta
tradução deve ser refeita sobre a nova base. Faça backup do original antes de substituir.

## Alterações adicionais (10/11/2026)
- `lang-pt-BR-dQc_pOO8.js` foi copiado como `lang-pt-BR-LUCAR1.js` (nome novo para furar o cache do navegador)
  e a referência foi trocada em `shared-DKvQuQy0.js`. O arquivo antigo e o `.bak-original` continuam na pasta.
- `shared-DKvQuQy0.js`: a função que formata rótulos (`Gy`) agora traduz car → Carro, motorcycle → Moto,
  dog → Cachorro, cat → Gato (somente na exibição; o Frigate e as automações não mudam).
  Para incluir outros rótulos, edite o objeto `m` dentro dessa função e regenere o `.gz`
  (`gzip -9 -c shared-DKvQuQy0.js > shared-DKvQuQy0.js.gz`).
- Backups dos originais: `shared-DKvQuQy0.js.bak-original` e `shared-DKvQuQy0.js.gz.bak-original`.

## Como refazer após atualizar o card (HACS)
Arquivos desta pasta: `lang-pt-BR.traduzido.js` (tradução completa) e `aplicar_ptbr.py` (reaplica tudo).
```
python aplicar_ptbr.py "Z:/www/community/advanced-camera-card"
```
O script faz backup `.bak-original` (só na 1ª vez), troca o conteúdo do `lang-pt-BR-*.js`, aplica a
tradução de rótulos no `shared-*.js` e regenera os `.gz`. É seguro rodar mais de uma vez.
Se o card ganhar textos novos, eles aparecem em inglês até a tradução ser atualizada (peça ao Claude).
Se o script avisar "função de rótulos não encontrada", o código do card mudou e precisa de ajuste manual.
Obs.: nesta pasta não há git; a cópia de segurança é esta pasta (OneDrive).
