person = 'albert einstein    '
message = 'Once said, "A person who never made a mistake never tried anything new." some more'

full_message = f'{person.title().strip()}. \n\t{message}'
print(full_message.removesuffix(' some more'))