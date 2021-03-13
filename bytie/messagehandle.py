from dotenv import load_dotenv
import ast
import requests
import hashlib
import random
import re
import os
import glob
import subprocess
import atexit
import json
import yfinance
from os import path
from numpy import fromstring, array2string
from numpy.fft import fft
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

try:
    import mandelbrot
    import lambada
    import libstdlambada
except Exception:
    from . import mandelbrot
    from . import lambada
    from . import libstdlambada


load_dotenv()

HOST = os.getenv("BYTIE_HOST") or 'http://localhost/'
PATH = os.getenv("BYTIE_PATH") or './.tmp'

# initialize interpreter
lambadainterpreter = lambada.Interpreter()
lambadainterpreter.addvar(
    "sum", lambada.PythonFunctionExpression(libstdlambada.sum))
lambadainterpreter.addvar(
    "mean", lambada.PythonFunctionExpression(libstdlambada.mean))
lambadainterpreter.addvar(
    "median", lambada.PythonFunctionExpression(libstdlambada.median))
lambadainterpreter.addvar(
    "plot", lambada.PythonFunctionExpression(libstdlambada.plot))
lambadainterpreter.addvar(
    "quantile", lambada.PythonFunctionExpression(libstdlambada.quantile))
lambadainterpreter.addvar(
    "random", lambada.PythonFunctionExpression(libstdlambada.draw_random_numbers))

message_handlers = []


def message_handler(name: str, prefix: bool = True, probability: float = 0.0):
    def decorator(func):
        def handler(message):
            if (prefix and message.startswith(name + ' ')) or (not prefix and message == name):
                msg = message[min(len(message), len(name)+1):]
                try:
                    return func(msg)
                except Exception as e:
                    return 'Beep boop! bytie is confused! ' + str(e)
            elif random.random() < probability:
                try:
                    return func(message)
                except Exception as e:
                    return 'Beep boop! bytie is confused! ' + str(e)
            return ''
        if func.__doc__ == None:
            # dev warning message
            print(
                f"Please provide a docstring for your message handler '{name}'. This will be used for help messages."
            )
            return func
        message_handlers.append({
            "name": name,
            "prefix": prefix,
            "probability": probability,
            "handler": handler,
            "help_message": func.__doc__,
            "function": func
        })
        return func

    return decorator


@message_handler("hey bytie!", prefix=False)
def bytie_handle_hey_bytie(command: str) -> str:
    "hey bytie!: I say 'Yes, sir!'"
    return "Yes, sir!"


@message_handler("ast")
def bytie_handle_ast(command: str) -> str:
    "ast ${python code} I generate abstract syntax trees"
    parsed = ast.parse(command)
    tree = ast.dump(parsed)
    return tree


@message_handler("latex")
def bytie_handle_latex(command: str) -> str:
    "latex ${equation}: I generate LaTeX equations"
    return "https://latex.codecogs.com/png.latex?" + command


@message_handler('8ball')
def bytie_handle_8ball(command: str) -> str:
    "8ball ${question} : I deeply analyze your question and give a comprehensive answer."
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
    number = int(hashlib.sha1(command.encode("utf-8")).hexdigest(), 16)
    return eight_ball_messages[number % len(eight_ball_messages)]


@message_handler('dadjoke', prefix=False)
def bytie_handle_dadjoke(command: str) -> str:
    "dadjoke: I prepare a top quality joke for you."
    resp = requests.get(
        "https://icanhazdadjoke.com", headers={"Accept": "application/json"}
    )
    if resp.status_code == 200:
        joke_id = resp.json()["id"]
        return f"https://icanhazdadjoke.com/j/{joke_id}.png"
    else:
        return "Couldn't get a dadjoke :("


@message_handler("say something new", prefix=False)
def bytie_handle_saysomethingnew(message: str) -> str:
    "say something new: Let me pick new things!"
    resp = requests.get("https://uselessfacts.jsph.pl/random.txt?language=en")
    if resp.status_code == 200:
        return resp.text.split("\n")[0]
    else:
        return "failatun failun failure :("


@message_handler("iplikisyin", probability=0.025)
def bytie_handle_iplikisyin(message: str) -> str:
    "iplikisyin ${message} : I show you exactly what you sound like."
    vowels = r"[aeıioöuü]"
    choice = random.choice("io")
    result = re.sub(vowels, choice, message.lower()) + " :rofl:"
    return result


@message_handler("usd", prefix=False)
def bytie_handle_dolar(message: str) -> str:
    "usd: Price of USD in Turkish Liras"
    webcontent = requests.get("https://themoneyconverter.com/USD/TRY").text
    parsed1 = webcontent.split("1 USD = ")
    dolartl = parsed1[1].split(" ")[0]
    return dolartl


@message_handler("fft?", prefix=False)
def bytie_handle_fft(message: str) -> str:
    "fft?: I tell you top secret information about fft."
    return "lib var"


