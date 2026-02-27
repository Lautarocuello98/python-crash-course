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
        if customer < 0:
            raise ValueError("Customer count cannot be negative.")
        self.customer_count = customer

    def increment_number_served(self, number):
        if number < 0:
            raise ValueError("Cannot increment by negative number.")
        self.customer_count += number

    # 🔹 Método común para mostrar info
    def show_details(self):
        self.describe_restaurant()
        print(f"Customers served: {self.customer_count}")
        self.open_restaurant()


class IceCreamStand(Restaurant):
    def __init__(self, restaurant_name):
        super().__init__(restaurant_name, "Ice Cream place")
        self.flavors = []

    def show_flavors(self):
        print("Flavors available:")
        for flavor in self.flavors:
            print(f"- {flavor}")

    # 🔹 Sobrescribimos comportamiento
    def show_details(self):
        self.describe_restaurant()
        print(f"Customers served: {self.customer_count}")
        self.show_flavors()
        self.open_restaurant()


restaurants = []

while True:
    type_place = input("Is this an ice cream stand? (yes/no): ").strip().lower()
    name = input("Tell me the name: ").strip()

    if type_place == "yes":
        restaurant = IceCreamStand(name)
        flavors_input = input("Enter flavors separated by commas: ")
        restaurant.flavors = [f.strip().title() for f in flavors_input.split(",")]

    else:
        cuisine = input("Tell me the cuisine type: ").strip()
        if not cuisine:
            print("Invalid input.")
            continue
        restaurant = Restaurant(name, cuisine)

    count_customer = int(input("How many customers served? ").strip())
    restaurant.set_number_served(count_customer)

    more_customer = input("Do you want to add more customers? (yes/no) ").strip().lower()
    if more_customer == "yes":
        count_customer_more = int(input("How much more customers served? ").strip())
        restaurant.increment_number_served(count_customer_more)

    restaurants.append(restaurant)

    continue_ = input("You want to add other? (yes/no)\n").lower()
    if continue_ == "no":
        break


print("\n--- SUMMARY ---\n")

for restaurant in restaurants:
    restaurant.show_details()
    print()