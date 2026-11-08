---
name: gta-pesquisa
description: Pesquisa e checa curiosidades de GTA (todos os jogos) para o canal GTAVI | MISSION PASSED e mantém o banco data/curiosidades.json. Use quando precisar de novas curiosidades, checar um fato antes de virar vídeo, ou repor o estoque de pautas.
---

# Pesquisa de curiosidades GTA

Objetivo: nunca publicar fake. Curiosidade de GTA tem MUITO mito (Pé-Grande em San Andreas, fantasmas, "Darkel cortado pelo 11/9").
Mito pode virar vídeo, mas no formato "mito ou verdade", deixando claro o que é lenda.

## Banco de pautas: `data/curiosidades.json`
Cada item:
```json
{"id": "slug-unico", "jogo": "GTA San Andreas", "titulo": "Gancho curto", "fato": "O fato em 1-3 frases, com números exatos",
 "formato": "voce_sabia|mito_ou_verdade|bastidores|numeros_absurdos|misterio|polemica|linha_do_tempo|top3",
 "confianca": "alta|media|lenda", "status": "a_checar|checada|roteirizada|produzido|postado|descartada",
 "fontes": ["url1", "url2"]}
```

## Regras de verificação (obrigatórias antes de status "checada")
1. Pelo menos 2 fontes independentes, OU 1 fonte primária (Rockstar Newswire, Take-Two investidores, Guinness, entrevista de dev).
2. Wikis de fãs (gta.fandom, grandtheftwiki) servem para achar pistas, não como única fonte para números.
3. Números: usar o valor exato da fonte e o ano ("230 milhões, segundo a Take-Two em maio de 2026").
4. Se as fontes discordam: escrever a versão mais cautelosa ou usar o formato mito_ou_verdade.
5. Nunca afirmar intenção da Rockstar sem fonte ("a Rockstar deixou pistas de propósito" é proibido sem prova).
6. Use WebSearch (mode "standard"; "extended" para fatos raros ou recentes). Registre as URLs em `fontes`.

## Como repor o estoque
- Meta: sempre 30+ itens "checada" na fila (≈10 dias de postagens).
- Varie jogos (GTA 1/2, III, VC, SA, LCS/VCS, IV, V, Online, VI) e formatos: nunca 3 seguidos do mesmo jogo ou formato.
- Pós-lançamento do GTA VI (19/11/2026): priorizar GTA VI (easter eggs, comparações com GTA V, detalhes do mapa), sem spoilers do final da história.
- Fontes de pauta: r/GTA6, r/GTA, Rockstar Newswire, entrevistas antigas (Dan Houser, Leslie Benzies), GTAForums, livros/documentários sobre a Rockstar.
