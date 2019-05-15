#!/usr/bin/env python

""" server.py: Authenticates to a server """

__author__ = "Konstantin Zelmanovich"

import sys
import json
import hashlib

my_dict = {}
seen = {}


def generate_hash_otp(secret_key, n):
    my_hash = secret_key
    for i in range(n):
        my_hash = hashlib.md5(my_hash).hexdigest()
    return my_hash


def verify_passwords(server_password, argv_password):
    return str(server_password) == str(argv_password)


def print_usage():
    print """  
    S/Key Server example usage:
            python server.py [password] : authenticates to a server

    S/Key Server example output:
            SUCCESSFULLY AUTHENTICATED | FAILED
    """


def main():
    if len(sys.argv) == 2:
        with open('./conf-server/storage.json') as f:
            my_json = json.load(f)
            server_password = my_json.items()[0][1]
            max_count = int(my_json.items()[0][0])

        argv_password = sys.argv[1]
        supplied_password = generate_hash_otp(argv_password, 1)

        # reading seen
        with open("./conf-server/expired.json", "r") as f:
            seen = json.load(f)

        # veryfying if the passwords match
        if verify_passwords(supplied_password, server_password):
            # checking if the password has been used
            if argv_password not in seen["seen"]:
                print "\nSUCCESSFULLY AUTHENTICATED\n"
                my_dict[max_count - 1] = supplied_password
                with open("./conf-server/storage.json", "w") as f:
                    json.dump(my_dict, f)

                seen['seen'].append(argv_password)
                with open("./conf-server/expired.json", "w") as f:
                    json.dump(seen, f)
            else:
                print "\nFAILED\n"
        else:
            print "\nFAILED\n"
    else:
        print_usage()
        exit(1)


if __name__ == "__main__":
    main()
