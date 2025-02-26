# -*- coding: utf-8 -*-
import random
from .constants import ID_CHARACTERS

"""
Generates random 7 character human-readable ID
"""
def generate():
    generated_id = ''
    for _ in range(7):
        generated_id = generated_id + random.choice(ID_CHARACTERS)
    return generated_id
