def album_info(artist_name, album, number_of_songs=None):
    info = {
        'artist': artist_name,
        'album': album
    }
    if number_of_songs is not None:
        info['number_of_songs'] = number_of_songs
    return info


record = []

while True:
    print("\nTell me albums:")
    print("Press 'q' to quit")

    input_artist = input("What artist? ").strip()
    if input_artist.lower() == 'q':
        break

    input_album = input("What album? ").strip()
    if input_album.lower() == 'q':
        break

    have_number = input("Do you know how many songs? (yes/no) ").strip().lower()
    if have_number == 'q':
        break

    if have_number == 'yes':
        number_input = input("How many? ").strip()
        if number_input.lower() == 'q':
            break

        if number_input.isdigit():
            record.append(
                album_info(input_artist.title(), input_album.title(), int(number_input))
            )
        else:
            print("Invalid number. Saved without song count.")
            record.append(
                album_info(input_artist.title(), input_album.title())
            )

    elif have_number == 'no':
        record.append(
            album_info(input_artist.title(), input_album.title())
        )

    else:
        print("Please answer 'yes' or 'no'.")


print("\nAlbums entered:")
for item in record:
    songs = item.get('number_of_songs', 'Unknown')
    print(f"{item['artist']}, {item['album']}, songs: {songs}")