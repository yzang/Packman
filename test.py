#encoding=utf-8
__author__ = 'zym'

import util

a=set()
a.add((1,2))
a.add((3,4))
b=set()
b.add((1,5))
b.add((2,5))
b.add((3,5))
c=[]
c.append(a)
c.append(b)
print len(max(c,key=len))
