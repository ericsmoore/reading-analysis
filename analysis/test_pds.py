import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

books = pd.read_excel('data/reading-data.xlsx', sheet_name='books')
sessions = pd.read_excel('data/reading-data.xlsx', sheet_name='sessions')
events = pd.read_excel('data/reading-data.xlsx', sheet_name='events')

books = books.merge(
    sessions.groupby('book_id')['active_time'].sum(), how='left', on='book_id'
)

start = sessions['start_datetime'].min().floor('D') - pd.offsets.MonthBegin()
end = sessions['start_datetime'].max().floor('D') + pd.offsets.MonthEnd(0)

hours_per_day = (
    sessions[sessions['active_time'].notna()]
    .assign(day=sessions['start_datetime'].dt.floor('D'))
    .groupby('day')['active_time']
    .sum()
    .dt.total_seconds()
    .div(3600)
    .reindex(pd.date_range(start, end, freq='D'), fill_value=0)
)

ax = hours_per_day.plot(
    title='Hours of Reading per Day',
    legend=False,
    yticks=[0, 1, 2],
    ylim=(0, 2.5),
)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.SU))
ax.grid(axis='x', which='major', linestyle='--', alpha=0.3)
plt.tight_layout()

plt.savefig('outputs/fig.png')

num_books = len(books)
total_seconds = sum(sessions['active_time'].dropna().dt.total_seconds())
total_hours = total_seconds / 3600
total_pages = sum(books['page_count'].dropna())
total_words = sum(books['word_count'].dropna())

print('Books Read:', num_books)
print('Hours Read:', round(total_hours, 2))
print('Pages Read:', total_pages)
print('Words Read:', total_words)
