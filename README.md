## Chart Generator

A Python Tkinter-based GUI app that allows users to analyze business CSV files with date filtering, theme customization, and summary + chart generation.

## Features

- Upload business-related CSV files
- Optional date range filtering using calendar pickers
- Light/Dark/Default themes with dynamic preview
- Auto-generated summary with revenue, quantity, top items, and category breakdown
- Visual histogram chart embedded via matplotlib
- Manual PDF report saved with timestamp

## Requirements

- Python 3.x
- pandas
- matplotlib
- tkcalendar

## Run the App

```bash
pip install pandas matplotlib tkcalendar
python chart generator.py
```

## Notes

- The app auto-detects date and revenue columns.
- Report is saved in the same folder as the uploaded file.
