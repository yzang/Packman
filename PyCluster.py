# -*- coding: utf-8 -*-
__author__ = 'zym'

class Cluster():
    def __init__(self,id=0):
        self.id=id
        self.points=[]
        self.size=0
        self.center=None
        self.distance=0

class DirectorCluster(Cluster):
    def __init__(self,id=0):
        self.id=id
        self.points=[]
        self.gender=''
        self.birth=[]
        self.stkid=[]


def manhattanDistance(point_a, point_b):
    (x1,y1) = point_a
    (x2,y2) = point_b
    return abs(x1-x2)+abs(y1-y2)

def euclideanDistance(point_a, point_b):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    (x1,y1) = point_a
    (x2,y2) = point_b
    return ( (x1-x2) ** 2 + (y1-y2) ** 2 ) ** 0.5

def dbscan(data,eps,function=manhattanDistance,min_pts=1):
    cluster_id=0
    visited={}
    clusters=[]
    for point in data:
        #for each unvisited points in dataset
        if point not in visited:
            visited[point]=True
            neighbors=get_neighbors(point,data,eps,clusters,function)
            if len(neighbors)<=min_pts:
                cluster_id+=1
                c=Cluster(cluster_id)
                c.points.append(point)
                clusters.append(c)
            else:
                cluster_id+=1
                c=Cluster(cluster_id)
                clusters.append(c)
                expand_cluster(point,data,neighbors,visited,c,clusters,eps,function)
    return clusters

def expand_cluster(point,data,neighbors,visited,c,clusters,eps,function):
    c.points.append(point)
    for neighbor_point in neighbors:
        if neighbor_point not in visited:
            visited[neighbor_point]=True
            new_neighbors=get_neighbors(neighbor_point,data,eps,clusters,function)
            join_neighbors(neighbors,new_neighbors)
        if not find_in_cluster(neighbor_point,clusters):
            c.points.append(neighbor_point)


def join_neighbors(n1,n2):
    for point in n2:
        if point not in n1:
            n1.append(point)


def find_in_cluster(point,clusters):
    for cluster in clusters:
        if point in cluster.points:
            return True
    return False

def get_neighbors(point_a,data,eps,clusters,function):
    """
    neighbors=[point1,point2,point3...]
    """
    neighbors=[point_a]
    for point_b in data:
        if point_a!=point_b and not find_in_cluster(point_b,clusters):
            distance=function(point_a,point_b)
            if distance<=eps:
                neighbors.append(point_b)
    return neighbors

def compute_director_cluster(cluster):
    points=cluster.points
    gender_dict={}
    for point in points:
        birth=point[3]
        stkid=point[4]
        gender=point[2]
        gender_dict[gender]=gender_dict.get(gender,0)+1
        if birth not in cluster.birth:
            cluster.birth.append(birth)
        if stkid not in cluster.stkid:
            cluster.stkid.append(stkid)
    cluster.gender=get_modes(gender_dict)

def computer_data_cluster(cluster,point=None):
    cluster.size=len(cluster.points)
    for i in range(cluster.size):
        for j in range(i+1,cluster.size):
            cluster.distance+=manhattanDistance(cluster.points[i],cluster.points[j])


def get_modes(dict):
    max_key=max(dict,key=dict.get)
    return max_key

def scan_other_points(data,clusters):
    visited={}
    if len(clusters)>0:
        cluster_id=clusters[len(clusters)-1].id
    else:
        cluster_id=0
    for point in data:
        gender=point[2]
        stkid=point[4]
        for cluster in clusters:
            if (gender==cluster.gender or gender==None or gender=="") and stkid in cluster.stkid:
                cluster.points.append(point)
                visited[point[0]]=True
                break
        if point[0] not in visited:
            visited[point[0]]=True
            cluster_id+=1
            c=Cluster(cluster_id)
            c.points.append(point)
            compute_director_cluster(c)
            clusters.append(c)

def scan_similar_names(data,eps=0.6):
    '''
    data=[(id,cv,gender,birth,stkid,catagory),()...]
    '''
    data_with_cv=[]
    data_without_cv=[]
    for d in data:
        if d[1] is None or len(d[1])<4:
            data_without_cv.append(d)
        else:
            data_with_cv.append(d)
    clusters=dbscan(data_with_cv,eps)
    for cluster in clusters:
        compute_director_cluster(cluster)
    scan_other_points(data_without_cv,clusters)
    return clusters

