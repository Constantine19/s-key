#!/usr/bin/env python

""" key-init.py: Initializes a user with a secret password """

__author__ = "Konstantin Zelmanovich"

import json
import hashlib

my_dict = {}

def generate_hash_otp(secret_key, n):
    my_hash = secret_key
    for i in range(n):
        my_hash = hashlib.md5(my_hash).hexdigest()
    return my_hash

def main():
    passw = raw_input("\nInitialize your plaintext password: ")

    if passw is "":
        print "\nPassword can not be empty\n" 
        exit(1)

    with open("./conf-client/secret.txt", "w+") as f:
        f.write(passw + "\n")
        f.write("10000")

    with open("./conf-client/secret.txt") as f:
        my_data = f.readlines()
        secret_key = my_data[0]
        n = int(my_data[1])

    # Storing n-th in json storage
    my_dict[n] = generate_hash_otp(secret_key, n)
    with open("./conf-server/storage.json", "w") as f:
        json.dump(my_dict, f)


    seen = {}
    seen['seen'] = []
    with open("./conf-server/expired.json", "w") as f:
        json.dump(seen, f)
        
    print "\nInitialization completed!\n"


if __name__ == "__main__":
    main()