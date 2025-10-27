s = "%u7EB3%u6307ETF"
s = s.replace("%", "\\")
print(s.encode("utf-8").decode("unicode_escape"))

from urllib.parse import quote

print(quote("浙"))
print('江'.encode('ascii'))
