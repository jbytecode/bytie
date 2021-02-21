import ast
import requests
import hashlib
import random
import re
import os
import glob
from os import path
from numpy import fromstring, array2string
from numpy.fft import fft

import mandelbrot

from dotenv import load_dotenv

load_dotenv()


def bytie_handle_hey_bytie() -> str:
    return "Yes, sir!"


def bytie_handle_ast(command: str) -> str:
    parsed = ast.parse(command)
    tree = ast.dump(parsed)
    return tree


def bytie_handle_latex(command: str) -> str:
    return "https://latex.codecogs.com/png.latex?" + command


eight_ball_messages = [
    "As I see it, yes.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don’t count on it.",
    "It is certain.",
    "It is decidedly so.",
    "Most likely.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Outlook good.",
    "Reply hazy, try again.",
    "Signs point to yes.",
    "Very doubtful.",
    "Without a doubt.",
    "Yes.",
    "Yes – definitely.",
    "You may rely on it.",
]


def bytie_handle_8ball(command: str) -> str:
    number = int(hashlib.sha1(command.encode("utf-8")).hexdigest(), 16)
    return eight_ball_messages[number % len(eight_ball_messages)]


def bytie_handle_dadjoke() -> str:
    resp = requests.get(
        "https://icanhazdadjoke.com", headers={"Accept": "application/json"}
    )
    if resp.status_code == 200:
        joke_id = resp.json()["id"]
        return f"https://icanhazdadjoke.com/j/{joke_id}.png"
    else:
        return "Couldn't get a dadjoke :("


def bytie_handle_saysomethingnew() -> str:
    resp = requests.get("https://uselessfacts.jsph.pl/random.txt?language=en")
    if resp.status_code == 200:
        return resp.text.split("\n")[0]
    else:
        return "failatun failun failure :("


def bytie_handle_iplikisyin(message: str) -> str:
    vowels = r"[aeıioöuü]"
    choice = random.choice("io")
    result = re.sub(vowels, choice, message.lower()) + " :rofl:"
    return result


def bytie_handle_dolar():
    webcontent = requests.get("https://themoneyconverter.com/USD/TRY").text
    parsed1 = webcontent.split("1 USD = ")
    dolartl = parsed1[1].split(" ")[0]
    return dolartl

def bytie_handle_fft():
    return "lib var"

def bytie_handle_fftCalc(xs: str) -> str:
    if ',' in xs:
        xs = fromstring(xs, dtype=float, sep=",")
    else:
        xs = fromstring(xs, dtype=float, sep=" ")
    if xs.size > 0:    
        return array2string(fft(xs), precision=2)
    else:
        return "meh"

def bytie_handle_mandelbrot(command: str) -> str:
    """
    mandelbrot <x> <y> <zoom> <max_iter> <divergance_radius>

    """
    args = command.split()
    try:
        x = float(args[1])
        y = float(args[2])
        zoom = float(args[3])
        max_iter = int(args[4])
        divergance_radius = float(args[5])
    except:
        return "Please feed a zoom and a center paramter! Also maximum number of iterations and divergance radius!"

    HOST = os.getenv("BYTIE_HOST")
    PATH = os.getenv("BYTIE_PATH")

    filename = f"image_{x}_{y}_{zoom}_{max_iter}_{divergance_radius}.png"
    filepath = f"{PATH}/{filename}"
    url = f"{HOST}/{filename}"
    if not(path.exists(filepath)):
        mandelbrot.mandelbrot(zoom=zoom, center=(x, y), filename=filepath, max_iter=max_iter, div_radius=divergance_radius)
    return url

def bytie_handle_XTRY(currency):
    r = requests.get("https://api.exchangeratesapi.io/latest?base=TRY").json()["rates"]
    if currency in r:
        XTRY = 1/r[currency]
        return f"{currency}TRY: {XTRY:.2f}"
    else:
        return "Please enter a valid currency abbrevation"

def bytie_handle_xkcd(n):
    r = requests.get(f"https://xkcd.com/{n}/info.0.json")
    if r.status_code == 200:
        return r.json()["img"]
    else:
        return f"Two possibilities exist: either xkcd down or xkcd {n} does not exist. Both are equally terrifying."

def bytie_handle_randomxkcd():
    r = requests.get(f"https://xkcd.com/info.0.json")
    if r.status_code == 200:
        maxkcd = r.json()["num"]
        rnd = random.randint(1,maxkcd)
        return (bytie_handle_xkcd(rnd))
    else:
        return f"xkcd down :/"

def bytie_handle_clean_temp()->str:
    files = glob.glob(os.getenv("BYTIE_PATH") + "/*")
    for f in files:
        os.remove(f)
    L = len(files)
    return f"I removed {L} garbage(s)"

def bytie_handle_help() -> str:
    help_str = """
        Welcome, I am the bot of this channel. Try typing:

        - hey bytie!: I say 'Yes, sir!'
        
        - ast ${python code}: I generate abstract syntax trees 

        - latex ${equation}: I generate LaTeX equations

        - 8ball ${question}: I deeply analyze your question and give a comprehensive answer. Ersagun did this patch. 

        - dadjoke: I prepare a top quality joke for you. 

        - say something new: Let me pick new things!

		- usd: Price of USD in Turkish Liras

        - mandelbrot ${x} ${y} ${zoom} : I generate a mandelbrot image for you. 
	
	    - fft?: I tell you top secret information about fft.
	
	    - fft <',' or ' ' seperated numbers>: I calculate fft of your numbers.

        - XTRY ${abbr. of currency}: Price of a currency in Turkish Liras

        - !xkcd {num}: I show you the xkcd you specified. Random xkcd for bad inputs.

        - bytie clean temp!: Trig my garbage collector!

        - bytie help!: this.help();

    """
    return help_str
