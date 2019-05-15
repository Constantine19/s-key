# S/Key One-Time Password implementation

Description
===========

S/Key is a one-time password system. Each password used in the system is usable only for one authentication. Hence, passwords are not re-usable, and therefore, if there is a "man-in-the-middle" attack and a password is intercepted, it is not going to be useful. Additionally, knowledge of already-used passwords in a user's S/Key password sequence provide no information about future passwords. Thus, even all of one's S/Key passwords are "sniffed" as they transit an insecure network, they will not benefit their interceptor.


To run
======

First, a user initializes S/Key by selecting a secret plaintext password. A secure hash function (MD5) is applied to the secret password `n` times (10000 by default).
Run the following command to initialize a user with a secret plaintext password:
```
~/s-key/python key-init.py
```
Below is the output:
```
Initialize your plaintext password: <PASSWORD>

Initialization completed!
```
The result of the last hash is stored on the server. 
Now, when user attempts to log in, the server will issue a challenge, which is the number `n-1`. 

Client machine will apply `n-1` iterations of the hash function to the secret key and will send this response to the server. Run the following command to start a client:

```
~/s-key/python client.py
```
 
This will generate a one-time `n-1-th` password and will print it:

```
~/s-key/python client.py
Your one-time password is: 3a2e3f5a631de31410fc439cf8c26913
```
After a one-time password is generated, it is ready to be used to authenticate to a server. The server will apply the MD5 hash function to this `n-1-th` response. Therefore, transforming it into `n-th` value, that is stored on the server and compare it.

 Run the below command and use the password, that was received from client, as an argument:
```
~/s-key/python server.py 3a2e3f5a631de31410fc439cf8c26913
```

If the result it obtains is the same as the value it stored earlier:
* The authentication worked
    - It will print: `SUCCESSFULLY AUTHENTICATED`
    - The user is allowed in, and the server replaces the stored value with the response obtained from the client, and decrements the password counter.

If the result it obtains is different from the value it stored:
* The authentication did not work
    - It will print `FAILED`


High Level Architecture
=======================

## Configuration
There are two configurations:
* `/conf-client`
    - located on the client side
    - contains:
        - `sercret.txt`
            - holds the original password and the number of times that it is being hashed. By default this number is 10000

* `/conf-server`
    - located on the server side
    - contains:
        - `expired.json`
            - holds all the passwords that were used per session so that a password is not being used more than once
        - `storage.json`
            - keeps track of the stored n-th cash, so that when n-1-th hash is supplied, it can be evaluated and verified

## Crypto

The MD5 was chosen as a hashing algorithm for this project. The reasons behind this decision is for its speed (in comparison with SHA256) and wide availability across multiple programming languages.

The MD5 algorithm takes a message as an input of arbitrary length and produces as output a 128-bit
message digest of the input. The authentication algorithm computes a digest of the entire data of the secret message, used for authentication. MD5 consists of 64 operations, grouped into four rounds of 16 operations, which makes it very secure and almost impossible to reverse back to it's original plaintext.

Below is the method, that generates md5 hex digest using a `secret_key` (that is provided by user) and `n`, a number of times to hash it.
```
def generate_hash_otp(secret_key, n):
    my_hash = secret_key
    for i in range(n):
        my_hash = hashlib.md5(my_hash).hexdigest()
    return my_hash
```


## Communication Model

The client/server model introduces two roles that can be assumed by processes: the role of service user - `client` and the role of service provider - `server`. The distribution of roles implies an asymmetry in the distributed execution of an application. The server offers a service to which one or more clients has access. 

## Test cases

Below are the several test cases that were performed.
* Supplying empty plaintext secret key
```
┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python key-init.py 

Initialize your plaintext password: 

Password can not be empty
```
* Supplying non-empty plaintext secret key
```
┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python key-init.py 

Initialize your plaintext password: 12345678

Initialization completed!

```
* Running client.py multiple times and using not the most recent password
```
┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python client.py 

Your one-time password is: ecc414ddf0c4f51837c0b8a024723118

┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python client.py 

Your one-time password is: 28ae93dd4bf930f004bcecba0abf6c20

┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python client.py 

Your one-time password is: 8ace4a519aa81486a6c987741bc37f8a

┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python client.py 

Your one-time password is: 9531254304823f9a7f7bf88537c724d3

┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python server.py ecc414ddf0c4f51837c0b8a024723118

FAILED

```

* Running client.py multiple times and using the most recent password
```
┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python client.py 

Your one-time password is: 80e92e3c6440b7652aacccf80f371bf2

┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python client.py 

Your one-time password is: 3f5786cad41584a6ab168fb727a659b6

┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python client.py 

Your one-time password is: 68d6504ea125fa891514e4bf88ef7da3

┌─[~/Desktop/CS 475/cs475-spring-2019/s-key]
└──╼ python server.py 68d6504ea125fa891514e4bf88ef7da3

SUCCESSFULLY AUTHENTICATED
```