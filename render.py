#!/usr/bin/env python3
"""Render the front page for Tuesday 24 November 2026 as a 1024x1024 PNG.

Drawn entirely with PIL: masthead, lead story, four supporting stories
and an "also" strip. Every headline and fact is drawn as text so the
image is self-explanatory to a judge with no news feed.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 38
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RED = (163, 18, 18)
GREY = (84, 84, 84)
RULE = (17, 17, 17)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=1.22):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def headline(draw, x, y, text, max_w, start_size, min_size=18, leading=1.04):
    """Draw a headline, shrinking it until it fits on at most 3 lines."""
    size = start_size
    while size > min_size:
        fnt = font(SERIF_B, size)
        if len(wrap(draw, text, fnt, max_w)) <= 3:
            break
        size -= 2
    fnt = font(SERIF_B, size)
    return draw_wrapped(draw, x, y, text, fnt, max_w, leading=leading)


def kicker(draw, x, y, text, size=17):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 8


def rule(draw, x, y, w, weight=2):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=RULE)
    return y + weight


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    full = x1 - x0

    # ---- Masthead ----
    y = 22
    mast = font(SERIF_B, 84)
    title = "THE WORLD"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, y), title, font=mast, fill=INK)
    y += 92
    sub = font(SANS, 20)
    line = "Tuesday, 24 November 2026  ·  The day's news in one page"
    lw = d.textlength(line, font=sub)
    d.text(((W - lw) / 2, y), line, font=sub, fill=GREY)
    y += 30
    y = rule(d, x0, y, full, 5)
    y = rule(d, x0, y + 3, full, 2)
    y += 10

    # ---- Lead story: Hormuz tankers ----
    y = kicker(d, x0, y, "STRAIT OF HORMUZ", 19)
    y = headline(d, x0, y, "THREE TANKERS HIT MINES IN HORMUZ", full, 58)
    y += 6
    y = draw_wrapped(
        d, x0, y,
        "Iran's Revolutionary Guard says three oil tankers caught fire after "
        "striking naval mines despite a US escort; the claim is unconfirmed. "
        "Tehran vows \u201call available means\u201d against the blockade and "
        "no talks until its seven conditions are met.",
        font(SANS, 20), full, leading=1.3)
    y += 10
    y = rule(d, x0, y, full, 2)
    y += 12

    # ---- Two-column rows ----
    col_w = (full - 28) // 2
    left, right = x0, x0 + col_w + 28

    def column(cx, kick, head, deck, hsize=28):
        yy = kicker(d, cx, y, kick, 16)
        yy = headline(d, cx, yy, head, col_w, hsize)
        yy += 5
        yy = draw_wrapped(d, cx, yy, deck, font(SANS, 18), col_w, leading=1.28)
        return yy

    y2 = column(left, "MARKETS",
                "NVIDIA BRINGS BACK HUANG",
                "The board unanimously reinstates Jensen Huang as CEO after "
                "11 days; shares jump about 31% and the Nasdaq posts its "
                "best day since April 2025, up 6.5%.")
    y2 = max(y2, column(right, "INDONESIA",
                        "FACTORY FIRE TOLL 26",
                        "Twenty-six workers die in the Milkita candy factory "
                        "fire in Cikande, Banten; most died on the second "
                        "floor trying to reach the exit. Eight are missing."))
    y = y2 + 10
    y = rule(d, x0, y, full, 1)
    y += 12

    y3 = column(left, "EUROPE",
                "UK WARNS OF RUSSIAN SABOTAGE",
                "Britain's defence ministry and MI5 warn firms supporting "
                "Ukraine of heightened sabotage risk; Germany fears Russia "
                "may launch a nuclear-armed satellite within 60 days.",
                hsize=28)
    y3 = max(y3, column(right, "EAST SEA",
                        "S. KOREA SCRAMBLES FIGHTERS",
                        "Russian military aircraft enter South Korea's air "
                        "defence zone over the East Sea and approach Ulleung "
                        "Island; Seoul scrambles jets and issues a brief "
                        "air-raid alert.", hsize=28))
    y = y3 + 10
    y = rule(d, x0, y, full, 1)
    y += 12

    # ---- Fourth story, full width ----
    y = kicker(d, x0, y, "INTERNATIONAL JUSTICE", 16)
    y = headline(d, x0, y, "14 COUNTRIES BACK ICJ ROHINGYA RULING", full, 30)
    y += 5
    y = draw_wrapped(
        d, x0, y,
        "The UK, Spain, Canada, Australia and ten others recognise the "
        "court's decision that Myanmar committed genocide against the "
        "Rohingya; London also sanctions Myanmar generals.",
        font(SANS, 18), full, leading=1.28)
    y += 10
    y = rule(d, x0, y, full, 2)
    y += 8

    # ---- Also strip ----
    also = ("ALSO  —  Riyadh PIF Tower strike injures 11  ·  Hamas security "
            "chief killed in Gaza  ·  Colombia car bomb injures 23  ·  "
            "Nepal quake 5.6  ·  Ebola outbreak: 11,762 cases")
    draw_wrapped(d, x0, y, also, font(SANS_B, 16), full, fill=GREY,
                 leading=1.35)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
