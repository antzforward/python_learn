prices = {
 'ACME': 45.23,
 'AAPL': 612.78,
 'IBM': 205.55,
 'HPQ': 37.20,
 'FB': 10.75
}
print( prices )
min_price = min(zip(prices.values(), prices.keys()))
print( min_price )
min_value = prices[min(prices, key=lambda k: prices[k])]
print( min_value )
print(min(prices, key=lambda k: prices[k]))
# Best Choice
print(min(prices.items(), key=lambda item: item[1]))

prices_sorted = sorted(prices.items(),key=lambda item: item[1])
print( prices_sorted )

prices_sorted = sorted(prices.items(),key=lambda item: item[1],reverse=True)
print( prices_sorted )

prices_sorted = sorted( prices.items() )
print( prices_sorted )