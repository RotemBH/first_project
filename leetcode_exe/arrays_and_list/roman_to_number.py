"""
turn roman number to integer
"""

class Solution:
    def romanToInt(self, s: str) -> int:
        roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900}
        roman_number = 0
        _index = 0
        while _index < len(s):
            if _index+1 < len(s) and s[_index:_index+2] in roman:
                roman_number+= roman[s[_index:_index+2]]
                _index+=2
            else:
                roman_number+= roman[s[_index]]
                _index+=1
        return roman_number

test = Solution()

assert test.romanToInt('III') == 3
assert test.romanToInt('IV') == 4
assert test.romanToInt('IX') == 9
assert test.romanToInt('LVIII') == 58
assert test.romanToInt('MCMXCIV') == 1994