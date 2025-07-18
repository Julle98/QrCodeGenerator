import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageTk
import qrcode

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.base_font_size = 12
        self.base_button_height = 1
        self.base_button_width = 20
        self.languages = {
            'fi': {
                'title': "QR-koodin generaattori",
                'content': "Sisältö:",
                'size': "Koko (px):",
                'margin': "Marginaali:",
                'choose_fg': "Valitse etuväri",
                'choose_bg': "Valitse taustaväri",
                'generate': "Generoi QR-koodi",
                'save': "Lataa QR-koodi",
                'error_content': "Syötä sisältö QR-koodille.",
                'error': "Virhe",
                'saved': "Tallennettu",
                'saved_msg': "QR-koodi tallennettu: {file_path}",
                'error_save': "Generoi QR-koodi ennen tallennusta.",
                'lang': "Kieli:",
                'fi': "Suomi",
                'en': "Englanti"
            },
            'en': {
                'title': "QR Code Generator",
                'content': "Content:",
                'size': "Size (px):",
                'margin': "Margin:",
                'choose_fg': "Choose foreground color",
                'choose_bg': "Choose background color",
                'generate': "Generate QR Code",
                'save': "Download QR Code",
                'error_content': "Please enter content for the QR code.",
                'error': "Error",
                'saved': "Saved",
                'saved_msg': "QR code saved: {file_path}",
                'error_save': "Generate QR code before saving.",
                'lang': "Language:",
                'fi': "Finnish",
                'en': "English"
            }
        }
        self.lang = tk.StringVar(value='fi')
        self.root.title(self.languages[self.lang.get()]['title'])
        self.content_var = tk.StringVar()
        self.size_var = tk.IntVar(value=300)
        self.margin_var = tk.IntVar(value=4)
        self.fg_color = "black"
        self.bg_color = "white"
        self.qr_img = None

        self.create_widgets()
        self.root.bind('<Configure>', self.on_resize)

    def create_widgets(self):
        self.font = ("Arial", self.base_font_size)
        lang_frame = tk.Frame(self.root)
        self.lang_label = tk.Label(lang_frame, text=self.languages[self.lang.get()]['lang'], font=self.font)
        self.lang_label.pack(side=tk.LEFT)
        self.radio_fi = tk.Radiobutton(lang_frame, text=self.languages['fi']['fi'], variable=self.lang, value='fi', command=self.update_language, font=self.font)
        self.radio_fi.pack(side=tk.LEFT)
        self.radio_en = tk.Radiobutton(lang_frame, text=self.languages['en']['en'], variable=self.lang, value='en', command=self.update_language, font=self.font)
        self.radio_en.pack(side=tk.LEFT)
        lang_frame.pack(pady=5)

        self.labels = {}
        self.labels['content'] = tk.Label(self.root, text=self.languages[self.lang.get()]['content'], font=self.font)
        self.labels['content'].pack()
        self.entry_content = tk.Entry(self.root, textvariable=self.content_var, width=40, font=self.font)
        self.entry_content.pack()

        self.labels['size'] = tk.Label(self.root, text=self.languages[self.lang.get()]['size'], font=self.font)
        self.labels['size'].pack()
        self.entry_size = tk.Entry(self.root, textvariable=self.size_var, font=self.font)
        self.entry_size.pack()

        self.labels['margin'] = tk.Label(self.root, text=self.languages[self.lang.get()]['margin'], font=self.font)
        self.labels['margin'].pack()
        self.entry_margin = tk.Entry(self.root, textvariable=self.margin_var, font=self.font)
        self.entry_margin.pack()

        self.btn_fg = tk.Button(self.root, text=self.languages[self.lang.get()]['choose_fg'], command=self.choose_fg, font=self.font, height=self.base_button_height, width=self.base_button_width)
        self.btn_fg.pack()
        self.btn_bg = tk.Button(self.root, text=self.languages[self.lang.get()]['choose_bg'], command=self.choose_bg, font=self.font, height=self.base_button_height, width=self.base_button_width)
        self.btn_bg.pack()
        self.btn_generate = tk.Button(self.root, text=self.languages[self.lang.get()]['generate'], command=self.generate_qr, font=self.font, height=self.base_button_height, width=self.base_button_width)
        self.btn_generate.pack()
        self.btn_save = tk.Button(self.root, text=self.languages[self.lang.get()]['save'], command=self.save_qr, font=self.font, height=self.base_button_height, width=self.base_button_width)
        self.btn_save.pack()

        self.qr_label = tk.Label(self.root)
        self.qr_label.pack(pady=10)

    def on_resize(self, event):
        # Skaalaa fonttia ja nappuloita ikkunan koon mukaan
        w = max(event.width, 300)
        h = max(event.height, 400)
        font_size = max(self.base_font_size, int(min(w, h) / 30))
        self.font = ("Arial", font_size)
        # Päivitä fontit
        self.lang_label.config(font=self.font)
        self.radio_fi.config(font=self.font)
        self.radio_en.config(font=self.font)
        for lbl in self.labels.values():
            lbl.config(font=self.font)
        self.entry_content.config(font=self.font)
        self.entry_size.config(font=self.font)
        self.entry_margin.config(font=self.font)
        self.btn_fg.config(font=self.font)
        self.btn_bg.config(font=self.font)
        self.btn_generate.config(font=self.font)
        self.btn_save.config(font=self.font)

    def update_language(self):
        lang = self.lang.get()
        self.root.title(self.languages[lang]['title'])
        self.lang_label.config(text=self.languages[lang]['lang'])
        self.radio_fi.config(text=self.languages['fi']['fi'])
        self.radio_en.config(text=self.languages['en']['en'])
        self.labels['content'].config(text=self.languages[lang]['content'])
        self.labels['size'].config(text=self.languages[lang]['size'])
        self.labels['margin'].config(text=self.languages[lang]['margin'])
        self.btn_fg.config(text=self.languages[lang]['choose_fg'])
        self.btn_bg.config(text=self.languages[lang]['choose_bg'])
        self.btn_generate.config(text=self.languages[lang]['generate'])
        self.btn_save.config(text=self.languages[lang]['save'])

    def choose_fg(self):
        color = colorchooser.askcolor(title="Valitse etuväri")
        if color[1]:
            self.fg_color = color[1]

    def choose_bg(self):
        color = colorchooser.askcolor(title="Valitse taustaväri")
        if color[1]:
            self.bg_color = color[1]

    def generate_qr(self):
        content = self.content_var.get()
        size = self.size_var.get()
        margin = self.margin_var.get()
        lang = self.lang.get()
        if not content:
            messagebox.showerror(self.languages[lang]['error'], self.languages[lang]['error_content'])
            return
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=max(1, size // 40),
            border=margin
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color).convert('RGB')
        img = img.resize((size, size), Image.NEAREST)
        self.qr_img = img
        tk_img = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=tk_img)
        self.qr_label.image = tk_img
        # Suurenna ikkuna automaattisesti jos QR-koodi ei näy
        self.root.update_idletasks()
        qr_label_bbox = self.qr_label.bbox()
        if qr_label_bbox:
            qr_bottom = qr_label_bbox[1] + qr_label_bbox[3]
            win_height = self.root.winfo_height()
            if qr_bottom > win_height:
                self.root.geometry(f"{self.root.winfo_width()}x{qr_bottom+50}")

    def save_qr(self):
        lang = self.lang.get()
        if self.qr_img:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.qr_img.save(file_path)
                messagebox.showinfo(self.languages[lang]['saved'], self.languages[lang]['saved_msg'].format(file_path=file_path))
        else:
            messagebox.showerror(self.languages[lang]['error'], self.languages[lang]['error_save'])

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()
