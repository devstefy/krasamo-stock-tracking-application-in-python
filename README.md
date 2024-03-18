# 👋 KRASAMO STOCK TRACKING APPLICATION IN PYTHON
![MIT](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.10.11-blue) ![VSC](https://img.shields.io/badge/IDE-Visual_Studio_Code-blue) ![2024](https://img.shields.io/badge/date-march_2024-blue) ![@devstefy](https://img.shields.io/badge/autor-@devstefy-purple)
![Stock Tracking Wallpaper](https://img.freepik.com/free-photo/cardano-blockchain-platform-collage_23-2150827491.jpg)

## 📙Description
This application allows you to track stocks you are interested in, providing information such as the current price, the daily minimum and maximum, and the listing status.

**Thank you for using the Stock Tracking Application!**

## 📊APIs 
[Finance API Alpha Vantage](https://www.alphavantage.co/)

## 📚Libraries
- [Requests](https://pypi.org/project/requests/)
- [Pandas](https://pandas.pydata.org/)
- [IO](https://docs.python.org/3/library/io.html)
- [Datetime](https://docs.python.org/3/library/datetime.html)
- [Streamlit](https://streamlit.io/)
- [Streamlit Option Menu](https://discuss.streamlit.io/t/streamlit-option-menu-is-a-simple-streamlit-component-that-allows-users-to-select-a-single-item-from-a-list-of-options-in-a-menu/20514)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html)

### 🐍Pip install
```powershell
    pip install requests
    pip install pandas
    pip install streamlit
    pip install streamlit-option-menu
    pip install sqlite2
```

## Features

- `Get global quote data`: Look up the current price, daily minimum and maximum for a specific stock.
- `View listing status`: Check if a stock is active, inactive, or delisted.
- `Read data from database`: Access information stored in the local database.
- `Update database`: Save global quote information to the local database.

## Documentation
You can check the docstring of each .py file or you can open the .html files in the browser ([Pydoc](https://docs.python.org/3/library/pydoc.html)).

## Running
Navigate to the application directory and execute the following command:
```powershell
    python -m streamlit run main.py
```

## Limitations
1. It is not possible to query the global quotes of all symbols because it involves an API request for each symbol. We tried to use the [BATCH_STOCK_QUOTES](https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&apikey=VJ856XHXT0I8GR7N&symbols=MSFT,AAPL,FB) endpoint but it is not available.
2. API limits requests to 25 per day. API limits requests to 25 per day. Therefore, if the limit is exceeded then we will proceed to only use the database.

## License

Krasamo Stock Tracking Application in Python is [MIT Licenses](https://github.com/devstefy/krasamo-stock-tracking-application-in-python/blob/devstefy/LICENSE).

## Contact

For any questions or comments, you can contact me through [GitHub](https://github.com/devstefy) or by email(p.stefani16@gmail.com).


