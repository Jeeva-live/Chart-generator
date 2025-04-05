import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from datetime import datetime

class DataAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chart Generator")
        self.root.geometry("1000x600")

        self.theme = "Default"  # Initial theme
        self.build_ui()
        self.apply_theme()

    def build_ui(self):
        # Header frame
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.header_frame, text="Chart Genrator", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # Theme switch
        theme_frame = tk.Frame(self.root)
        theme_frame.pack(pady=5, anchor='ne', padx=10)
        tk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=2)
        self.theme_var = tk.StringVar(value=self.theme)
        theme_menu = tk.OptionMenu(theme_frame, self.theme_var, "Default", "Dark", "Light", command=self.change_theme)
        theme_menu.pack(side=tk.LEFT)

        # File selection
        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(pady=10)

        self.file_label = tk.Label(self.file_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=10)

        browse_button = tk.Button(self.file_frame, text="Browse", command=self.load_file)
        browse_button.pack(side=tk.RIGHT, padx=10)

        # Date filter
        self.date_frame = tk.Frame(self.root)
        self.date_frame.pack(pady=10)

        tk.Label(self.date_frame, text="Start Date (Optional):").pack(side=tk.LEFT, padx=5)
        self.start_date = DateEntry(self.date_frame, date_pattern="dd-mm-yyyy")
        self.start_date.pack(side=tk.LEFT, padx=5)

        tk.Label(self.date_frame, text="End Date (Optional):").pack(side=tk.LEFT, padx=5)
        self.end_date = DateEntry(self.date_frame, date_pattern="dd-mm-yyyy")
        self.end_date.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(self.date_frame, text="Clear Dates", command=self.clear_dates)
        clear_button.pack(side=tk.LEFT, padx=10)

        # Analyze button
        analyze_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        analyze_button.pack(pady=10)

        # Report preview area
        self.preview_frame = tk.Frame(self.root)
        self.preview_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = None  # Placeholder for matplotlib chart

    def apply_theme(self):
        themes = {
            "Default": {"bg": "#cfe2f3", "fg": "#000", "gradient": ["#cfe2f3", "#888"]},
            "Dark": {"bg": "#1c1c3c", "fg": "#fff", "gradient": ["#1c1c3c", "#4b0082"]},
            "Light": {"bg": "#e0f7fa", "fg": "#000", "gradient": ["#87ceeb", "#dda0dd"]}
        }

        selected = themes[self.theme_var.get()]
        bg = selected["bg"]
        fg = selected["fg"]

        widgets = [
            self.root, self.header_frame, self.file_frame, self.date_frame,
            self.preview_frame, self.title_label, self.file_label
        ]
        for widget in widgets:
            widget.configure(bg=bg)

        for frame in [self.header_frame, self.file_frame, self.date_frame]:
            for child in frame.winfo_children():
                try:
                    child.configure(bg=bg, fg=fg)
                except:
                    pass

    def change_theme(self, value):
        self.theme = value
        self.apply_theme()

    def clear_dates(self):
        self.start_date.set_date(datetime.strptime("01-01-2000", "%d-%m-%Y"))
        self.end_date.set_date(datetime.today())

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[["CSV Files", "*.csv"]])
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.df = pd.read_csv(file_path)
            messagebox.showinfo("Success", "File loaded successfully!")

    def generate_report(self):
        if not hasattr(self, 'df'):
            messagebox.showerror("Error", "Please load a CSV file first.")
            return

        df_copy = self.df.copy()
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()

        date_columns = [col for col in df_copy.columns if 'date' in col.lower()]
        if date_columns:
            df_copy[date_columns[0]] = pd.to_datetime(df_copy[date_columns[0]], errors='coerce')
            df_copy.dropna(subset=[date_columns[0]], inplace=True)

            default_start = datetime.strptime("01-01-2000", "%d-%m-%Y").date()
            default_end = datetime.today().date()

            if start_date != default_start or end_date != default_end:
                df_copy = df_copy[(df_copy[date_columns[0]].dt.date >= start_date) &
                                  (df_copy[date_columns[0]].dt.date <= end_date)]

        # Generate chart
        fig, ax = plt.subplots(figsize=(6, 4))
        df_copy.iloc[:, -1].hist(bins=10, color='skyblue', edgecolor='black', ax=ax)
        ax.set_title("Data Distribution")
        ax.set_xlabel("Values")
        ax.set_ylabel("Frequency")

        # Generate summary
        summary_text = f"📊 Summary Report\n\n"
        summary_text += f"🧾 Total Orders: {len(df_copy)}\n"

        revenue_col = [col for col in df_copy.columns if 'revenue' in col.lower() or 'total' in col.lower()]
        quantity_col = [col for col in df_copy.columns if 'quantity' in col.lower() or 'order' in col.lower()]
        item_col = [col for col in df_copy.columns if 'item' in col.lower() or 'product' in col.lower()]
        category_col = [col for col in df_copy.columns if 'category' in col.lower()]

        if revenue_col:
            total_revenue = df_copy[revenue_col[0]].sum()
            summary_text += f"💰 Total Revenue: ₹{total_revenue:,.2f}\n"

        if quantity_col:
            total_qty = df_copy[quantity_col[0]].sum()
            summary_text += f"📦 Total Quantity Sold: {total_qty}\n"

        if item_col:
            top_items = df_copy[item_col[0]].value_counts().head(3)
            summary_text += "\n🏆 Top Items:\n"
            summary_text += "\n".join([f"{idx}: {val} orders" for idx, val in top_items.items()]) + "\n"

        if category_col:
            category_summary = df_copy[category_col[0]].value_counts()
            summary_text += "\n🧩 Category-wise Summary:\n"
            summary_text += "\n".join([f"{cat}: {count} orders" for cat, count in category_summary.items()])

        # Clear previous canvas and widgets
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        # Display chart
        self.canvas = FigureCanvasTkAgg(fig, master=self.preview_frame)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

        # Display summary
        summary_label = tk.Label(self.preview_frame, text=summary_text, font=("Arial", 12), justify="left", anchor="w", bg=self.root["bg"])
        summary_label.pack(pady=10, fill=tk.BOTH)

        # Save report
        report_folder = os.path.dirname(self.file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(report_folder, f"Report_{timestamp}.pdf")
        fig.savefig(report_path)
        messagebox.showinfo("Report Saved", f"Report automatically saved as:\n{report_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalyzerApp(root)
    root.mainloop()
