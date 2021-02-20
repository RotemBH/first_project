"""Given an array of integers nums and an integer target,
return indices of the two numbers such that they add up to target."""


class Solution:
    """
    explanation: loop over the array, check if the value in some cache (seen). if it is- we saw it diff from target
    so return the value in the cache -it is the diff index, else continue searching
    if no two values is added to target, return empty list.
    """
    def twoSum(self, nums: list, target: int) -> list:
        seen = {}
        for index, value in enumerate(nums):
            print(index, value)
            if value in seen:
                return [seen[value], index]
            else:
                seen[target - value] = index
        return []


test = Solution()
ans = test.twoSum([2, 6, 8, 4, 1], 3)
print(ans)
