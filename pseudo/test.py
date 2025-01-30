def josephus(size, stride, number):
    people = [i for i in range(1, size + 1)]
    capped = number if size % stride == 0 else min(number, size)

    index = 0
    visited_since_last_kill = stride
    killed = 0
    last_killed = 0
    while killed < capped:
        i = index % size
        person = people[i]

        if person == 0:
            index += 1
        else:
            if visited_since_last_kill == stride:
                people[i] = 0
                killed += 1
                visited_since_last_kill = 0
                last_killed = person
            visited_since_last_kill += 1

        index += 1
    return last_killed


print(josephus(10, 3, 5))
