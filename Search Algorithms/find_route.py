import sys



"""Search for the shortest path to the destinantion city"""
def findroute(file, startcity, goalcity):
    check = 1
    fringe = []
    visited = []
    visitednodes = []
    fringe.append(["", startcity, int(0)])
    end = "END OF INPUT"
    while (check):
        openfile = open(file, "r")
        if (fringe == []):
            print "No route connecting."
            return []


        pickcandidate = fringe.pop(0) # select the candidate for expansion


        if pickcandidate[1] == goalcity:
            check = 0

        if pickcandidate[1] not in visited:
            visited.append(pickcandidate[1])
            visitednodes.append(pickcandidate)
            count = 0

            """Finds the adjacent cities and selects the candidate and appends it to the fringe"""
            for citynodes in openfile:
                #print citynodes
                if end in citynodes:
                    #print "No data to read"
                    break
                if pickcandidate[1] in citynodes:
                    count = count + 1
                    citynodes = citynodes.split()
                    if pickcandidate[1] == citynodes[0]:
                        citynodes[2] = int(citynodes[2]) + int(pickcandidate[2])
                        fringe.append(citynodes)
                    elif pickcandidate[1] == citynodes[1]:
                        temp = citynodes[0]
                        citynodes[0] = citynodes[1]
                        citynodes[1] = temp
                        citynodes[2] = int(citynodes[2]) + int(pickcandidate[2])
                        fringe.append(citynodes)
            if count == 0 and fringe == []:

                return []


            fringe = sortfringe(fringe)

        openfile.close()
    #print visitednodes
    return visitednodes


"""Sorting the successors in the fringe to implement Uniform cost search"""
def sortfringe(fringe):
    for successors in range(1, len(fringe)):
        key = fringe[successors][2]
        list = fringe[successors]
        i = successors - 1
        while (i >= 0 and fringe[i][2] > key):
            fringe[i + 1] = fringe[i]
            i = i - 1
        fringe[i + 1] = list
        #print fringe
        #print "sorting check"
    #print fringe
    return fringe


"""Traces the parent nodes of the candidates expanded"""
def traceroute(visitednodes, start):
    if visitednodes == []:
        print "Distance: Infinite"
        print "Route:\nNone"
        return

    visitednodes = visitednodes[::-1]
    route = []
    #print visitednodes
    if visitednodes[0][1] != start:
        return
    pick = visitednodes[0]
    #print pick[2]
    route.append(pick)
    for node in visitednodes:
        if pick[0] in node[1]:
            pick = node
            route.append(pick)
    #print "Check route", route



    print "\nDistance:", route[0][2], "km"
    print "\nRoute:"
    routecost = 0
    route = route[::-1]
    for successors in range(1, len(route)):
        print route[successors][0], "to", route[successors][1], ",", route[successors][2] - routecost, "km"
        routecost = route[successors][2]



def main(argv):
    """Reading the command line arguments"""
    file = argv[1]  # reading the file name

    try:
        fopen = open(file, "r")
    except:
       print "Invalid File Name"

    try:
        source = argv[2]  # reading the source city
    except:
       print "Invalid source"

    try:
        destination = argv[3]  # reading the destination city
    except:
        print "Invalid destination"


    """Calling the functions to find the shortest route(Uniform Cost Search)"""
    candidates = findroute(file, source, destination)

    """Trace the successors parents"""
    traceroute(candidates, destination)


if __name__== "__main__":
    main(sys.argv)



