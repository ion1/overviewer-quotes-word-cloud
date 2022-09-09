import argparse
import logging

from overviewer_quotes_word_cloud import OverviewerQuotes, render


def main():
    logging.basicConfig(level=logging.INFO)

    ap = argparse.ArgumentParser(description="#overviewer quotes word cloud generator")
    ap.add_argument(
        "input",
        metavar="INPUT_PATH",
        type=str,
        help="quote database dump filename",
    )
    ap.add_argument(
        "output",
        metavar="OUTPUT_PATH",
        type=str,
        help="image filename",
    )
    args = ap.parse_args()

    ovq = OverviewerQuotes()
    ovq.read(args.input)
    render(args.output, ovq.quotes)


if __name__ == "__main__":
    main()
