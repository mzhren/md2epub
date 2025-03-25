import tkinter as tk
from gui import MarkdownToEpubApp

def main():
    root = tk.Tk()
    app = MarkdownToEpubApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
