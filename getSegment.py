import numpy as np
from getProjOnSegment import get_proj_on_segment

def get_segment(pss, p, dMax):
   flag = 0
   i = 0
   j = 0
   d = np.inf

   for i0 in range(len(pss)):
       ps = pss[i0].ps
       n = ps.shape[0]

       d = np.inf
       for j0 in range(n-1):
           pt, t, dj = get_proj_on_segment(ps[j0, :], ps[j0+1, :], p)

           if dj < d and dj < dMax and 0 < t and t < 1:
               flag = 1
               i = i0
               j = j0

   return flag, i, j