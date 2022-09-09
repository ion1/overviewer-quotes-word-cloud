import logging
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud, STOPWORDS
from wordcloud.wordcloud import FONT_PATH

__all__ = ["render"]


def render(filename, quotes):
    logger = logging.getLogger("overviewer_quotes")

    # <NachoIn> no, achin
    stopwords = list(set(STOPWORDS) - set(["no"]))

    width = 400
    height = 200
    label_height = 40
    padding_height = 20

    count = len(quotes)
    total_height = (label_height + height) * count + padding_height * (count - 1)

    img = Image.new("RGB", (width, total_height), "black")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, label_height)

    y = 0
    for nick, messages in sorted(quotes.items(), key=lambda i: str.lower(i[0])):
        logger.info(f"Rendering word cloud: {nick}")

        draw.text((0, y), nick, fill="white", font=font, anchor="lt")

        wc = WordCloud(
            stopwords=stopwords,
            include_numbers=True,
            width=width,
            height=height,
            scale=1,
        )
        wc.generate(" ".join(messages))
        img.paste(wc.to_image(), (0, y + label_height))

        y += label_height + height + padding_height

    logger.info(f"Saving image: {filename}")
    img.save(filename)
