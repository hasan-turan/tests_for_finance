import customtkinter as ctk


class CloseableFrame(ctk.CTkFrame):
    def __init__(self, parent, title):
        super(CloseableFrame, self).__init__(parent)
        self.title = title

        # Create a label for the title
        title_label = ctk.CTkLabel(self, text=title)
        title_label.grid(row=0, column=0, sticky="w", padx=5)

        close_button = ctk.CTkButton(self, text="X", command=self.close)
        close_button.grid(row=0, column=1, sticky="e", padx=5)

    def close(self):
        # Hide or destroy the frame when the close button is clicked
        self.grid_forget()  # Hide the frame (use destroy() to completely remove it)
