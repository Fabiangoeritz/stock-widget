import argparse
from datetime import datetime
import customtkinter as ctk
import yfinance as yf


class StockWidget:
    """A lightweight desktop widget displaying live Yahoo Finance stock prices."""

    BACKGROUND_COLOR = "#111111"
    TEXT_COLOR = "#BFBFBF"
    GREEN = "#44DD44"
    RED = "#FF5555"

    WINDOW_WIDTH = 230
    WINDOW_HEIGHT = 120

    UPDATE_INTERVAL = 5000

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker.upper()

        ctk.set_appearance_mode("dark")

        self.app = ctk.CTk()
        self.app.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.app.overrideredirect(True)
        self.app.attributes("-topmost", True)
        self.app.configure(fg_color=self.BACKGROUND_COLOR)

        self.offset_x = 0
        self.offset_y = 0

        self.create_widgets()
        self.bind_events()

    def create_widgets(self) -> None:
        """Create all GUI widgets."""

        self.close_button = ctk.CTkButton(
            self.app,
            text="✕",
            width=20,
            height=20,
            fg_color="transparent",
            hover_color="#333333",
            text_color="white",
            command=self.app.destroy,
        )

        self.ticker_label = ctk.CTkLabel(
            self.app,
            text=self.ticker,
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT_COLOR,
        )
        self.ticker_label.pack(pady=(10, 0))

        self.price_label = ctk.CTkLabel(
            self.app,
            text="...",
            font=("Segoe UI", 28, "bold"),
            text_color=self.TEXT_COLOR,
        )
        self.price_label.pack()

        self.change_label = ctk.CTkLabel(
            self.app,
            text="",
            font=("Segoe UI", 14),
            text_color=self.TEXT_COLOR,
        )
        self.change_label.pack()

        self.time_label = ctk.CTkLabel(
            self.app,
            text="",
            font=("Segoe UI", 10),
            text_color="#666666",
        )
        self.time_label.pack()

    def bind_events(self) -> None:
        """Bind mouse events."""

        self.app.bind("<Enter>", self.show_close)
        self.app.bind("<Leave>", self.hide_close)

        widgets = [
            self.app,
            self.ticker_label,
            self.price_label,
            self.change_label,
            self.time_label,
        ]

        for widget in widgets:
            widget.bind("<Button-1>", self.start_move)
            widget.bind("<B1-Motion>", self.move_window)

    def start_move(self, event) -> None:
        """Remember the mouse position before dragging."""

        self.offset_x = event.x
        self.offset_y = event.y

    def move_window(self, event) -> None:
        """Move the frameless window."""

        x = self.app.winfo_pointerx() - self.offset_x
        y = self.app.winfo_pointery() - self.offset_y
        self.app.geometry(f"+{x}+{y}")

    def show_close(self, event) -> None:
        """Show the close button when hovering."""

        self.close_button.place(x=205, y=5)

    def hide_close(self, event) -> None:
        """Hide the close button."""

        self.close_button.place_forget()

    def update_price(self) -> None:
        """Fetch the latest stock price and update the widget."""

        try:
            ticker = yf.Ticker(self.ticker)
            info = ticker.fast_info

            current = info["lastPrice"]
            previous = info["previousClose"]

            diff = current - previous
            percent = diff / previous * 100

            if diff >= 0:
                color = self.GREEN
                sign = "+"
            else:
                color = self.RED
                sign = ""

            self.price_label.configure(
                text=f"{current:.2f}",
                text_color=color,
            )

            self.change_label.configure(
                text=f"{sign}{diff:.2f} ({sign}{percent:.2f}%)",
                text_color=color,
            )

            self.time_label.configure(
                text=datetime.now().strftime("%H:%M:%S")
            )

        except Exception:
            self.price_label.configure(
                text="No Data",
                text_color=self.TEXT_COLOR,
            )
            self.change_label.configure(text="")
            self.time_label.configure(text="")

        self.app.after(self.UPDATE_INTERVAL, self.update_price)

    def run(self) -> None:
        """Start the widget."""

        self.update_price()
        self.app.mainloop()


def main() -> None:
    """Parse command line arguments and launch the widget."""

    parser = argparse.ArgumentParser(
        description="Desktop stock ticker widget"
    )

    parser.add_argument(
        "ticker",
        help="Ticker symbol (e.g. AAPL, NVDA, SAP.DE)",
    )

    args = parser.parse_args()

    widget = StockWidget(args.ticker)
    widget.run()


if __name__ == "__main__":
    main()