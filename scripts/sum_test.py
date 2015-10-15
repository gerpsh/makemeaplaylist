from playlist.models import *

import sys

def run():

    def is_tempo_match(tempo, song):
        double_tempo = tempo * 2
        half_tempo = tempo/2
        if ((song.tempo >= (tempo - 5)) and (song.tempo <= (tempo + 5))) or ((song.tempo >= (double_tempo - 5)) and (song.tempo <= (double_tempo + 5))) or ((song.tempo >= (half_tempo - 5)) and (song.tempo <= (half_tempo + 5))):
            return True
        else:
            return False

    def return_block(the_songs, the_duration):

        def combinationSumRec(candidates, target, index, sum, listT, solution):
            if sum == target:
                solution.append(list(listT))
            for i in range(index,len(candidates)):
                if (sum + candidates[i].duration > target):
                    break;
                listT.append(candidates[i])
                combinationSumRec(candidates, target, i, sum+candidates[i].duration, listT, solution)
                listT.pop()

        def combinationSum(candidates, target):
            solution=[]
            combinationSumRec(candidates, target, 0, 0, [], solution)
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

        #for list of lists
        def no_uniques(matrix):
            for l in matrix:
                if all_unique(l):
                    return False
            return True

        def findCombinations(candidates, target):
            result = combinationSum(candidates, target)
            if not result or no_uniques(result):
                findCombinations(candidates, target + 1)
            else:
                return result

        combs = findCombinations(cands, the_duration)
        if combs:
            x = filter(all_unique, findCombinations(cands, the_duration))
            if x:
                return x[0]
            else:
                return combs[0]

    cands = Song.objects.filter(energy__range=(0.90, 1.0))
    duration = 600
    tempo = 90
    cands = [song for song in cands if is_tempo_match(tempo, song)]
    x = return_block(cands, duration)
    print(x)
