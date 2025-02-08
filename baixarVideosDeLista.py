import yt_dlp
import re  # Biblioteca para trabalhar com expressões regulares

def extrair_link_video(linha):
    # Expressão regular para capturar links do YouTube, desde "https" até antes de qualquer "&" ou espaço
    match = re.search(r'https://www\.youtube\.com/watch\?v=[\w-]+', linha)
    if match:
        return match.group(0)  # Retorna o link capturado
    return None  # Retorna None se não for um link de vídeo válido

def download_video(video_url, pastaParaSalva, contador_atual, total_videos, ffmpeg_caminho, formato):
    try:
        if formato == 1:  # Baixar vídeo
            ydl_opts = {
                'outtmpl': f'{pastaParaSalva}/%(title)s.%(ext)s',
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Formato alterado
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_caminho,  # Define o caminho do FFmpeg
            }
        elif formato == 2:  # Baixar MP3
            ydl_opts = {
                'outtmpl': f'{pastaParaSalva}/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': ffmpeg_caminho,  # Define o caminho do FFmpeg
            }
        else:
            print(f'Formato inválido: {formato}')
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f'Download completo ({contador_atual}/{total_videos}): {video_url}')
    except Exception as e:
        print(f'Erro ao baixar {video_url}: {e}')

def download_videos_links_arquivo(arquivoComLinksDosVideos, pastaParaSalva, ffmpeg_caminho, formato):
    with open(arquivoComLinksDosVideos, 'r', encoding='utf-8', errors='ignore') as file:
        video_urls = file.readlines()
        links_validos = [extrair_link_video(linha) for linha in video_urls if extrair_link_video(linha)]
        
        total_videos = len(links_validos)
        print(f'Total de vídeos a serem baixados: {total_videos}')
        
        for contador, link in enumerate(links_validos, start=1):
            download_video(link, pastaParaSalva, contador, total_videos, ffmpeg_caminho, formato)

# Caminho do arquivo de texto contendo os links dos vídeos
arquivoComLinksDosVideos = 'linkesDeVideos.txt'

# Caminho da pasta onde os vídeos serão salvos
pastaParaSalva = 'D:/teste'

# Caminho do FFmpeg na pasta do projeto
ffmpeg_caminho = './ffmpeg/bin/ffmpeg.exe'

# Solicitar ao usuário o formato desejado: 1 para vídeo, 2 para MP3
while True:
    formato = input("Digite 1 para baixar vídeos ou 2 para baixar MP3: ")
    if formato in ['1', '2']:
        formato = int(formato)
        break
    else:
        print("Entrada inválida. Por favor, digite 1 ou 2.")

# Baixar os vídeos
download_videos_links_arquivo(arquivoComLinksDosVideos, pastaParaSalva, ffmpeg_caminho, formato)
