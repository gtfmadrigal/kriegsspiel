def throwError(function):
    if function == "arguments": errorMessage = "Too many arguments for command. Type 'man' [command] for information."
    elif function == "bad": errorMessage = "Bad command. Type 'help' for assistance."
    elif function == "os": errorMessage = "Unknown operating system."
    elif function == "team": errorMessage = "That unit does not belong to you, or it does not exist."
    elif function == "available": errorMessage = "That unit is currently unavailable."
    elif function == "function": errorMessage = "That function is unavailable to this unit."
    elif function == "heading": errorMessage = "Unit cannot exceed its maximum heading change."
    elif function == "dead": errorMessage = "Unit is dead."
    print(errorMessage)