import io
import re

__all__ = ["ParseError", "OverviewerQuotes"]


class ParseError(ValueError):
    pass


class OverviewerQuotes:
    NICK_MAP = {
        "achic": "achin",
        "achin_nn": "achin",
        "achin-web": "achin",
        "askelechin": "achin",
        "afrig": "agrif",
        "agrim": "agrif",
        "minaj": "agrif",
        "aheadley_": "aheadley",
        "CounterPumpkin": "CounterPillow",
        "CountPillow": "CounterPillow",
        "deadk": "edk",
        "demiurge": "edk",
        "e": "edk",
        "Tuna": "Tunabrain",
        "Tunabrainsss": "Tunabrain",
        "Tunouch": "Tunabrain",
        "node.js": None,
        "Trump": None,
    }

    def __init__(self):
        self.quotes = {}

    def read(self, filename, newline=None):
        with io.open(filename, "rt", newline=newline) as f:
            self.read_handle(f)

    def read_handle(self, f):
        for line in f:
            self.parse_line(line.rstrip("\r\n"))

    def parse_line(self, text):
        if text == "":
            return
        text = re.sub(r"\[(?:[0-9]+:)?[0-9]{2}:[0-9]{2}\] ", "", text)
        text = re.sub(r"^Guest44 has joined #overviewer  ", "", text)
        text = re.sub(r"  Guest44 has left #overviewer$", "", text)
        items = re.split("(?<! )  (?=[<*])", text)
        for item in items:
            self.parse_item(item)

    def parse_item(self, text):
        match = re.fullmatch(r"<[ @+]?(?P<nick>[^ >]+)> (?P<message>.+)", text)

        if not match:
            match = re.fullmatch(r"\* (?P<nick>[^ ]+) (?P<message>.+)", text)

        if not match:
            match = re.fullmatch(
                r"-!- [^ ]+ was kicked from #overviewer by (?P<nick>[^ ]+) \[(?P<message>.+)\]",
                text,
            )

        if not match:
            match = re.fullmatch(
                r"<-\* (?P<nick>[^ ]+) has kicked [^ ]+ from #overviewer \((?P<message>.+)\)",
                text,
            )

        if not match:
            match = re.fullmatch(
                r"(?P<nick>[^ ]+) is now known as (?P<message>[^ ]+)",
                text,
            )

        if not match:
            if (
                re.match("https:", text)
                or text == "(How Fiji got DST)"
                or re.match("<--.*quit.*Killed.*Sigyn", text)
            ):
                return

        if not match:
            raise ParseError(f"Failed to parse item: {text!r}")

        self.add_message(match.group("nick"), match.group("message"))

    def add_message(self, nick, message):
        mapped_nick = self.NICK_MAP.get(nick, nick)
        if mapped_nick != None:
            self.quotes.setdefault(mapped_nick, []).append(message)
