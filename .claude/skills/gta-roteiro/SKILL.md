---
name: gta-roteiro
description: Escreve roteiros de Shorts (30-45s) do canal GTAVI | MISSION PASSED a partir de uma curiosidade checada, com gancho forte, ritmo de retenção e CTA. Use antes de gerar narração.
---

# Roteiro de Short

> Depois de escrever, passe SEMPRE pela skill `gta-curadoria` (anti-cara-de-IA) antes de gerar a narração.

Entrada: um item "checada" de `data/curiosidades.json`. Saída: `producao/<data>_<slug>/roteiro.md` com:
texto da narração, título-gancho na tela (máx. 2 linhas, 5 palavras cada), lista de cenas com prompt de imagem, palavras para destacar.

## Estrutura (35-45s, 90-115 palavras)
1. **Gancho (0-3s)**: afirmação que cria curiosidade. Nunca "Olá, pessoal". Exemplos:
   - "O GTA 3 quase saiu diferente. E o motivo foi o 11 de setembro."
   - "Esse detalhe do GTA V custou 265 milhões."
   - "90% dos jogadores nunca viram isso em San Andreas."  (só use % se for verdade, senão "quase ninguém")
2. **Contexto (3-12s)**: o mínimo para entender.
3. **Virada (12-30s)**: o fato surpreendente, com número exato ou detalhe concreto.
4. **Bônus/mito (opcional)**: "E tem um mito famoso..." aumenta o tempo de tela.
5. **CTA (últimos 4-5s)**: pergunta que gera comentário + "segue o canal pra mais curiosidades de GTA".

## Regras
- Português do Brasil falado, frases curtas, sem palavrão pesado (anúncios).
- "GTA 3", "GTA 5" por extenso como se fala; números por extenso só quando a voz erra.
- Nada de afirmação sem fonte no banco. Se o fato é "média" confiança, use "segundo X" ou "dizem que".
- Sem spoilers do final de GTA VI. Sem violência gráfica como foco (regra de anúncios do YouTube).
- Loop: a última frase pode puxar a primeira (ex.: terminar com "...e foi assim que o GTA 3 quase saiu diferente").

## Formatos (alternar, nunca 3 iguais seguidos)
voce_sabia · mito_ou_verdade · bastidores · numeros_absurdos · misterio · polemica · linha_do_tempo · top3

## Cenas
4-7 cenas, uma a cada 5-8s, trocando no início de cada frase importante.
Prompt de imagem: descrever a cena + sufixo de estilo fixo:
"vertical illustration in the style of classic open-world crime game loading-screen art, bold comic-book ink outlines, cel shading, saturated colors, dramatic lighting, no text, no letters, no logos".
Nunca pedir personagens oficiais da Rockstar pelo nome (use descrições genéricas) nem marcas reais.
