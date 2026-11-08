---
name: gta-short
description: Produz um Short vertical completo do canal GTAVI | MISSION PASSED (narração João Félix, imagens estilo GTA, legenda animada, trilha synthwave, cartão MISSION PASSED) a partir de um roteiro. Use para transformar roteiro.md em vídeo final.
---

# Produção do Short

Pasta do vídeo: `producao/<AAAA-MM-DD>_<slug>/`. Exemplo completo: `producao/2026-11-09_gta3-11-setembro/`.

## Padrões fixos do canal
- **Voz:** Magnific `audio_tts`, voiceId **455 (João Félix)**, model `eleven_turbo_v2_5`, speed 1.08. (~50 créditos por Short)
- **Música:** `library/musicas/trilha_01_synthwave_miami.mp3` (padrão). Alternativas na `library/README.md`.
- **Imagens:** Runware, modelo FLUX.2 klein 9B (`runware:400@2`), 768x1344, ~US$ 0,001 por imagem.
- **Fontes:** `brand/fonts/Anton.ttf` (legenda/títulos).

## Versão "prende a atenção" (padrão a partir do v2, ver producao/2026-11-09_gta3-11-setembro-v2)
- **Voz expressiva**: `eleven_v3` + voiceId 455 + stability 0.4, com 1 tag curta por frase ([serious], [tense], [curious], [excited]),
  reticências para pausa e CAIXA ALTA para ênfase (~145 créditos/min). Ela sai lenta: rodar
  `python3 tools/tighten_audio.py narracao.mp3 timings_brutos.json narracao_ajustada.wav timings.json 1.22 0.2`
  (encurta pausas, acelera 1,22x e mantém a legenda sincronizada). Ignorar tokens de tag ("[", "serious]") nos tempos.
- **Visual de época**: imagens no estilo "early-2000s PlayStation 2 era open-world game screenshot, low-poly..." para GTA III/VC/SA.
- **Cenas em movimento**: animar 4-6 imagens com `tools/runware_video.py` (Seedance 1.0 Pro Fast, ~US$ 0,07 por 5s) e usar `"fit": "cover"`.
- **Corte a cada 2-4s**, `sfx` com `library/sfx/` (whoosh nos cortes, boom na revelação, chiado no "corta", hit na ênfase).
- **Momentos sensíveis** (tragédias reais): cartela preta simples + `music_mute`, sem imagem do evento.

## Passo a passo
1. **Narração**: `audio_tts` com o texto do roteiro → `creations_wait` → baixar MP3 para `narracao.mp3` (host pikaso.cdnpk.net liberado).
2. **Tempos das palavras**: `audio_timing_get` (paginar até `hasMore=false`) → salvar `timings.json` como
   `{"duration": s, "words": [{"text","start","end"}]}` (ignorar itens que são só pontuação).
3. **Imagens**: escrever `cenas.json` (lista de `{"name","prompt"}`) e rodar
   `RUNWARE_KEY_FILE=<arquivo da chave> python3 tools/runware_image.py <pasta>/cenas.json <pasta>/cenas`
   (a chave NUNCA vai para o repositório; peça ao usuário ou use a guardada fora do repo).
   Conferir as imagens (contact sheet) e refazer as com texto estranho/logos.
4. **projeto.json**: voice, timings, music, hook (`\\N` quebra linha), hook_end, highlight, end_card_start (início do CTA), scenes com `start` alinhado ao início das frases.
5. **Render**: `python3 tools/render_short.py <pasta>/projeto.json` (≈40s). Saída 1080x1920, 30fps, H.264/AAC.
6. **Checar**: extrair 5 frames (`ffmpeg -ss T -frames:v 1`) e olhar legenda, gancho e cartão final.
7. Atualizar status da curiosidade para "produzido" e registrar no app Central do Canal.

## Qualidade mínima
- Gancho legível em 1s, legenda nunca escondida pela interface do Shorts (fica a 70% da altura).
- Duração 30-50s. Voz sempre acima da música (o render já faz ducking).

## Trechos de gameplay real (recomendado: 1 a cada 2-3 cenas)
No `projeto.json`, uma cena pode ser vídeo em vez de imagem:
`{"video": "gameplay/sa_grove.mp4", "from": 12.5, "start": 6.0}` → usa o vídeo a partir de 12,5s, sem o áudio original,
convertido para vertical com fundo desfocado (padrão de Shorts de games). Ideal: 2-5s por trecho, sempre com narração por cima.

### De onde tirar o gameplay (ordem de segurança)
1. **Gravação própria** (melhor): GTA V, Trilogy, IV etc. no PC/console, sem HUD de rádio tocando música licenciada.
   Guardar em `Drive/.../01_Biblioteca/Gameplay_Bruto/<jogo>/`.
2. **YouTube com licença Creative Commons (CC BY)**: na busca do YouTube, Filtros → Recursos → "Creative Commons".
   Pode reutilizar com crédito: colocar "Gameplay: <canal> (CC BY)" na descrição. Registrar a URL e o canal em `library/gameplay_creditos.md`.
3. **Com autorização escrita** do dono do vídeo (print guardado no Drive em `Autorizacoes`).
4. **Evitar**: baixar vídeo qualquer do YouTube sem licença, trailers oficiais inteiros, cutscenes isoladas,
   trechos com música de rádio do jogo (Content ID).
Obs.: esta sessão na nuvem não acessa o YouTube; baixar os trechos no PC (ex.: yt-dlp, só de vídeos CC BY/autorizados/próprios)
ou rodar o sistema no PC, onde a pasta do Drive é local.