@message_handler("fft")
def bytie_handle_fftCalc(xs: str) -> str:
    "fft <',' or ' ' seperated numbers>: I calculate fft of your numbers."
    if ',' in xs:
        xs = fromstring(xs, dtype=float, sep=",")
    else:
        xs = fromstring(xs, dtype=float, sep=" ")
    if xs.size > 0:
        return array2string(fft(xs), precision=2)
    else:
        return "meh"


@message_handler("mandelbrot")
def bytie_handle_mandelbrot(command: str) -> str:
    "mandelbrot ${x} ${y} ${zoom} ${iterations} ${divergence_radius} : I generate a mandelbrot image for you."
    args = command.split()
    try:
        x = float(args[0])
        y = float(args[1])
        zoom = float(args[2])
        max_iter = int(args[3])
        divergance_radius = float(args[4])
    except:
        return "Please feed a zoom and a center paramter! Also maximum number of iterations and divergence radius!"

    filename = f"image_{x}_{y}_{zoom}_{max_iter}_{divergance_radius}.png"
    filepath = f"{PATH}/{filename}"
    url = f"{HOST}/{filename}"
    if not(path.exists(filepath)):
        mandelbrot.mandelbrot(zoom=zoom, center=(
            x, y), filename=filepath, max_iter=max_iter, div_radius=divergance_radius)
    return url


@message_handler("XTRY")
def bytie_handle_XTRY(currency: str) -> str:
    "XTRY ${abbr. of currency}: Price of a currency in Turkish Liras"
    currency = currency.upper()
    r = requests.get(
        "https://api.exchangeratesapi.io/latest?base=TRY").json()["rates"]
    if currency in r:
        XTRY = 1/r[currency]
        return f"{currency}TRY: {XTRY:.2f}"
    else:
        return "Please enter a valid currency abbrevation"


@message_handler("lambada")
def bytie_lambada_command(command: str) -> str:
    "lambada {expression}: I want to be Clojure when I grow up"
    try:
        result = lambadainterpreter.interprete(command)
        return result
    except BaseException as inst:
        return str(inst)


@message_handler("!xkcd")
def bytie_xkcd_command(command: str) -> str:
    "!xkcd {num}: I show you the xkcd you specified. Random xkcd for bad inputs."
    try:
        nxkcd = int(command)
        return bytie_handle_xkcd(nxkcd)
    except(ValueError, TypeError):
        return bytie_handle_randomxkcd()


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
        rnd = random.randint(1, maxkcd)
        return (bytie_handle_xkcd(rnd))
    else:
        return f"xkcd down :/"


@message_handler('bytie update and restart!', prefix=False)
def bytie_update_and_restart(message: str) -> str:
    "bytie update and restart!: Run git pull and register atexit() to restart run.sh"
    result = subprocess.run(["git", "pull"])

    def bytieatexit():
        subprocess.Popen(["/bin/bash", "run.sh"])

    atexit.register(bytieatexit)
    print("By by bytie!")
    exit(0)
    # Never runs.
    return "Restarting..."


