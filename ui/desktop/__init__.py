from ui.desktop.home import Home
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = int(0.8 * screen_width)
    window_height = int(0.8 * screen_height)

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app = Home(root)
    root.mainloop()
