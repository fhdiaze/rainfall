import sys
from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp
from rainfall.core.Vineyard import Vineyard

# Uncomment the next two lines if you want to use a file as standard input
in_path = "C:/Users/kuby/Downloads/icpc2019data/F-directingrainfall/sample-3.in"
sys.stdin = open(in_path, "r")

l, r, n = tuple([int(n) for n in input().split(" ")])

tarps = []

for i in range(n):
    tx, ty, hx, hy = tuple([int(i) for i in input().split(" ")])
    tarps.append(Tarp(Point(tx, ty), Point(hx, hy)))

vineyard = Vineyard(l, r, tarps)
vineyard.plot()
print(vineyard.memo_punctures())
