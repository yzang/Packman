#encoding=utf-8
__author__ = 'zym'
def getWeightFromMST(graph,count):
    total_weight=0
    forests=[]
    if count<=1:
        return 0
    while True:
        component=graph.pop()
        v1,v2,weight=component
        find_connection=False
        find_tree=False
        build_tree=True
        for i in xrange(len(forests)):
            tree=forests[i]
            if v1 in tree and v2 in tree:
                build_tree=False
                break
            elif v1 in tree or v2 in tree:
                find_tree=True
                tree.add(v1)
                tree.add(v2)
                total_weight+=weight
                for j in xrange(i+1,len(forests)):
                    second_tree=forests[j]
                    if v1 in second_tree or v2 in second_tree:
                        find_connection=True
                        for vertex in second_tree:
                            tree.add(vertex)
                        forests.pop(j)
                        break
                if find_connection:
                    break
        if not find_tree and build_tree:
            tree=set()
            tree.add(v1)
            tree.add(v2)
            total_weight+=weight
            forests.append(tree)
        if len(max(forests,key=len))==count:
            break
    return total_weight