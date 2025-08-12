# From: https://gist.github.com/TheusHen/698ccd93573c9f86d7c23a328c895570

import pyfiglet

def gen_art(text: str, font: str = "standard") -> str:
    return pyfiglet.figlet_format(text, font=font)