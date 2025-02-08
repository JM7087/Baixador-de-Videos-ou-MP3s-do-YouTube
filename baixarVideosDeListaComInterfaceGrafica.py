import yt_dlp
import re
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel

def extrair_link_video(linha):
    # Extrai o link do vídeo a partir de uma linha do arquivo
    match = re.search(r'https://www\.youtube\.com/watch\?v=[\w-]+', linha)
    if match:
        return match.group(0)
    return None

def download_video(video_url, pasta_para_salvar, contador_atual, total_videos, ffmpeg_caminho, formato, progress_callback):
    try:
        if formato == 1:
            # Opções para download de vídeo
            ydl_opts = {
                'outtmpl': f'{pasta_para_salvar}/%(title)s.%(ext)s',
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_caminho,
                'progress_hooks': [progress_callback],
            }
        elif formato == 2:
            # Opções para download de áudio (MP3)
            ydl_opts = {
                'outtmpl': f'{pasta_para_salvar}/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': ffmpeg_caminho,
                'progress_hooks': [progress_callback],
            }
        else:
            print(f'Formato inválido: {formato}')
            return
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            titulo = info_dict.get('title', 'Título Desconhecido')
            ydl.download([video_url])
        print(f'Download completo ({contador_atual}/{total_videos}): {video_url}')
        return titulo
    except Exception as e:
        # Aviso: operações de interface na thread secundária podem ocasionar problemas.
        QMessageBox.critical(None, "Erro", f"Erro ao baixar {video_url}: {e}")
        return None

def download_videos_links_arquivo(arquivo_com_links, pasta_para_salvar, ffmpeg_caminho, formato, progress_callback):
    try:
        with open(arquivo_com_links, 'r', encoding='utf-8', errors='ignore') as file:
            video_urls = file.readlines()
            links_validos = [extrair_link_video(linha) for linha in video_urls if extrair_link_video(linha)]
            
            total_videos = len(links_validos)
            print(f'Total de vídeos a serem baixados: {total_videos}')
            
            for contador, link in enumerate(links_validos, start=1):
                # Define o hook de progresso para cada vídeo
                def hook(d, contador=contador, total_videos=total_videos):
                    if d.get('status') == 'downloading':
                        progress_callback(d, contador, total_videos)
                    elif d.get('status') == 'finished':
                        progress_callback({'status': 'finished'}, contador, total_videos)
                
                titulo = download_video(link, pasta_para_salvar, contador, total_videos, ffmpeg_caminho, formato, hook)
                # Garante que a barra mostre 100% ao final de cada vídeo
                progress_callback({'status': 'finished'}, contador, total_videos)
        QMessageBox.information(None, "Sucesso", "Baixa concluída com sucesso!")
    except Exception as e:
        QMessageBox.critical(None, "Erro", f"Erro ao baixar vídeos: {e}")

class DownloadThread(QtCore.QThread):
    # Sinal enviando: número do vídeo atual, total de vídeos e percentual de download
    progress = QtCore.pyqtSignal(int, int, int)
    finished = QtCore.pyqtSignal()

    def __init__(self, arquivo, pasta, ffmpeg_caminho, formato, link=None):
        super().__init__()
        self.arquivo = arquivo
        self.pasta = pasta
        self.ffmpeg_caminho = ffmpeg_caminho
        self.formato = formato
        self.link = link

    def run(self):
        if self.link:
            download_video(
                self.link,
                self.pasta,
                1,
                1,
                self.ffmpeg_caminho,
                self.formato,
                lambda d: self.progress_callback(d, 1, 1)
            )
        else:
            download_videos_links_arquivo(
                self.arquivo,
                self.pasta,
                self.ffmpeg_caminho,
                self.formato,
                lambda d, contador, total_videos: self.progress_callback(d, contador, total_videos)
            )
        self.finished.emit()

    def progress_callback(self, d, contador, total_videos):
        # Calcula o percentual se possível
        if d.get('status') == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                percentual = int(d.get('downloaded_bytes', 0) / total_bytes * 100)
            else:
                percentual = 0
            self.progress.emit(contador, total_videos, percentual)
        elif d.get('status') == 'finished':
            self.progress.emit(contador, total_videos, 100)

class VideoDownloaderApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Baixador de Vídeos é MP3 do YouTube')
        # Ajuste o tamanho para acomodar o label de créditos
        self.setFixedSize(400, 350)

        layout = QtWidgets.QGridLayout()

        self.label_link = QtWidgets.QLabel('Link do vídeo:')
        layout.addWidget(self.label_link, 0, 0)

        self.texto_link = QtWidgets.QLineEdit(self)
        self.texto_link.textChanged.connect(self.verificar_campos)
        layout.addWidget(self.texto_link, 0, 1, 1, 2)

        self.label_ou = QtWidgets.QLabel('OU')
        self.label_ou.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_ou, 1, 0, 1, 3)

        self.label_arquivo = QtWidgets.QLabel('Arquivo de links:')
        layout.addWidget(self.label_arquivo, 2, 0)

        self.texto_arquivo = QtWidgets.QLineEdit(self)
        self.texto_arquivo.textChanged.connect(self.verificar_campos)
        layout.addWidget(self.texto_arquivo, 2, 1)

        self.botao_selecionar_arquivo = QtWidgets.QPushButton('Selecione o arquivo', self)
        self.botao_selecionar_arquivo.clicked.connect(self.selecionar_arquivo)
        layout.addWidget(self.botao_selecionar_arquivo, 2, 2)

        self.label_ou2 = QtWidgets.QLabel('É')
        self.label_ou2.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_ou2, 3, 0, 1, 3)

        self.label_pasta = QtWidgets.QLabel('Pasta para salvar:')
        layout.addWidget(self.label_pasta, 4, 0)

        self.texto_pasta = QtWidgets.QLineEdit(self)
        self.texto_pasta.textChanged.connect(self.verificar_campos)
        layout.addWidget(self.texto_pasta, 4, 1)

        self.botao_escolher_pasta = QtWidgets.QPushButton('Selecione a pasta', self)
        self.botao_escolher_pasta.clicked.connect(self.escolher_pasta)
        layout.addWidget(self.botao_escolher_pasta, 4, 2)

        self.label_formato = QtWidgets.QLabel('Formato:')
        layout.addWidget(self.label_formato, 5, 0)

        self.combo_formato = QtWidgets.QComboBox(self)
        self.combo_formato.addItems(['Vídeo', 'MP3'])
        layout.addWidget(self.combo_formato, 5, 1)

        self.botao_baixar_videos = QtWidgets.QPushButton('Baixar Vídeos/MP3', self)
        self.botao_baixar_videos.setEnabled(False)
        self.botao_baixar_videos.clicked.connect(self.baixar_videos)
        layout.addWidget(self.botao_baixar_videos, 6, 0, 1, 3)

        # Label para indicar qual vídeo está sendo baixado
        self.label_progresso = QLabel(self)
        layout.addWidget(self.label_progresso, 7, 0, 1, 3)

        # Barra de progresso para mostrar a porcentagem do download do vídeo atual
        self.barra_progresso = QtWidgets.QProgressBar(self)
        self.barra_progresso.setRange(0, 100)
        layout.addWidget(self.barra_progresso, 8, 0, 1, 3)
        # Inicialmente oculta
        self.barra_progresso.hide()

        # Label de créditos centralizado no final da janela
        self.label_creditos = QLabel("Desenvolvido By João Marcos - JM7087", self)
        self.label_creditos.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_creditos, 9, 0, 1, 3)

        self.label_version = QLabel("Versão 1.0 BETA", self)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label_version, 10, 0, 1, 3)

        self.setLayout(layout)

    def selecionar_arquivo(self):
        arquivo, _ = QFileDialog.getOpenFileName(self, 'Selecione o arquivo de links', '', 'Text Files (*.txt)')
        if arquivo:
            self.texto_arquivo.setText(arquivo)
        self.verificar_campos()

    def escolher_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, 'Selecione a pasta para salvar os vídeos')
        if pasta:
            self.texto_pasta.setText(pasta)
        self.verificar_campos()

    def verificar_campos(self):
        # Habilita o botão de download se houver pasta e (arquivo ou link)
        if self.texto_pasta.text() and (self.texto_arquivo.text() or self.texto_link.text()):
            self.botao_baixar_videos.setEnabled(True)
        else:
            self.botao_baixar_videos.setEnabled(False)

    def atualizar_progresso(self, contador, total_videos, percentual):
        # Atualiza a label com a contagem e a barra de progresso com o percentual
        self.label_progresso.setText(f"Baixando vídeo {contador} de {total_videos}")
        self.barra_progresso.setValue(percentual)

    def baixar_videos(self):
        arquivo = self.texto_arquivo.text()
        link = self.texto_link.text()
        pasta = self.texto_pasta.text()
        formato = self.combo_formato.currentText()

        if formato == 'Vídeo':
            formato = 1
        elif formato == 'MP3':
            formato = 2
        else:
            QMessageBox.critical(self, "Erro", "Formato inválido")
            return
        
        # caminho relativo ao arquivo ffmpeg
        ffmpeg_caminho = './ffmpeg/bin/ffmpeg.exe'

        # caminho absoluto ao arquivo ffmpeg para compilar o executável
        # ffmpeg_caminho = r'C:\Users\joaom\OneDrive\Documentos\VisualStudioCodeProjects\botDeBaixarVideosDoYouTubePython\ffmpeg\bin\ffmpeg.exe'

        if not os.path.isfile(ffmpeg_caminho):
            QMessageBox.critical(self, "Erro", "FFmpeg não encontrado! Verifique o caminho.")
            return

        # Exibe a barra de progresso somente quando o download inicia
        self.barra_progresso.show()

        # Desabilita os botões enquanto o download ocorre
        self.texto_link.setEnabled(False)
        self.texto_arquivo.setEnabled(False)
        self.texto_pasta.setEnabled(False)
        self.combo_formato.setEnabled(False)
        self.botao_selecionar_arquivo.setEnabled(False)
        self.botao_escolher_pasta.setEnabled(False)
        self.botao_baixar_videos.setEnabled(False)


        self.thread = DownloadThread(arquivo, pasta, ffmpeg_caminho, formato, link if link else None)
        self.thread.progress.connect(self.atualizar_progresso)
        self.thread.finished.connect(self.download_concluido)
        self.thread.start()

    def download_concluido(self):
    # Habilita os botões e atualiza a interface após o término do download
     self.texto_link.setEnabled(True)
     self.texto_arquivo.setEnabled(True)
     self.texto_pasta.setEnabled(True)
     self.combo_formato.setEnabled(True)
     self.botao_baixar_videos.setEnabled(True)
     self.botao_selecionar_arquivo.setEnabled(True)
     self.botao_escolher_pasta.setEnabled(True)
     self.label_progresso.setText("Download concluído! Pronto para novo download.")
     self.barra_progresso.setValue(0)
     self.barra_progresso.hide()  # Oculta a barra após o download

    # Limpa os inputs de link e arquivo
     self.texto_link.clear()
     self.texto_arquivo.clear()

     msg = QMessageBox()
     msg.setIcon(QMessageBox.Information)
     msg.setText("Download concluído!")
     msg.setWindowTitle("Sucesso")
     msg.setStandardButtons(QMessageBox.Ok)
     msg.setWindowModality(QtCore.Qt.NonModal)
     msg.show()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = VideoDownloaderApp()
    ex.show()
    sys.exit(app.exec_())
