# Make an empty list for storing aliens.
aliens = []

# Make 30 green aliens.
for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)

for alien in aliens[:3]:
    if alien['color'] == 'green':
        alien['color'] = 'yellow'
        alien['points'] = 10
        alien['speed'] = 'medium'
for alien in aliens[4:7]:
    if alien['color'] == 'green':
        alien['color'] = 'red'
        alien['points'] = 15
        alien['speed'] = 'fast'

# Show the first 10 aliens
for i, alien in enumerate(aliens[:10]):
    print(f"alien n{i+1} {alien}")

print('...')
