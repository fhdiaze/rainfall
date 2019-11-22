import sys
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp
from rainfall.core.Vineyard import Vineyard

# Uncomment the next two lines if you want to use a file as standard input
in_path = "C:/Users/kuby/Downloads/icpc2019data/F-directingrainfall/secret-10-matthias.in"
sys.stdin = open(in_path, "r")

l, r, n = tuple([int(n) for n in input().split(" ")])

tarps = []
max_x = 0

for i in range(n):
    lx, ly, hx, hy = tuple([int(i) for i in input().split(" ")])
    max_x = max(max_x, lx, hx)
    tarps.append(Tarp(Point(lx, ly), Point(hx, hy)))

vineyard = Vineyard(l, r, tarps, max_x)
print(vineyard.punctures())
