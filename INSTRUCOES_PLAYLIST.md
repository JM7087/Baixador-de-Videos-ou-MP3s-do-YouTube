# 📋 Como Usar a Funcionalidade de Playlists

## 🎯 Visão Geral

O bot agora suporta download de **playlists completas** do YouTube! Todos os vídeos da playlist serão baixados automaticamente.

---

## 💻 Interface Gráfica

### Passo a Passo:

1. **Abra o aplicativo** (`baixarVideosDeListaComInterfaceGrafica.py`)

2. **Cole a URL da playlist** no campo "Link do vídeo/playlist"
   - Exemplo: `https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`

3. **Selecione a pasta** de destino

4. **Escolha o formato**:
   - **Vídeo**: Baixa em MP4 (até 1080p)
   - **MP3**: Extrai apenas o áudio

5. **Clique em "Baixar Vídeos/MP3"**

### Resultado:
- Os vídeos serão salvos com numeração: 
  - `1 - Nome do Vídeo.mp4`
  - `2 - Outro Vídeo.mp4`
  - `3 - Mais um Vídeo.mp4`
  - etc.

---

## 📄 Arquivo de Links (linkesDeVideos.txt)

### Formato do Arquivo:

```
# Vídeos individuais
https://www.youtube.com/watch?v=ABC123

# Playlists completas (todos os vídeos serão baixados)
https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf

# Você pode misturar vídeos e playlists no mesmo arquivo
https://www.youtube.com/watch?v=XYZ789
https://www.youtube.com/playlist?list=PLoutraPlaylist123

# Linhas começando com # são ignoradas (comentários)
```

### Execute:
```bash
python baixarVideosDeLista.py
```

---

## 🔍 Como Obter o Link de uma Playlist

1. Acesse o YouTube
2. Vá para a playlist que deseja baixar
3. Copie a URL da barra de endereço
4. A URL deve conter `playlist?list=` ou `&list=`

### Exemplos de URLs Válidas:

✅ `https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`

✅ `https://www.youtube.com/watch?v=ABC123&list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`

✅ `https://youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`

---

## ⚙️ Recursos da Funcionalidade

- ✅ **Detecção automática** de playlists
- ✅ **Download sequencial** de todos os vídeos
- ✅ **Numeração automática** dos arquivos
- ✅ **Tratamento de erros**: Continua mesmo se um vídeo falhar
- ✅ **Progresso em tempo real** na interface gráfica
- ✅ **Suporte a MP3 e MP4**
- ✅ **Alta qualidade** (até 1080p para vídeos)

---

## 💡 Dicas

1. **Playlists grandes**: Para playlists com muitos vídeos, o processo pode demorar. Seja paciente!

2. **Espaço em disco**: Verifique se tem espaço suficiente antes de baixar playlists grandes

3. **Qualidade**: Por padrão, o bot baixa na melhor qualidade disponível (até 1080p)

4. **Erros**: Se algum vídeo específico falhar, o bot continua com os próximos

---

## 🐛 Solução de Problemas

### "URL de playlist inválida"
- Verifique se a URL contém `list=` 
- Certifique-se de que a playlist é pública

### Downloads muito lentos
- Normal para playlists grandes
- Depende da sua velocidade de internet
- Vídeos em 1080p são maiores e demoram mais

### Vídeo específico falha
- Pode estar privado ou removido
- O bot continua automaticamente com os próximos

---

## 📞 Suporte

Desenvolvido por **João Marcos - JM7087**

Versão: 1.0 BETA (com suporte a playlists)
