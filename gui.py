import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from main import main as cli_main


def run_cli(args):
    import sys

    sys.argv = ["pdf-ocr-translator"] + args
    try:
        cli_main()
        messagebox.showinfo("Done", "Translation finished.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_run():
    if not input_var.get() or not output_var.get():
        messagebox.showwarning("Missing", "Please select input and output files.")
        return

    args = [
        "--input",
        input_var.get(),
        "--output",
        output_var.get(),
        "--ocr-lang",
        ocr_lang_var.get(),
        "--src-lang",
        src_lang_var.get(),
        "--tgt-lang",
        tgt_lang_var.get(),
        "--translation-backend",
        backend_var.get(),
        "--dpi",
        dpi_var.get(),
        "--jpeg-quality",
        quality_var.get(),
    ]

    if font_var.get():
        args += ["--font-path", font_var.get()]
    if not allow_pivot_var.get():
        args += ["--no-pivot"]

    t = threading.Thread(target=run_cli, args=(args,), daemon=True)
    t.start()


def browse_input():
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if path:
        input_var.set(path)


def browse_output():
    path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if path:
        output_var.set(path)


def browse_font():
    path = filedialog.askopenfilename(filetypes=[("Font files", "*.ttf;*.ttc")])
    if path:
        font_var.set(path)


root = tk.Tk()
root.title("PDF OCR Translator")

input_var = tk.StringVar()
output_var = tk.StringVar()
font_var = tk.StringVar()
ocr_lang_var = tk.StringVar(value="auto")
src_lang_var = tk.StringVar(value="auto")
tgt_lang_var = tk.StringVar(value="en")
backend_var = tk.StringVar(value="marian")
dpi_var = tk.StringVar(value="150")
quality_var = tk.StringVar(value="80")
allow_pivot_var = tk.BooleanVar(value=True)

row = 0

tk.Label(root, text="Input PDF").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=input_var, width=50).grid(row=row, column=1)
tk.Button(root, text="Browse", command=browse_input).grid(row=row, column=2)
row += 1

tk.Label(root, text="Output PDF").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=output_var, width=50).grid(row=row, column=1)
tk.Button(root, text="Browse", command=browse_output).grid(row=row, column=2)
row += 1

tk.Label(root, text="Font (optional)").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=font_var, width=50).grid(row=row, column=1)
tk.Button(root, text="Browse", command=browse_font).grid(row=row, column=2)
row += 1

opts = ["auto", "en", "ch", "japan", "korean"]
tk.Label(root, text="OCR language").grid(row=row, column=0, sticky="w")
tk.OptionMenu(root, ocr_lang_var, *opts).grid(row=row, column=1, sticky="w")
row += 1

src_opts = ["auto", "en", "zh", "ja", "ko"]
tk.Label(root, text="Source language").grid(row=row, column=0, sticky="w")
tk.OptionMenu(root, src_lang_var, *src_opts).grid(row=row, column=1, sticky="w")
row += 1

tgt_opts = ["en", "zh", "ja", "ko"]
tk.Label(root, text="Target language").grid(row=row, column=0, sticky="w")
tk.OptionMenu(root, tgt_lang_var, *tgt_opts).grid(row=row, column=1, sticky="w")
row += 1

backend_opts = ["marian", "argos"]
tk.Label(root, text="Translation backend").grid(row=row, column=0, sticky="w")
tk.OptionMenu(root, backend_var, *backend_opts).grid(row=row, column=1, sticky="w")
row += 1

tk.Label(root, text="DPI").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=dpi_var, width=10).grid(row=row, column=1, sticky="w")
row += 1

tk.Label(root, text="JPEG quality").grid(row=row, column=0, sticky="w")
tk.Entry(root, textvariable=quality_var, width=10).grid(row=row, column=1, sticky="w")
row += 1

tk.Checkbutton(root, text="Allow pivot via English (default on)", variable=allow_pivot_var).grid(
    row=row, column=1, sticky="w"
)
row += 1

tk.Button(root, text="Run", command=on_run).grid(row=row, column=1, pady=10)

root.mainloop()
