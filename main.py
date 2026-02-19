import os
import re
import sys
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class MainUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(default=resource_path("icon.ico"))
        self.title("ADOFAI Map Finder")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.title_font = ("Noto Sans KR", 28, "bold")
        self.custom_font = ("Noto Sans KR", 15)
        self.btn_font = ("Noto Sans KR", 16)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="ADOFAI 창작마당 맵 리스트", font=self.title_font)
        self.title_label.grid(row=0, column=0, padx=20, pady=(25, 15), sticky="w")

        self.search_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", corner_radius=10)
        self.search_frame.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="ew", ipadx=10, ipady=10)

        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.search_var,
            font=self.custom_font,
            placeholder_text="검색어를 입력하세요...",
            width=300,
            height=35,
            border_width=1
        )
        self.search_entry.pack(side="left", padx=(10, 15))
        self.search_entry.bind("<Return>", self.update_list)

        self.check_artist = ctk.CTkCheckBox(self.search_frame, text="작곡가", font=self.custom_font, width=60,
                                            command=self.update_list)
        self.check_artist.pack(side="left", padx=10)
        self.check_artist.select()

        self.check_author = ctk.CTkCheckBox(self.search_frame, text="제작자", font=self.custom_font, width=60,
                                            command=self.update_list)
        self.check_author.pack(side="left", padx=10)
        self.check_author.select()

        self.check_song = ctk.CTkCheckBox(self.search_frame, text="제목", font=self.custom_font, width=60,
                                          command=self.update_list)
        self.check_song.pack(side="left", padx=10)
        self.check_song.select()

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="검색",
            font=self.custom_font,
            command=self.update_list,
            width=80,
            height=35,
            corner_radius=8
        )
        self.search_btn.pack(side="right", padx=(15, 10))

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="nsew")

        self.all_maps = []
        self.load_maps()

    def load_maps(self):
        base_path = r"C:\Program Files (x86)\Steam\steamapps\workshop\content\977950"

        if not os.path.exists(base_path):
            return

        for folder in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder)
            if os.path.isdir(folder_path):
                adofai_file = os.path.join(folder_path, "main.adofai")
                if os.path.exists(adofai_file):
                    artist, author, song = self.extract_song_info(adofai_file)
                    self.all_maps.append((artist, author, song, folder_path))

        self.all_maps.sort(key=lambda x: x[2].lower())
        self.update_list()

    def update_list(self, event=None):
        query = self.search_var.get().lower()
        use_artist = self.check_artist.get()
        use_author = self.check_author.get()
        use_song = self.check_song.get()

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for artist, author, song, folder_path in self.all_maps:
            if query:
                match = False
                if use_artist and query in artist.lower(): match = True
                if use_author and query in author.lower(): match = True
                if use_song and query in song.lower(): match = True
                if not match:
                    continue

            display_parts = []
            if use_artist:
                display_parts.append(artist)
            if use_author:
                display_parts.append(author)
            if use_song:
                display_parts.append(song)

            if not display_parts:
                display_name = "표시할 항목 없음"
            else:
                display_name = " - ".join(display_parts)

            self.add_button(display_name, folder_path)

    def extract_song_info(self, filepath):
        artist = "Unknown"
        author = "Unknown"
        song = "Unknown"
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                content = f.read()

                artist_match = re.search(r'"artist"\s*:\s*"((?:\\.|[^"\\])*)"', content)
                if artist_match:
                    raw_artist = artist_match.group(1).replace('\\"', '"').replace('\\n', ' ')
                    artist = re.sub(r'<[^>]+>', '', raw_artist).strip()

                author_match = re.search(r'"author"\s*:\s*"((?:\\.|[^"\\])*)"', content)
                if author_match:
                    raw_author = author_match.group(1).replace('\\"', '"').replace('\\n', ' ')
                    author = re.sub(r'<[^>]+>', '', raw_author).strip()

                song_match = re.search(r'"song"\s*:\s*"((?:\\.|[^"\\])*)"', content)
                if song_match:
                    raw_song = song_match.group(1).replace('\\"', '"').replace('\\n', ' ')
                    song = re.sub(r'<[^>]+>', '', raw_song).strip()
        except:
            pass
        return artist, author, song

    def add_button(self, title, path):
        btn = ctk.CTkButton(
            self.scroll_frame,
            text=title,
            font=self.btn_font,
            fg_color="#333333",
            hover_color="#444444",
            text_color="#E0E0E0",
            anchor="w",
            height=45,
            corner_radius=8,
            command=lambda p=path: self.copy_path(p)
        )
        btn.pack(pady=4, fill="x", padx=5)

    def copy_path(self, path):
        self.clipboard_clear()
        self.clipboard_append(path)
        self.update()


if __name__ == "__main__":
    app = MainUI()
    app.mainloop()