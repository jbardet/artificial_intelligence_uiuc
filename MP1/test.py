#print("Le node qu'on remove")
    #print(node[0].I)
    node.remove(node[0])
    move_f = Frontier[0]
    #print("Frontier")
    #print(Frontier)
    #print("Frontier[0]")
    #print(move_f)
    move_n = node[0]
    #print("Node[0]")
    #print(move_n.I)
    initialize = node[0].f
    #print("f de Node[0]")
    #print(initialize)
    for i in node :
        if i.f < initialize :
            #print("Reordrer")
            Frontier[Frontier.index(i.I)] = move_f
            Frontier[0] = i.I
            node[node.index(i)] = move_n
            node[0] = i
            initialize = i.f
            move_f = Frontier[0]
            move_n = node[0]
            initialize = node[0].f
            #print("Nouveau Node[0], Frontier[0], f")
            #print(node[0].I)
            #print(Frontier[0])
            #print(initialize)
    for i in node :
        if i.f == initialize :
            if i.g > node[0].g :
                #print("Reordrer")
                Frontier[Frontier.index(i.I)] = move_f
                Frontier[0] = i.I
                node[node.index(i)] = move_n
                node[0] = i
                initialize = i.f
                move_f = Frontier[0]
                move_n = node[0]
                initialize = node[0].f
                #print("Nouveau Node[0], Frontier[0], f")
                #print(node[0])
                #print(Frontier[0])
                #print(initialize)
    parent_node = node[0]
    g = parent_node.g + 1
    #print("Frontier avant modif")
    #print(Frontier)
    for k in node :
        if Frontier[0] in k.O :
            if k.I == Frontier[0] :
                k.O.remove(Frontier[0])
                print("FIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIND")
                print(k.O)
                print(len(k.O))
                print(k.f)
                print(k.I)
                if len(k.O) == 0 :
                    print("BREAK")
                    break
    Neig = maze.getNeighbors(Frontier[0][0], Frontier[0][1])
    #print("Frontier pour prendre les NEIG")
    #print(Frontier)
    #print("Neig")
    #print(Neig)
    #print(node[0].f)
    #print(node[0].I)
    for j in Neig :
        distance = float("inf")
        #print(Frontier)
        if (j not in Frontier) & (j not in Explored) :
            #print("J'appende à FRONTIER")
            #print(j)
            Frontier.append(j)
            node.append(Node(j, parent_node))
            Explored.append(node[-1])
            node[-1].O = parent_node.O
            for i in node[-1].O :
                heuristic = (abs(j[0] - i[0]) + abs(j[1] - i[1]))
                if heuristic < distance :
                    distance = heuristic
            node[-1].g = g
            node[-1].f = g + distance + (len(node[-1].O)-1)*(maze.getDimensions()[0]-4)
            #print("New point")
            #print(node[-1].I)
            #print(node[-1].g)
            #print(node[-1].f)
        else :
            for i in node :
                if i.I == j :
                    for k in i.O :
                        heuristic = (abs(j[0] - k[0]) + abs(j[1] - k[1]))
                        if heuristic < distance :
                            distance = heuristic
                    i.g = g
                    i.f = g + distance + (len(i.O)-1)*(maze.getDimensions()[0]-4)
                    #print("modifier point, son f")
                    #print(i.I)
                    #print(i.f)
    #print("Je supprime")
    #print(Frontier[0])
    Frontier.remove(Frontier[0])


"""
for i in MST :
    if len(visited_node) > 0 :
        print(i)
        for j in visited_node :
            if i[1] not in j[0] :
                cost = cost + i[0]
                if i[2] in j[0] :
                    print("change visitor")
                    j[0] = i[2]
                elif i[2] in j[1] :
                    print("change visitor")
                    j[1] = i[2]
                else :
                    print("add visitor1")
                    visited_node.append([i[1], i[2]])
                    break
            elif i[2] not in j[1] :
                cost = cost + i[0]
                if i[1] not in j[0] :
                    cost = cost + i[0]
                    if i[2] in j[0] :
                        print("change visitor")
                        j[0] = i[2]
                    elif i[2] in j[1] :
                        print("change visitor")
                        j[1] = i[2]
                    else :
                        print("add visitor2")
                        visited_node.append([i[1], i[2]])
                        break
            else :
                print("ciao")
                MST.remove(i)
    else :
        visited_node.append([i[1], i[2]])
        print("first")
print(MST)
print(cost)
print(visited_node)
"""

    """"
    the fings that doens't work

    change = False
    to_change = []
    to_who = []
    for k in node :
        print("kiko")
        print(k.I)
        print(k.O)
        for l in k.O :
            if k.I == l :
                change = True
                to_change.append(l)
                to_who.append(Node2(k.I, k.P, k.O))
    distance = float("inf")
    if change :
        print("FIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIND")
        node.append(Node2(to_who[-1].I, to_who[-1].P, to_who[-1].O))
        print(node[-1].O)
        print(l[-1])
        node[-1].O.remove(l)
        if len(node[-1].O) > 0 :
            for j in node[-1].O :
                heuristic = (abs(node[-1].I[0] - j[0]) + abs(node[-1].I[1] - j[1]))
                if heuristic < distance :
                    distance = heuristic
            node[-1].f = g + distance + (len(node[-1].O)-1)*(maze.getDimensions()[0]-4)
        else :
            print("CESTFINININININININININININIININININININN")
    """
