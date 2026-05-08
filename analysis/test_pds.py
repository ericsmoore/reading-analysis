import pandas as pd
import matplotlib.pyplot as plt

books = pd.read_excel('data/reading-data.xlsx', sheet_name = 'books')
sessions = pd.read_excel('data/reading-data.xlsx', sheet_name = 'sessions')
events = pd.read_excel('data/reading-data.xlsx', sheet_name = 'events')

total_minutes_read = sum(sessions['active_time'].dropna().dt.total_seconds() / 60)
total_hours_read = total_minutes_read / 60

print('Hours Read:', total_hours_read)
