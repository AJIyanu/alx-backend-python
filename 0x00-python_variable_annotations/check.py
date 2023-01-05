#!/usr/bin/env python3
concat = __import__('1-concat').concat

str1 = "egg"
str2 = 56

print(concat(str1, str2) == "{}{}".format(str1, str2))
print(concat.__annotations__)
