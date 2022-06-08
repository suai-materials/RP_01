with open("TASK_1_PANKOV.txt", "r", encoding="utf-8") as file:
    print("Number of lines containing \".h\" and \".cc\":")
    ''' Iterate over all lines with a list expression, checking for .cc and .h
    If our lines did not go through "if",
    then they do not participate in the final list and with "len" we do not count them
    '''
    print("Total: ",
          len([print(i + 1) for i, line in enumerate(file) if ".cc" in line and ".h" in line]))
