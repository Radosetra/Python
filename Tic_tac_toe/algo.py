def isWinner(playerValue,solutionList):
    for sol in solutionList :
        sol = sol.lower()
        spiltedList = [ elem for elem in sol]
        flag = True
        for elem in spiltedList:
            if (elem not in playerValue):
                flag = False
                break
        if flag:
            return flag

    return False

    # for sol in solutionList:
    #     sol = sol.lower()
    #     if all(elem in playerValue for elem in sol):
    #         # print("La solution", sol, "est présente dans playerValue")
    #         return True
    # # print("Aucune solution n'est présente dans playerValue")
    # return False

solutions = [
    "ADG",
    "BEH",
    "CFI",
    "GHI",
    "DEF",
    "ABC",
    "AEI",
    "GEC"
]

player1 = "abi"
val = isWinner(player1, solutions)
    
        
print(val)