#/usr/bin/python
#coding:utf8

import numpy as np
def Cosine(x, y):
  return 1.0*np.dot(x, y)/np.sqrt(np.dot(x,x))/np.sqrt(np.dot(y,y))
if __name__ == '__main__':
  print Cosine(np.array([-1,-2]), np.array([1,2]))
