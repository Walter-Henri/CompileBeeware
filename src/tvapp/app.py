import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
import os
from .stream_manager import StreamManager
from .config import DEFAULT_LIVE_URLS

class TVApp(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.stream_manager = StreamManager()

        # Create a box to hold all content
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Title
        title_label = toga.Label(
            "TVApp - Streaming de Vídeos",
            style=Pack(text_align="center", font_size=18, padding_bottom=20)
        )

        # Input for live name
        self.live_name_input = toga.TextInput(
            placeholder="Digite o nome da live (ex: live1, live2, live3, live4)",
            style=Pack(flex=1, padding=5)
        )
        
        # Button to open live
        open_button = toga.Button(
            "Abrir Live",
            on_press=self.open_live,
            style=Pack(padding_left=10, padding=5)
        )

        # Button to update links
        update_button = toga.Button(
            "Atualizar Links",
            on_press=self.update_links,
            style=Pack(padding_left=10, padding=5)
        )

        input_box = toga.Box(style=Pack(direction=ROW, padding_bottom=10))
        input_box.add(self.live_name_input)
        input_box.add(open_button)
        input_box.add(update_button)

        # Video player area (using WebView for HTML5 video)
        self.video_player = toga.WebView(style=Pack(flex=1, height=400))

        # Status message area
        self.status_label = toga.Label(
            "Digite o nome de uma live e clique em 'Abrir Live'",
            style=Pack(padding_top=10, text_align="center")
        )

        # Error message area
        self.error_label = toga.Label("", style=Pack(color="red", padding_top=10))

        main_box.add(title_label)
        main_box.add(input_box)
        main_box.add(self.video_player)
        main_box.add(self.status_label)
        main_box.add(self.error_label)

        self.main_window.content = main_box
        self.main_window.show()

    async def open_live(self, widget):
        live_name = self.live_name_input.value.strip()
        self.error_label.text = ""
        self.status_label.text = "Buscando link da live..."

        if not live_name:
            self.error_label.text = "Por favor, insira o nome da live."
            self.status_label.text = ""
            return

        try:
            video_url = await self.stream_manager.get_live_link(live_name)
            
            if video_url:
                # Create HTML5 video player
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <style>
                        body {{
                            margin: 0;
                            padding: 20px;
                            background-color: #000;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }}
                        video {{
                            width: 100%;
                            height: auto;
                            max-width: 800px;
                        }}
                    </style>
                </head>
                <body>
                    <video controls autoplay>
                        <source src="{video_url}" type="application/x-mpegURL">
                        Seu navegador não suporta o elemento de vídeo.
                    </video>
                </body>
                </html>
                """
                self.video_player.set_content("", html_content)
                self.status_label.text = f"Reproduzindo: {live_name}"
            else:
                self.error_label.text = f"Nenhum link M3U8 disponível para '{live_name}'"
                self.status_label.text = ""
        except Exception as e:
            self.error_label.text = f"Erro ao buscar link: {str(e)}"
            self.status_label.text = ""

    async def update_links(self, widget):
        self.status_label.text = "Atualizando links das lives..."
        self.error_label.text = ""


        try:
            success = await self.stream_manager.update_live_links(DEFAULT_LIVE_URLS)
            if success:
                self.status_label.text = "Links atualizados com sucesso!"
            else:
                self.error_label.text = "Erro ao atualizar links"
                self.status_label.text = ""
        except Exception as e:
            self.error_label.text = f"Erro ao atualizar links: {str(e)}"
            self.status_label.text = ""


def main():
    return TVApp()

