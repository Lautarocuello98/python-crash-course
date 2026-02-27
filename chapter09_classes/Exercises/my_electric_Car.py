from electric_car import ElectricCar, Car

my_leaf = ElectricCar('nissan', 'leaf', 2024)
print(my_leaf.get_descriptive_name())
my_leaf.battery.describe_batery()
my_leaf.battery.get_range()

print()

my_mustang = Car('ford', 'mustang', 2024)
print(my_mustang.get_descriptive_name())
my_mustang.odometer_reading = 23
my_mustang.read_odometer()
