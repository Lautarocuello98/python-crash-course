from name_function import get_formatted_name

def test_first_last_name():
    formatted_name = get_formatted_name('janis', 'joplin')
    assert formatted_name == 'Janis Joplin'