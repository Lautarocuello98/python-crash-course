my_favorite_food = ['pizza', 'falafel', 'carrot cake']
my_friend_favorite_food = my_favorite_food[:]

my_favorite_food.append('cannoli')
my_friend_favorite_food.append('ice cream')

print(f"My favorite foods are:")
for food in my_favorite_food:
    print(food)

print(f"\nMy friend's favorite foods are:")
for food in my_friend_favorite_food:
    print(food)




