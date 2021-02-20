import ast
import hashlib

def bytie_handle_hey_bytie() -> str:
    return "Yes, sir!"


def bytie_handle_ast(command: str) -> str:
    parsed = ast.parse(command)
    tree = ast.dump(parsed)
    return tree


def bytie_handle_latex(command: str) -> str:
    return "https://latex.codecogs.com/png.latex?" + command


eight_ball_messages = [
    'As I see it, yes.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don’t count on it.',
    'It is certain.',
    'It is decidedly so.',
    'Most likely.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Outlook good.',
    'Reply hazy, try again.',
    'Signs point to yes.',
    'Very doubtful.',
    'Without a doubt.',
    'Yes.',
    'Yes – definitely.',
    'You may rely on it.'
]
def bytie_handle_8ball(command: str) -> str:
    number = int(hashlib.sha1(command.encode("utf-8")).hexdigest(), 16)
    return eight_ball_messages[number % len(eight_ball_messages)]


def bytie_handle_help() -> str:
    help_str = """

        Welcome, I am the bot of this channel. Try typing:

        - hey bytie!
                I say 'Yes, sir!'

        - ast ${python code}
                I generate abstract syntax trees 

        - latex ${equation}
                I generate LaTeX equations

        - 8ball ${question}
                I deeply analyze your question and give a comprehensive answer. 
                Ersagun did this patch. 

        - bytie help!
                this.help();

    """
    return help_str


