#!/usr/bin/env python

""" client.py: Generates a one-time password prints it's hashed version """

__author__ = "Konstantin Zelmanovich"

import sys
import json
import hashlib

my_dict = {}


def generate_hash_otp(secret_key, n):
    my_hash = secret_key
    for i in range(n):
        my_hash = hashlib.md5(my_hash).hexdigest()
    return my_hash


def print_usage():
    print """  
    S/Key Client example usage:
            python client.py : generates a one-time password

    S/Key Client example output:
            Your one-time password is: [password]
    """


def main():
    if len(sys.argv) == 1:
        with open("./conf-client/secret.txt") as f:
            my_data = f.readlines()
            secret_key = my_data[0]
            n = int(my_data[1])
            print "\nYour one-time password is: " + str(generate_hash_otp(secret_key, n - 1)) + "\n"

        # Storing n-th in json storage
        my_dict[n] = generate_hash_otp(secret_key, n)
        with open("./conf-server/storage.json", "w") as f:
            json.dump(my_dict, f)

        # Decrement n from secret.txt
        with open("./conf-client/secret.txt", "r") as f:
            get_all = f.readlines()

        with open("./conf-client/secret.txt", "w") as f:
            for i, line in enumerate(get_all, 1):
                if i == 2:
                    f.writelines(str(int(get_all[1]) - 1))
                else:
                    f.writelines(line)
    else:
        print_usage()


if __name__ == "__main__":
    main()
