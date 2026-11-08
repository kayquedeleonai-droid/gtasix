---
name: gta-curadoria
description: Revisão humana-simulada de roteiro e narração do canal GTAVI | MISSION PASSED para o conteúdo NÃO parecer feito por IA - corta frases forçadas, deixa o texto com cara de brasileiro falando de GTA, revisa ritmo e pronúncia da voz. Use SEMPRE entre gta-roteiro e gta-short, e de novo depois de gerar a narração.
---

# Curadoria: soar como gente, não como IA

O público de GTA percebe na hora texto de IA ("Prepare-se para se surpreender!"). Isso derruba retenção e o YouTube
também penaliza conteúdo "produzido em massa". Toda peça passa por esta revisão antes de virar áudio.

## Etapa 1: ler o roteiro em voz alta (mentalmente) e reprovar se tiver
**Muletas de IA (proibidas):**
- "Prepare-se", "Você não vai acreditar", "Fique até o final", "Neste vídeo", "Vamos mergulhar", "Sem mais delongas",
  "Algo incrível", "Fascinante", "Curiosamente", "Além disso", "Vale ressaltar", "No entanto", "Em suma", "Certamente".
- Trios forçados ("rápido, intenso e inesquecível"), frases com dois-pontos dramáticos em série, perguntas retóricas empilhadas.
- Exagero sem prova ("o maior segredo da história dos games").
- Português de livro: "cujo", "dentre", "outrossim", "a qual", "mediante", ênclise formal ("tornou-se" → "virou").

**Como um brasileiro fala de GTA (preferir):**
- Frases curtas, ordem direta, verbo forte: "A Rockstar adiou o jogo." > "O lançamento foi adiado pela Rockstar."
- Oralidade leve: "pra", "tá", "olha só", "sabe aquele...", "o detalhe é que", "só que", "e aí", "tipo" (no máximo 1 vez).
- Gíria de gamer com moderação: "zerar", "missão", "procurado", "cheat", "speedrun", "NPC", "mapa".
- Números do jeito que se fala: "noventa milhões", "duzentos e trinta milhões de cópias".
- Opinião honesta e pontual: "e sinceramente, ficou melhor assim."

## Etapa 2: checklist de nota (0-2 cada, aprovar com 12+ de 14)
1. Gancho entende-se em 2 segundos e cria curiosidade real?
2. Dá para ler em voz alta sem tropeçar (nenhuma frase com mais de ~18 palavras)?
3. Zero muletas de IA da lista acima?
4. Soa como alguém contando para um amigo, não como verbete?
5. Tem pelo menos 1 detalhe concreto (número, nome, ano, lugar)?
6. O fato está igual ao do banco (sem exagero novo)?
7. CTA natural (pergunta real, não "deixe seu like")?
Se reprovar: reescrever e pontuar de novo. Salvar o placar em `roteiro.md` (seção "Curadoria").

## Etapa 3: variar para não parecer linha de montagem
- Nunca dois vídeos seguidos com a mesma primeira palavra ou a mesma estrutura de gancho.
- Alternar CTAs: pergunta de opinião, "marca quem jogava isso", "qual GTA você quer ver no próximo?", sem CTA (às vezes).
- Banco de aberturas usadas: anotar em `data/aberturas_usadas.txt` e checar antes.

## Etapa 4: narração (depois de gerar o áudio)
- Antes de gerar: chamar `audio_tts_direction` para o modelo escolhido; usar pausas com pontuação ("...", vírgulas),
  não com tags exageradas. Voz padrão: João Félix (455). Testar `stability` 0.35-0.45 para soar menos robótico.
- Escrever pronúncias difíceis do jeito que se fala: "GTA 3" (não "GTA III"), "Rókstar" se errar, "Darkél".
- Conferir pela transcrição/tempos (`audio_timing_get`): palavras faltando, ritmo acima de ~3,2 palavras/s = rápido demais.
- Pedir ao usuário para ouvir os 3 primeiros vídeos de cada semana; anotar ajustes aqui na skill.

## Etapa 5: visual
- Ilustração demais cansa: a cada 2-3 cenas ilustradas, usar 1 trecho de gameplay real (ver `gta-short`, cenas com "video").
- Nada de texto ilegível gerado por IA nas imagens (refazer a cena).
