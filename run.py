import logging

from overviewer_quotes_word_cloud import OverviewerQuotes, render


def main():
    logging.basicConfig(level=logging.INFO)

    ovq = OverviewerQuotes()
    ovq.read("20220908_IRCQuotes.cleaned-up.txt")
    render("overviewer_quotes_word_cloud.png", ovq.quotes)


if __name__ == "__main__":
    main()
