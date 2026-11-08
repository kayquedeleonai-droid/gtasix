# Biblioteca do canal

## Voz (escolher UMA para ser a voz fixa do canal)

Todas na Magnific (ElevenLabs, modelo eleven_turbo_v2_5), com o mesmo texto de teste:

| Arquivo | Voz | voiceId | Perfil |
|---|---|---|---|
| voz/amostra_1_DuarteFonseca.mp3 | Duarte Fonseca | 1219 | Rápida e animada, feita para Shorts e ganchos virais |
| voz/amostra_2_ViniciusBarroso.mp3 | Vinícius Barroso | 933 | Energia média, tom de review e conteúdo de games |
| voz/amostra_3_TiagoMacedo.mp3 | Tiago Macedo | 1409 | Voz de locutor, grave e com credibilidade |
| voz/amostra_4_DuarteQueiroz.mp3 | Duarte Queiroz | 1060 | Brasileira nativa, firme e dramática (documentário) |
| voz/amostra_5_ViniciusCordeiro.mp3 | Vinícius Cordeiro | 1281 | Brasileira natural, conversada, boa para redes sociais |
| voz/amostra_6_JoaoFelix.mp3 | João Félix | 455 | Jovem, dinâmica, feita para YouTube |
| voz/amostra_7_TiagoLima.mp3 | Tiago Lima | 450 | Animada e descontraída, tom de entretenimento |
| voz/amostra_8_RafaelValente.mp3 | Rafael Valente | 116 | Cativante, cria conexão rápida |
| voz/amostra_9_OtavioNogueira.mp3 | Otávio Nogueira | 1098 | Feita para redes sociais |

As amostras 4 a 9 usam um fato verdadeiro (as três cidades de San Andreas e suas inspirações reais).

O texto das amostras é só um teste de voz. A frase sobre o Pé-Grande NÃO foi checada e não deve ir para um vídeo.

## Músicas (instrumentais geradas por IA, sem direitos de terceiros)

| Arquivo | Estilo | Uso sugerido | Origem |
|---|---|---|---|
| musicas/trilha_01_synthwave_miami.mp3 (60s) | Synthwave anos 80, Miami | Vice City, GTA VI, vídeos "vibe" | Magnific (ElevenLabs Music) |
| musicas/trilha_02_synthwave_rap_neon.mp3 (2min17) | Synthwave + hip hop, 808, vocoder | Fundo padrão dos Shorts | Runware (MiniMax Music 2.6) |
| musicas/trilha_03_synthwave_rap_dark.mp3 (2min09) | Synthwave + trap sombrio | Mistérios, crimes, lado sombrio | Runware |
| musicas/trilha_05_synthwave_rap_sunset.mp3 (2min56) | Synthwave + boom bap, talk-box | Nostalgia, clássicos (Vice City, SA) | Runware |
| musicas/trilha_06_synthwave_rap_chase.mp3 (1min08) | Synthwave + phonk, perseguição | Ação, cortes rápidos, fuga da polícia | Runware |
| musicas/trilha_04_suspense_curiosidades.mp3 (7,6s) | Suspense e mistério | Ganchos e vinhetas de "você sabia?" | Runware (MiniMax Music 2.6) |

Para gerar mais: `RUNWARE_KEY_FILE=<arquivo da chave> python3 tools/runware_music.py jobs.json library/musicas` (a chave nunca vai para o repositório).
