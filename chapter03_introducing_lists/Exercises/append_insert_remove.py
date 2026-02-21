motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles)

motorcycles.append('ducati')
print(motorcycles)

motorcycles.insert(0, 'zanela')
print(motorcycles)

del motorcycles[1]
print(motorcycles)

popped_motorcycles = motorcycles.pop(2)

print(popped_motorcycles)

motorcycles.remove('ducati')
print(motorcycles)

