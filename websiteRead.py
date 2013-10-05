from urllib2 import urlopen
data = urlopen("http://www.meethue.com/api/nupnp")
#data = urlopen('https://uniservices1.uobgroup.com/secure/online_rates/gold_and_silver_prices.jsp')
web_pg = data.read()
print web_pg
