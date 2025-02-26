# -*- coding: utf-8 -*-
import random
from .constants import ID_CHARACTERS

ids = set()

"""
Generates random 7 character human-readable ID
"""
def generate():
    generated_id = ''
    is_unique = False
    while not is_unique:
        for _ in range(7):
            generated_id = generated_id + random.choice(ID_CHARACTERS)
        if generated_id not in ids:
            ids.add(generated_id)
            is_unique = True
        else:
            generated_id = ''
    return generated_id

"""
Generates unique 7 character human-readable ID
"""
def generate_bulk(bulk_size):
    generated_ids = set()
    for _ in range(bulk_size):
        generated_ids.add(generate())
    return generated_ids
