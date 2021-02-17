"""
given a dictionary of keys=sons, values=fathers, find for each son the most distance father is has

"""
a = {
    'a': 'c',
    'c': 'd',
    'b': 'c',
    'd': None,
    'e': None,
    'h': 'a',
    'j':'k',
    'k':'j'


}


def find_distance_father():
    new_a = {}
    for key in a:
        father = a[key]
        seen = set()
        seen.add(father)
        while True:
            if father in a:
                if a[father] is not None and a[father] not in seen and key != a[father]:
                    father = a[father]
                else:
                    break
            else:
                break
        new_a[key] = father
    return new_a


new_a = find_distance_father()

print(new_a)

