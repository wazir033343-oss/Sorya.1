
import os
import threading
import requests

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window

KV = """
BoxLayout:
    orientation: "vertical"
    padding: 18
    spacing: 12
    canvas.before:
        Color:
            rgba: 0.07, 0.05, 0.16, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "[b]SORYA[/b] ❤️"
        markup: True
        font_size: "34sp"
        color: 0.85, 0.65, 1, 1
        size_hint_y: 0.15

    Label:
        text: "Hello jaan! Main tumhari AI assistant hoon."
        font_size: "16sp"
        size_hint_y: 0.10

    TextInput:
        id: api
        hint_text: "Gemini API Key"
        password: True
        multiline: False
        size_hint_y: 0.09

    ScrollView:
        Label:
            id: chat
            text: "SORYA: Mujhse baat karo! ❤️"
            size_hint_y: None
            height: self.texture_size[1]
            text_size: self.width, None
            halign: "left"
            valign: "top"
            font_size: "16sp"

    TextInput:
        id: message
        hint_text: "Yahan message likho..."
        multiline: False
        size_hint_y: 0.10

    Button:
        text: "Send ❤️"
        size_hint_y: 0.12
        background_color: 0.55, 0.25, 0.85, 1
        on_release: app.send_message()
"""

class SoryaApp(App):
    def build(self):
        self.title = "SORYA AI"
        Window.clearcolor = (0.07, 0.05, 0.16, 1)
        return Builder.load_string(KV)

    def send_message(self):
        key = self.root.ids.api.text.strip()
        message = self.root.ids.message.text.strip()

        if not key or not message:
            self.add_chat("SORYA: API key aur message enter karo.")
            return

        self.root.ids.message.text = ""
        self.add_chat("Tum: " + message)
        self.add_chat("SORYA: Soch rahi hoon... ❤️")

        threading.Thread(
            target=self.ask_gemini,
            args=(key, message),
            daemon=True
        ).start()

    def add_chat(self, text):
        label = self.root.ids.chat
        label.text += "\n\n" + text

    def ask_gemini(self, key, message):
        try:
            url = (
                "https://generativelanguage.googleapis.com/"
                "v1beta/models/gemini-2.5-flash:generateContent"
            )

            data = {
                "system_instruction": {
                    "parts": [{
                        "text": (
                            "Tum SORYA ho, ek friendly Pakistani "
                            "female AI assistant. Roman Urdu mein "
                            "sweet aur respectful jawab do."
                        )
                    }]
                },
                "contents": [{
                    "role": "user",
                    "parts": [{"text": message}]
                }]
            }

            response = requests.post(
                url,
                params={"key": key},
                json=data,
                timeout=60
            )
            result = response.json()

            if response.ok:
                answer = result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                answer = "API Error: " + str(result)

        except Exception as e:
            answer = "Connection Error: " + str(e)

        Clock.schedule_once(
            lambda dt: self.add_chat("SORYA: " + answer)
        )

SoryaApp().run()

