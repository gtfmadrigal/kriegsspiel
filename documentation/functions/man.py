def man(argument):
    manpage = str(argument)
    if os.name == "nt": path = "manpages\\" + manpage
    elif os.name == "posix": path = "manpages/" + manpage
    else: 
        print("Unknown operating system.")
        return
    file = open(path, "r")
    for line in file:
        print(file.read())