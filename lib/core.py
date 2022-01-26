import zlib
import random
import base64
import tokenize

from .utils import obfuscate_int, string_to_hex, obfuscate_string

from rich.console import Console


class Obfuscated:
    """Manage obfuscated code"""

    def __init__(self):
        self.indent_level: int = 0
        self.__content: str = ""

    def add_line(self, line: str, end=" #Obfuscator made by toast#3108\n") -> None:
        """Add a line to the code"""
        self.__content += ("    " * self.indent_level) + line + end

    @property
    def content(self) -> str:
        """Return the content"""
        return self.__content


class Obfuscator:
    """Obfuscate a file"""

    def __init__(self, file_name: str):
        self.console = Console()

        self.file = open(file_name, "r")

        with open(file_name, "r") as file:
            if "#7ta9x4ebgc37ho5yrdgdncxkw9xwle1y#" in file.read():
                self.console.print("Already obfuscated!")
                exit(0)

        self.generated_strings: list[str] = []

        self.eval = self.junk_string(10)
        self.mainf = self.junk_string(10)
        self.mainc = self.junk_string(10)
        self.exec = self.junk_string(10)
        self.comp = self.junk_string(10)
        self.none = self.junk_string(10)
        self.name = self.junk_string(10)
        self.hash = self.junk_string(10)
        self.arra = self.junk_string(10)

        self.obfuscated = Obfuscated()
        self.ident_level: int = 0

    def obfuscate_tokens(self) -> str:
        self.console.print("Tokenizing code...")

        _tokens = tokenize.generate_tokens(self.file.readline)
        tokens = []

        for token in _tokens:

            if token.type == 62:
                continue

            """
            if token.type == 3:
                token = tokenize.TokenInfo(
                    type=token.type,
                    string=obfuscate_string(token.string[1:-1], range=(1, 3)),
                    start=token.start,
                    end=token.end,
                    line=token.line,
                )
            """

            if token.type == 2:
                token = tokenize.TokenInfo(
                    type=token.type,
                    string=obfuscate_int(int(token.string), range=(1, 3)),
                    start=token.start,
                    end=token.end,
                    line=token.line,
                )

            tokens.append(token)

        return tokenize.untokenize(tokens)

    def obfuscate(self):
        """Obfuscate the code"""

        self.console.print("Generating template...")

        self.obfuscated.add_line(
            f"{self.eval}=eval({obfuscate_string('eval')});", end=""
        )

        obfuscated_exec = f"{self.eval}({obfuscate_string('exec')})"

        self.obfuscated.add_line(f"{self.exec}={obfuscated_exec};", end="")
        self.obfuscated.add_line("\n")

        self.obfuscated.add_line(
            f"{self.none},{self.name},{self.hash},{self.comp}"
            "="
            f"{self.eval}('{string_to_hex('None')}')"
            ","
            f"{self.eval}('{string_to_hex('__name__')}')"
            ","
            f"{self.eval}('{string_to_hex('hash')}')"
            ","
            f"{self.eval}('{string_to_hex('compile')}')"
        )

        lines = self.obfuscate_tokens().splitlines()

        self.obfuscated.add_line(
            f"{self.arra}={self.eval}({obfuscate_string('str()')});"
        )

        for line in lines:
            line += "\n"

            self.obfuscated.add_line(
                f"{self.arra}+={obfuscate_string(line)};"
            )

        code = ""
        code += self.comp
        code += "("
        code += self.arra
        code += ","
        code += obfuscate_string("<string>", range=(1, 2))
        code += ","
        code += obfuscate_string("exec")
        code += ")"

        self.obfuscated.add_line(f"{self.exec}({code})")

    def junk_string(self, length: int = 10, b64: bool = False) -> str:
        """Generate a random string of a given length"""
        string = "".join(random.choice("Il") for _ in range(length))

        if string in self.generated_strings:
            string = self.junk_string(length, b64)

        self.generated_strings.append(string)

        return (
            base64.b64encode(string.encode()).decode().replace("=", "")
            if base64
            else string
        )

    def finalize(self) -> str:
        """Finalize the code"""

        self.console.print("Finalizing with zlib compression...")

        compressed = zlib.compress(self.obfuscated.content.encode())

        final = (
            "import sys\n"
            "sys.setrecursionlimit(999999999)\n"
            "exec("
            f"__import__('{string_to_hex('zlib')}').decompress({compressed})"
            ")  #7ta9x4ebgc37ho5yrdgdncxkw9xwle1y#"
        )

        final_size = len(final)

        self.console.print(f"Final code lenght: {final_size:,} ")

        return final
