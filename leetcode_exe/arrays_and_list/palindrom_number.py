"""Given an integer x, return true if x is palindrome integer."""

class Solution:
    def isPalindrome(self, x: int) -> bool:
        str_x = str(x)
        if len(str_x) < 2:
            return True
        else:
            start = 0
            end = len(str_x)-1
            while start<=end:
                if str_x[start] != str_x[end]:
                    return False
                start +=1
                end-=1
        return True

test = Solution()
assert test.isPalindrome(555) == True
assert test.isPalindrome(121) == True
assert test.isPalindrome(10) == False
assert test.isPalindrome(-55) == False