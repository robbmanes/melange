#!/usr/bin/env python
import sys

# reads /etc/sub{u,g}id and parses into a human-readable format with examples
def main():
    if len(sys.argv) <= 1:
        file = '/etc/subuid'
    else:
        file = sys.argv[1]

    users = {}
    with open(file) as f:
        for line in f:
            user, id_start, id_range = line.split(':')
            if user not in users:
                users[user] = {}

            users[user][id_start] = id_range.replace('\n', '')

    line = 'INDIVIDUAL USER NAMESPACE REPORT'
    print(line)
    print('-' * len(line))
    fields = "{:^22s}|{:^22s}|{:^22s}"
    for name, entry in users.items():
        print('%s:' % (name))
        line = fields.format('amount_of_ids', 'starting_id', 'ending_id')     
        print(line)
        print('-' * len(line))
        total_ids = 0
        lowest_id = 0
        for id_start, id_range in entry.items():
            if lowest_id == 0 or lowest_id >= int(id_start):
                lowest_id = int(id_start)
            total_ids += int(id_range)
            id_end = str(int(id_start) + int(id_range))
            print(fields.format(id_range, id_start, id_end))
        if total_ids >= 1000:
            line = 'EXAMPLE: ID 1000 in a user namespace owned by {user} would be ID {host_id} on the host.'
            print(line.format(user=name, host_id=(lowest_id + 1000)))
        print("")



if __name__ == '__main__':
    sys.exit(main())
