from .models import *
import random

#Check whether song meets tempo criteria
def is_tempo_match(tempo, song):
    double_tempo = tempo * 2
    half_tempo = tempo/2
    if ((song.tempo >= (tempo - 5)) and (song.tempo <= (tempo + 5))) or ((song.tempo >= (double_tempo - 5)) and (song.tempo <= (double_tempo + 5))) or ((song.tempo >= (half_tempo - 5)) and (song.tempo <= (half_tempo + 5))):
        return True
    else:
        return False

#find combinations for blocks
def build_block(the_songs, the_duration):

    #recursively find combinations from each basepoint
    #args:
    #   candidates: list of potential candidates, in this case songs
    #   target: target number of seconds for the block
    #   index: starting index for the candidate list
    #   sum: current sum of seconds for the collected blocked
    #   currentList: list of songs currently being testing for solution-ness
    #   solution: final list of solutions
    def combinationSumProcess(candidates, target, index, sum, currentList, solution):
        #if this solution works, add to list of valid solutions
        if sum == target:
            solution.append(list(currentList))

        for i in range(index,len(candidates)):
            if (sum + candidates[i].duration > target):
                break;
            currentList.append(candidates[i])
            combinationSumProcess(candidates, target, i, sum+candidates[i].duration, currentList, solution)
            currentList.pop()

    #find all solutions
    #args:
    #   candidates: list of potential candidates, in this case songs
    #   target: target number of seconds for the block
    def combinationSum(candidates, target):
        solution=[]
        combinationSumProcess(candidates, target, 0, 0, [], solution)
        return solution

    #for single list, check if all songs are unique
    def all_unique(l):
        titles = []
        for song in l:
            if song.title in titles:
                return False
            else:
                titles.append(song.title)
        return True

    #for list of lists, check if there are no unique lists
    def no_uniques(matrix):
        for l in matrix:
            if all_unique(l):
                return False
        return True

    #fund combinations, increment desired time by 1 if initial solution set is empty
    def findCombinations(candidates, target):
        result = combinationSum(candidates, target)
        if not result or no_uniques(result):
            findCombinations(candidates, target + 1)
        else:
            return result

    combs = findCombinations(the_songs, the_duration)
    #filter out non-unique solutions
    if combs:
        x = filter(all_unique, combs)
        if x:
            return random.choice(x)
        else:
            return random.choice(combs)
