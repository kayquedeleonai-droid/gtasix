# GTAVI | MISSION PASSED

Sistema de produção do canal **@GTAVI-MISSIONPASSED** no YouTube.

- **Fase 1 (até o lançamento):** Shorts de curiosidades de toda a franquia GTA.
- **Fase 2 (pós-lançamento):** cortes editados dos melhores momentos do GTA VI.

## Estrutura

- `brand/`: identidade visual (perfil, capa, descrição). Para regenerar: `python3 brand/make_brand.py`

- `app/central.html`: app Central do Canal (agenda da semana, banco de pautas, meta, fontes de cortes), publicado em https://claude.ai/artifact/SLYeNAbXCnMLNsZRPg8GHb
- `data/curiosidades.json`: banco de curiosidades (fonte das pautas)
- `docs/estrategia.md`: plano de crescimento e monetização
- `tools/`: `render_short.py` (edição), `runware_image.py` e `runware_music.py` (geração; chave fora do repo)
- `producao/`: um projeto por vídeo (o primeiro: `2026-11-09_gta3-11-setembro`)
- `.claude/skills/`: gta-pesquisa, gta-roteiro, gta-curadoria, gta-short, gta-publicacao, gta-cortes, gta-monetizacao, gta-diario
