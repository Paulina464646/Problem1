
from random import shuffle, choice
from os import urandom
from hashlib import sha1

# Merkles-Puzzles
task_size = 2 ** 16

def merkles_puzzle():
    secret = [None] * task_size
    puzzles = [None] * task_size

    for i in range(task_size):# Alice generated a lot of secrets

        secret[i] = urandom(16)# messages generation

        pair = secret[i] + int.to_bytes(i, 4, 'big') # messages + index
        # pair and sha1
        plaintxt = pair + sha1(pair).digest()

        key = urandom(10)# Alice cyphers the message:
        noise = sha1(key).digest()
        noise = noise + sha1(noise).digest()
        ciphertxt = bytes(i ^ j for i, j in zip(plaintxt, noise))

        puzzles[i] = ciphertxt + key[2:]
    shuffle(puzzles)
    return secret, puzzles

def solve_puzzle(puzzle):
    ciphertxt = puzzle[:40]
    key = puzzle[40:]

    for i in range(task_size):

        noise = sha1(int.to_bytes(i, 2, 'big') + key).digest() # possibilities
        noise = noise + sha1(noise).digest()# Bob decyphers the message
        plaintxt = bytes(i ^ j for i, j in zip(ciphertxt, noise))

        pair = plaintxt[:20]
        digest = plaintxt[20:]

        if sha1(pair).digest() == digest:
            return i, pair[:16], int.from_bytes(pair[16:], 'big')


alice_secret, public_puzzles = merkles_puzzle()

bob_time, bob_secret, public_index = solve_puzzle(choice(public_puzzles))

print('Massage and index published by Bob')
print('Full key:', bob_secret)
print('Index:', public_index)
print('Total steps:', bob_time)
print('Message shared by Alice ')
print('Full key:', alice_secret[public_index])
total_time, total_puzzles = 0, 0

for puzzle in public_puzzles:
    adv_time, adv_key, adv_index = solve_puzzle(puzzle)
    total_time = total_time + adv_time
    total_puzzles = total_puzzles + 1

    if adv_index == public_index:
        print('The secret has been found: ', adv_key)
        break

    if total_time > bob_time * 100:
        print('No results')
        break

print('searched puzzles:', total_puzzles)
print('steps:', total_time)