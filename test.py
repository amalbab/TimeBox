class Solution(object):
    def longestConsecutive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        sequences = [[nums[0],nums[0], 1]]
        for i in range(1, len(nums)):
            print(sequences)
            num = nums[i]
            index = -1
            found = False
            for j in range(len(sequences)):
                s = sequences[j]
                if num == s[0]-1:
                    if index != -1:
                        s[0] = sequences[index][0]
                        s[2] = s[2] + sequences[index][2]
                        sequences.pop(index)
                        break
                    else:
                        s[0] = num
                        s[2]+=1
                        index = j
                        found = True
                elif num == s[1] + 1:
                    if index != -1:
                        s[1] = sequences[index][1]
                        s[2] = s[2] + sequences[index][2]
                        sequences.pop(index)
                        break
                    else:
                        s[1] = num
                        s[2]+=1
                        index = j
                        found = True
                elif s[0] < num < s[1]:
                    s[2]+=1
                    found = True
            if not found:
                sequences.append([num, num, 1])

            
        max_s = 0
        for s in sequences:
            if s[2] > max_s:
                max_s = s[2]
        return max_s
            
if __name__ == "__main__":
    nums = [0,3,7,2,5,8,4,6,0,1]
    sol = Solution()
    print(sol.longestConsecutive(nums))