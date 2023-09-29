import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from CTkListbox import *
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates


class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Candlestick Chart")
        self.left_frame = None
        self.center_frame = None
        self.stock_listbox = None
        self.fig = None
        self.ax = None
        self.canvas = None
        self.canvas_widget = None
        self.center_canvas = None
        self.create_ui()
        self.populate_stock_list()

    def on_mousewheel(self, event):
        self.center_canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def create_ui(self):
        # Create  left
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill=ctk.Y)
        self.stock_listbox = CTkListbox(self.left_frame, command=self.on_stock_selected)
        self.stock_listbox.configure(highlight_color="green", hover_color="blue", text_color="white")
        self.stock_listbox.pack(fill=ctk.BOTH, expand=True)

        # Create center

        self.center_canvas = ctk.CTkCanvas(self.root)
        self.center_canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        scrollbar = ctk.CTkScrollbar(self.root, orientation=ctk.VERTICAL, command=self.center_canvas.yview)
        scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        self.center_canvas.configure(yscrollcommand=scrollbar.set)

        self.center_frame = ctk.CTkFrame(self.center_canvas)
        self.center_canvas.create_window((0, 0), window=self.center_frame, anchor=ctk.NW)
        self.center_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Create a Matplotlib figure and canvas for the candlestick chart
        # self.fig = Figure(figsize=(6, 4))
        # self.ax = self.fig.add_subplot(111)
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.center_frame)
        #
        # root_bg_color = self.root.cget("bg")
        # print(root_bg_color)
        # self.canvas_widget = self.canvas.get_tk_widget()
        # self.canvas_widget.configure(bg=root_bg_color)
        # self.canvas_widget.pack(fill=ctk.BOTH, expand=True)

    def populate_stock_list(self):
        # Sample stock list (replace with your own data)
        stocks = ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN", "FB"]
        for stock in stocks:
            self.stock_listbox.insert(ctk.END, stock)

    def on_stock_selected(self, event):
        selected_stock = self.stock_listbox.get(self.stock_listbox.curselection())

        data = self.get_stock_data()

        # fig, axes = mpf.plot(data, type='candle', style='charles', returnfig=True, figratio=(2, 1))
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.clear()
        ax.xaxis_date()
        # ax.plot(range(len(data)), data, marker='o', linestyle='-', color='b')
        candlestick_ohlc(ax, zip(mdates.date2num(data['Date']), data['Open'], data['High'], data['Low'], data['Close']), width=0.6)
        ax.set_title(f"Time Series for {selected_stock}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Value")

        stock_canvas = FigureCanvasTkAgg(fig, master=self.center_frame)
        canvas_widget = stock_canvas.get_tk_widget()
        canvas_widget.pack(padx=10, pady=10)

        # stock_canvas.get_tk_widget().pack()
        # stock_canvas.draw()
        #
        # self.center_frame.update_idletasks()
        # self.center_canvas.config(scrollregion=self.center_canvas.bbox("all"))

    def get_stock_data(self):
        # Sample code to generate candlestick data (replace with your own data)
        limit = 50
        data = {
            'Date': pd.date_range('2023-01-01', periods=limit, freq='D'),
            'Open': [random.uniform(100, 150) for _ in range(limit)],
            'High': [random.uniform(150, 200) for _ in range(limit)],
            'Low': [random.uniform(50, 100) for _ in range(limit)],
            'Close': [random.uniform(100, 150) for _ in range(limit)],
        }
        df = pd.DataFrame(data=data)

        df.index = pd.DatetimeIndex(df['Date'])
        return df
