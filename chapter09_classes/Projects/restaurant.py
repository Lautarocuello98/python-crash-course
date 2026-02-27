class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name.title()
        self.cuisine_type = cuisine_type
        self.customer_count = 0

    def describe_restaurant(self):
        print(f"The restaurant {self.restaurant_name} is a {self.cuisine_type}")
    
    def open_restaurant(self):
        print(f"The restaurant {self.restaurant_name} is open")

    def set_number_served(self, customer):
        self.customer_count = customer

    def increment_number_served(self, number):
        self.customer_count += number

restaurants = []

while True:
    name = input("Tell me the name: ").strip()
    cuisine = input("Tell me the cuisine type: ").strip()

    if not name or not cuisine:
        print("Invalid input.")
        continue

    count_customer = int(input("How many customers served? ").strip())

    restaurant = Restaurant(name, cuisine)
    restaurant.set_number_served(count_customer)

    more_customer = input("Do you want to add more customers? (yes/no) ").strip().lower()
    if more_customer == 'yes':
        count_customer_more = int(input("How much more customers served? ").strip())
        restaurant.increment_number_served(count_customer_more)
    
    restaurants.append(restaurant)

    continue_ = input("You want to add other? (yes/no)\n").lower()
    if continue_ == 'no':
        break

print()

for restaurant in restaurants:
    restaurant.describe_restaurant()
    print(f"Customers served: {restaurant.customer_count}")

print()

for restaurant in restaurants:
    restaurant.open_restaurant()

print()