import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

books = pd.read_excel('data/reading-data.xlsx', sheet_name='books')
sessions = pd.read_excel('data/reading-data.xlsx', sheet_name='sessions')
events = pd.read_excel('data/reading-data.xlsx', sheet_name='events')

total_minutes_read = sum(
    sessions['active_time'].dropna().dt.total_seconds() / 60
)
total_hours_read = total_minutes_read / 60

total_pages_read = sum(books['page_count'].dropna())
total_words_read = sum(books['word_count'].dropna())

hours_per_day = (
    sessions[sessions['active_time'].notna()]
    .assign(day=sessions['start_datetime'].dt.date)
    .groupby('day')['active_time']
    .sum()
    .dt.total_seconds()
    .reset_index()
)

hours_per_day['active_time'] /= 3600

print(hours_per_day)
print('Hours Read:', total_hours_read)
print('Pages Read:', total_pages_read)
print('Words Read:', total_words_read)

hours_per_day.plot.bar(
    x='day', y='active_time', title='Hours of Reading per Day'
)

plt.tight_layout()
plt.show()
plt.close('all')
