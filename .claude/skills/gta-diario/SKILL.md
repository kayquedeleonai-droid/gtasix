---
name: gta-diario
description: Rotina diária do canal GTAVI | MISSION PASSED - escolhe as pautas do dia, produz 3 Shorts completos, prepara a publicação e organiza tudo nas pastas do dia. Use quando pedirem "os vídeos de hoje", "rodar o dia" ou ao disparar a tarefa agendada.
---

# Rotina diária

1. **Planejar**: ler `data/curiosidades.json`; escolher 3 itens "checada" (variar jogo e formato; respeitar o calendário do app Central do Canal).
   Se houver menos de 10 "checada", rodar a skill `gta-pesquisa` antes.
2. **Para cada pauta**: `gta-roteiro` → `gta-short` → `gta-publicacao`. Pasta: `producao/<AAAA-MM-DD>_<slug>/`.
3. **Organizar no Drive** (`Canais/GTAVI-MissionPassed/02_Producao/Semana_<seg>_a_<dom>/<n>_<Dia>_<MM-DD>/`):
   criar a pasta da semana se não existir. Pela nuvem, o conector do Drive só aceita texto: subir `publicacao.md`/roteiro;
   o MP4 vai pelo repositório ou rodando o sistema no PC (G:\Meu Drive\...), onde a cópia é direta.
4. **Atualizar status**: curiosidade → "produzido"; no app Central do Canal, marcar o post do dia como "pronto".
5. **Resumo final**: lista dos 3 vídeos com título, horário sugerido e o que precisa de aprovação humana.

Custos por dia (3 Shorts): ~150 créditos Magnific (voz) + ~US$ 0,02 de imagens no Runware.
