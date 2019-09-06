from rainfall.core.Point import Point
from rainfall.core.Tarp import Tarp
from rainfall.core.Vineyard import Vineyard

l, r, n = tuple([int(n) for n in input().split(" ")])

tarps = []

for i in range(n):
    tx, ty, hx, hy = tuple([int(i) for i in input().split(" ")])
    tarps.append(Tarp(Point(tx, ty), Point(hx, hy)))

vineyard = Vineyard(l, r, tarps)
vineyard.plot()

print(vineyard)
print(vineyard.tarps_box())
print(vineyard.min_punctures())
print(vineyard.punctures(18, 40))
print(vineyard.punctures(11, 30))
print(vineyard.punctures(15, 30))
