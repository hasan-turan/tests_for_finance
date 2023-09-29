import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ClosableCanvasFrame(ctk.CTkFrame):
    def __init__(self, parent, title, figure):
        super().__init__(parent)
        self.canvas_title = title

        # Create a label for the canvas title
        title_label = ctk.CTkLabel(self, text=self.canvas_title)
        title_label.grid(row=0, column=0, sticky="w", padx=5)

        # Create a canvas
        self.canvas = FigureCanvasTkAgg(figure, master=self)

        self.canvas.get_tk_widget().grid(row=1, column=0, padx=5, pady=5)

        # Create a close button
        close_button = ctk.CTkButton(self, text="Close", command=self.close)
        close_button.grid(row=2, column=0, sticky="e", padx=5, pady=5)



    def close(self):
        # Hide or destroy the frame when the close button is clicked
        self.grid_forget()  # Hide
