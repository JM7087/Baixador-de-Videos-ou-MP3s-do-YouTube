# Changelog - Correção do Bot de Download do YouTube

## Data: 30/06/2026

### Problema Identificado
O bot não estava mais baixando vídeos do YouTube devido a dois problemas:
1. **yt-dlp desatualizado**: Versão 2024.11.4 (desatualizada)
2. **Erro de extração de assinatura**: YouTube alterou sua API, causando erros de "Signature extraction failed"

### Correções Aplicadas

#### 1. Atualização do yt-dlp
- **Versão anterior**: 2024.11.4
- **Versão atual**: 2026.6.9
- **Comando usado**: `python -m pip install --upgrade yt-dlp`

#### 2. Configuração do Player Client Android
Adicionada a opção `'extractor_args': {'youtube': {'player_client': ['android']}}` nos arquivos:
- `baixarVideosDeListaComInterfaceGrafica.py`
- `baixarVideosDeLista.py`

Esta configuração evita a necessidade de instalar Node.js ou outro runtime JavaScript, usando o client Android do YouTube que não requer descriptografia de assinaturas.

### Arquivos Modificados
- ✅ baixarVideosDeListaComInterfaceGrafica.py
- ✅ baixarVideosDeLista.py

### Atualização 2 - Melhor Qualidade (30/06/2026)
**Problema**: Vídeos sendo baixados em 360p (baixa qualidade)

**Solução**: 
- Player client alterado de `android` para `android_vr` (com fallback)
- String de formato otimizada para garantir melhor qualidade

**Resultado**: Downloads agora em **1080p (Full HD)** quando disponível!

### Atualização 3 - Suporte a Playlists (30/06/2026)
**Nova Funcionalidade**: Download de playlists completas do YouTube

**Implementações**:
- ✅ Detecção automática de URLs de playlist
- ✅ Download de todos os vídeos da playlist automaticamente
- ✅ Nomenclatura com índice da playlist (1 - Nome, 2 - Nome, etc.)
- ✅ Suporte a playlists tanto na interface gráfica quanto no arquivo de links
- ✅ Tratamento de erros para continuar mesmo se algum vídeo falhar

**Como usar**:
- **Interface Gráfica**: Cole o link da playlist no campo "Link do vídeo/playlist"
- **Arquivo de Links**: Adicione a URL da playlist no arquivo `linkesDeVideos.txt`

**Formato da URL de playlist**:
```
https://www.youtube.com/playlist?list=CODIGO_DA_PLAYLIST
```

### Como Manter Atualizado
Para evitar problemas futuros, recomenda-se atualizar o yt-dlp regularmente:
```bash
python -m pip install --upgrade yt-dlp
```

### Status
✅ **Funcionando perfeitamente** - Downloads em alta qualidade (até 1080p) e suporte a playlists completas!