@message_handler('bytie tell me a story!', prefix=False)
def bytie_handle_tell_story(message: str) -> str:
    "bytie tell me a story!: biyti til mi i sitiri :rofl:"
    urls = [
        "http://4.bp.blogspot.com/-txmMmc24--I/VZ663QSkjoI/AAAAAAAAAto/uNg3peYTV-k/s1600/10.jpg",
        "https://listelist.com/wp-content/uploads/2015/02/twitter-fenomeni-mememetali-620x375.jpg",
        "https://img-s2.onedio.com/id-55047c15ff285b051a6db88f/rev-0/w-635/listing/f-jpg-webp/s-da729d8e8726fa8611d4cd227133dcd57cdc797f.webp",
        "https://img-s1.onedio.com/id-55047c2add6e2f5b444334ba/rev-0/w-635/listing/f-jpg-webp/s-90ba45a4f5c476c0f30ae051f49ac5b7d775caaf.webp",
        "https://lh3.googleusercontent.com/proxy/i3y1JJen_Yoqup2G7aHTrleVk04KVvoL4H6P5BZRqYFdwmsTdAuzBpDbTXqipXYWcA57uJvF5s93WDaLZfpUbBcGsl75Ao-VarLheXlxHuJN",
        "https://www.pekguzelsozler.com/wp-content/uploads/2018/06/Mehmet-Ali-S%C3%B6zleri.jpg",
        "https://lh3.googleusercontent.com/proxy/k9Xq6CGQouGDh-hfcrm74O24INK3DsvV8WjiWAl2U9TSSBKC-p32zDn7UjWdWEcDFhgBbD9qpaIIMsjgCKzXbCNmPAQUiUmSBI4Y148aQyB2",
        "https://galeri14.uludagsozluk.com/766/mehmet-ali-hikayeleri_1966871.jpg",
        "https://lh3.googleusercontent.com/proxy/YPEWqXacnbOVRMDDAGoVvad73OznLON8-1UPKlVNG_xPhmqlzs1yYR8WFZOnRhoUHrzmG5Xj6lUA3WVFEnRGmVjzaeyy4B7OriCF9iSIjkyT",
        "https://galeri14.uludagsozluk.com/771/mehmet-ali-hikayeleri_1966872.png",
        "https://lh3.googleusercontent.com/proxy/gnEBxKRuPrTokcLmbI-n0NG5is4Sm2--SvCdt3CwmL2Dem6cgm6-9F2cOY_L0kzOg_-2w0YYbJKT--xUXYmteAiGiUlY2yhtC43Pzidby3U",
        "https://lh3.googleusercontent.com/proxy/du3Tnk4NlxAGxSGwN9YtB_ZSfbbr-puyMBSRFxzIjLgW9ZDjk2zfKulKXIItzIjtjwM8vUw2OdiesdLkc8Nt0QxmVWWMOnWIeQEZ6fLT5KM",
        "https://lh3.googleusercontent.com/proxy/gLjCNM1B3KILiXMOROa4GLkw3-DSIZBRVEWQrFcTfQSigmo5CntZ1vKTZ3Hzh8EDwy9mH5wv0biQNt8HXah4lEW8kmbU4marmzVQ92DUFjs",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRELhz2h8-e6O9YPfCB83UY7WJECHhxL4cy_w&usqp=CAU",
        "https://www.istanbulhaber.com.tr/d/gallery/1968_1.jpg",
        "https://lh3.googleusercontent.com/proxy/TOcrqDhr13oJ_qYjyf4bBhCEd5D-ib-WQCoGL3weG6E4GFkNMYPVRiFOILrPaOQtogH7U8-ReZcgj5nYUqreKofj4poFUCl3Z-DkuPBec1bWjtGEHW12FSZN9rbUh1aFvbP4hQq6PqzN3EoNDaH4phTf4ySbbsuzsUaGl1AXG8HFwGo",
        "https://64.media.tumblr.com/bb812bdec87f92afb2d3128e62ffe61c/tumblr_o1mp4uUwKK1ujmvy2o1_500.jpg",
        "http://img7.mynet.com/galeri/2015/02/09/024123679/8506980-501x226.jpg",
        "https://galeri8.uludagsozluk.com/416/mememetali_752598.jpg",
        "https://www.youtube.com/watch?v=QGkIeNlJaPU",
        "https://www.youtube.com/watch?v=aNossrX5PqQ",
        "https://img-s1.onedio.com/id-55047c2add6e2f5b444334ba/rev-0/w-635/listing/f-jpg-webp/s-90ba45a4f5c476c0f30ae051f49ac5b7d775caaf.webp",
        "https://img-s2.onedio.com/id-55047c621a21b1541537eb59/rev-0/w-635/listing/f-jpg-webp/s-836d804ea708a8802009f8290fc066febd35c20b.webp",
        "https://img-s2.onedio.com/id-55047c6d1a21b1541537eb5d/rev-0/w-635/listing/f-jpg-webp/s-28bb362a18017115392de02bf1ad9c02dc9a0708.webp",
        "https://img-s1.onedio.com/id-55047cb1e2cec1b01338bb60/rev-0/w-635/listing/f-jpg-webp/s-1dd66044823b4066a29a2cbe4ff19023562c20d2.webp",
        "https://iasbh.tmgrup.com.tr/21ecd2/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/4.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/6ec9de/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/5.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/535a3e/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/6.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/ef07d8/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/7.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/972982/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/8.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/abaefa/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/9.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/966b3d/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/10.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/2b9696/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/11.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/aa58a6/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/14.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/0bbf5f/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/15.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/7ceb3e/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/17.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/3d217d/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/18.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/52ad4e/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/19.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/d20ce3/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/21.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/5655ee/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/22.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/bf61a4/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/23.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/f90cd8/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/24.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/7de959/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/25.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/908471/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/26.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/d8bdaa/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/27.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/aaca39/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/28.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/a81ff2/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/29.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/69850f/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/30.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/580fa6/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/31.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/64f064/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/32.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/1fd0dc/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/34.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/249887/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/35.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/640be6/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/38.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/1c6408/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/40.jpg&mw=752&mh=700",
        "https://iasbh.tmgrup.com.tr/86e4f0/0/0/0/0/0/0?u=http://i.teknokulis.com/galeri/internet/twiterin-son-fenomeni-ile-tanisin-mehmet-ali/41.jpg&mw=752&mh=700",
        "Çocuk kızı kaçırmış kız ilk baş ondan nefret etmiş sonra çocuk odun kırıyormuş kız camdan onu görmüş demiş ne güçlü bi erkek aşık olmuş..",
        "Çocukla kız tepeye çıkmışlar kız çocuğu uçurumdan aşağı itmiş çocuk demiş naaptın kız demiş ittim seni çocuk demiş ama neden kız demiş çünkü herkes öldürür sevdiğini..."
    ]
    return random.sample(urls, 1)[0]


