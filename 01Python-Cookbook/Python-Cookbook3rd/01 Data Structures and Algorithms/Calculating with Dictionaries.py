prices = {
 'ACME': 45.23,
 'AAPL': 612.78,
 'IBM': 205.55,
 'HPQ': 37.20,
 'FB': 10.75
}
print( prices )#{'ACME': 45.23, 'AAPL': 612.78, 'IBM': 205.55, 'HPQ': 37.2, 'FB': 10.75}
min_price = min(zip(prices.values(), prices.keys()))
print( min_price )#(10.75, 'FB')
min_value = prices[min(prices, key=lambda k: prices[k])]
print( min_value )#FB
print(min(prices, key=lambda k: prices[k]))#('FB', 10.75)
# Best Choice
print(min(prices.items(), key=lambda item: item[1]))#('FB', 10.75)

prices_sorted = sorted(prices.items(),key=lambda item: item[1])
print( prices_sorted )#[('FB', 10.75), ('HPQ', 37.2), ('ACME', 45.23), ('IBM', 205.55), ('AAPL', 612.78)]

prices_sorted = sorted(prices.items(),key=lambda item: item[1],reverse=True)
print( prices_sorted )#[('AAPL', 612.78), ('IBM', 205.55), ('ACME', 45.23), ('HPQ', 37.2), ('FB', 10.75)]

prices_sorted = sorted( prices.items() )
print( prices_sorted )#[('AAPL', 612.78), ('ACME', 45.23), ('FB', 10.75), ('HPQ', 37.2), ('IBM', 205.55)]