"""
Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string.

"""

def find_longest_str(strs):
    longest = ''
    min_str = min(strs, key=len)
    for ind, ch in enumerate(min_str):
        flag = True
        for _s in strs:
            if _s[ind] != ch:
                flag = False
                break
        if flag:
            longest += ch
        else:
            break
    return longest


assert find_longest_str(["cir","car"])=='c'
assert find_longest_str(["flower","flow","flight"])=='fl'
assert find_longest_str(["dog","racecar","car"])==''