@message_handler('bytie play song!', prefix=False)
def bytie_handle_play_song(message: str) -> str:
    "bytie play song!: I always forget the lyrics."
    return "This command is deprecated and will be removed in future releases. I don't think of being a robot in my next life."


@message_handler('bytie clean temp!', prefix=False)
def bytie_handle_clean_temp(message: str) -> str:
    "bytie clean temp!: Trig my garbage collector!"
    files = glob.glob(PATH + "/*")
    for f in files:
        os.remove(f)
    L = len(files)
    return f"I removed {L} garbage(s)"


@message_handler('bytie help!', prefix=False)
def bytie_handle_help(message: str) -> str:
    "bytie help! : Do you really need more help?"
    docs = []
    for handler in message_handlers:
        msg = handler['help_message']
        docs.append(f"\n\n            - {msg}")
    docs = "".join(docs)
    return f"Welcome, I am the bot of this channel. Try typing:{docs}"


@message_handler('python', prefix=False)
def bytie_handle_python(message: str) -> str:
    "python: I tell you the objective truth about python."
    return "python is great, and you should feel proud of it."


@message_handler("stonks")
def bytie_handle_stonks(command: str) -> str:
    "stonks {STOCKCODE}: as historical as Fortran. See: stock"
    stockname = command
    stockinfo = yfinance.Ticker(stockname)
    data = stockinfo.history(period="1mo")
    closes = list(data["Close"])
    n = len(closes)
    if len(data) == 0:
        return "No data found: " + str(command)
    else:
        filename = f"image_{stockname}.png"
        filepath = f"{PATH}/{filename}"
        url = f"{HOST}/{filename}"
        t = range(n)
        plt.plot(t, closes)
        plt.title(f"Last {n} days of {stockname}")
        plt.savefig(filepath)
        plt.close()
        return url


@message_handler("stock")
def bytie_handle_stock(command: str) -> str:
    "stock {STOCKCODE}: Örnek vereyim, stock GOOG"
    stockinfo = yfinance.Ticker(command)
    data = stockinfo.history(period="")

    if len(data) == 0:
        return "No data found: " + str(command)
    else:
        formatted = data.T.to_string(float_format='{:,.4f}'.format)
        result = "```\n" + command + "\n\n" + formatted + "\n```"
        return result


@message_handler("datetime")
def bytie_handle_datetime(command: str) -> str:
    "datetime region/location: I don't need an  watch."
    capt = requests.get(
        f"http://worldtimeapi.org/api/timezone/{command}")
    result = ""
    try:
        jsondata = json.loads(capt.text)
        result = jsondata["datetime"]
    except:
        result = "¯\_(ツ)_/¯ ney?"
    return result


@message_handler('bytie korona!', prefix=False)
def bytie_handle_covid(command: str) -> str:
    "bytie korona!: I show you daily vaka sayısı."

    url = 'https://covid19.saglik.gov.tr/TR-66935/genel-koronavirus-tablosu.html'
    content = requests.get(url).text

    try:
        rgx = r"var geneldurumjson = (\[.*?\]);//]]"
        match = re.search(rgx, content).group(1)
        data = json.loads(match)
        daily = data[0]

        res = """**{tarih}**
    * **Vaka**:  {gunluk_vaka}
    * **Test**:  {gunluk_test}
    * **Hasta**: {gunluk_hasta}
    * **Vefat**: {gunluk_vefat}
    * **İyileşen**: {gunluk_iyilesen}
    """.format(**daily)

        return res

    except Exception as e:
        return "Format değişmiş haberin yok! " + str(e) + " :/"


@message_handler('bytie weather')
def bytie_weather(command: str) -> str:
    "bytie weather: I show you weather condition anywhere in the world. bytie weather <city>"
    command= command.capitalize()
    if command[0] == "İ":
        new = list(command)
        new[0] = "I"
        command = ''.join(new)
    url = "https://www.google.com/search?q=" + "weather" + command
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str1 = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str1.split('\n')
    sky = data[1]
    result = f"{command} için hava durumuna bakıyorum.\n Hava sıcaklığı: {temp}\n Gökyüzü: {sky}"
    return result



if __name__ == '__main__':
    @message_handler('test', prefix=True, probability=0)
    def test(message):
        "test : tests @message_handler functionality"
        return message + ', indeed.'
    while True:
        text = input("bytie> ")
        for handler in message_handlers:
            message = handler['handler'](text)
            if message:
                print(message)
