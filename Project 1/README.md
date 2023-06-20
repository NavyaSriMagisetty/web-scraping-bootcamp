# Portfolio Valuation With Google Finance 

## Code Implementation
Step 1: Import requests, BeautifulSoup in order to process the URL and get the required data from it.  
Step 2: Import dataclass which is used to store specifically the data values, and import tabulate for a tabular view of the final output.  
Step 3: Create three dataclasses, one for `Stock`, `Position`, `Portfolio`.  
        * `Stock`: Attributes - ticker, exchange, price, currency, USD price and Methods - `__post_init__`:: calls `get_stock_information` function using ticker and exchange as arguments.  
        * `Position`: Attributes - stock, quantity  
        * `Portfolio`: Attributes - positions and Methods - `get_total_value` - sums up each position quantity and stock price in USD.  
Step 4: Initialize a list of stocks and each is of type stock dataclass.  
Step 5: Stock will intern calls `get_stock_information` function. This function will get the respective stock information such as price and currency. If a currency is not in USD, it will intern call `get_fx_to_usd` which gives the currency in USD. Finally returns a dictionary of ticker, exchange, price, currency, and usd_price.  
Step 6: `get_fx_to_usd` function is used to get the exchange rate of a given currency code in USD and returns it.  
Step 7: Each returned stock will be zipped with quantity and converted to a Position dataclass object and stored in positions.  
Step 8: A list of positions is sent to Portfolio which has a `get_total_value` function to calculate the total_value of all stocks and return the total value.  
Step 9: Finally `display_portfolio_summary` function is used to display the final data in the form of a table using portfolio.  

