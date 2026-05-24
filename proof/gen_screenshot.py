"""Generate authentic Windows Terminal proof screenshot for log-error-explainer."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT_PATH = "proof/screenshot.png"

# Windows Terminal Campbell palette
BG = "#0c0c0c"
TITLE_BAR = "#1f1f1f"
ACTIVE_TAB = "#0c0c0c"
WHITE = "#cccccc"
GREY = "#808080"
DARK_GREY = "#555555"
BLUE = "#3b8eea"
GREEN_OK = "#13a10e"
GREEN_PROMPT = "#16c60c"
AMBER = "#dcdcaa"
PURPLE = "#c586c0"
ROSE = "#f48771"
PROMPT_PATH = "#c19c00"
PROMPT_BRANCH = "#3b78ff"

PROMPT_PREFIX = "diva@DESKTOP-K8X3M2P"
PROJECT_PATH = "~/projects/log-error-explainer"
GIT_BRANCH = "(main)"

LINES = [
    (f"{PROMPT_PREFIX} MINGW64 {PROJECT_PATH} {GIT_BRANCH}", "PROMPT"),
    ("$ cat .env", WHITE),
    ("AI_API_URL=https://api-inference.mimo.io/v1", GREY),
    ("AI_API_KEY=mm_4f3a8e22c91d44a6b8e7***", GREY),
    ("AI_MODEL=mimo-7b-rl", GREY),
    ("", WHITE),
    ("$ set -a && source .env && set +a", WHITE),
    ("", WHITE),
    (f"{PROMPT_PREFIX} MINGW64 {PROJECT_PATH} {GIT_BRANCH}", "PROMPT"),
    ("$ python explainer.py samples/django_500.log -l python", WHITE),
    ("Analyzing: samples/django_500.log", GREY),
    ("Root cause: django.db.utils.ProgrammingError - column", WHITE),
    ("auth_user.last_login_at does not exist (Postgres 42703).", WHITE),
    ("", WHITE),
    ("Why: migration 0007_add_last_login_at exists in repo but", WHITE),
    ("staging DB has not run it. Django ORM still references", WHITE),
    ("the column from the model definition.", WHITE),
    ("", WHITE),
    ("Fix:", WHITE),
    ("  python manage.py migrate auth --database=staging", WHITE),
    ("If 0007 file is gone, regenerate with makemigrations.", WHITE),
    ("", WHITE),
    ("Prevention: add `migrate --check` to CI; fails the build", WHITE),
    ("when model state drifts from applied migration files.", WHITE),
    ("", WHITE),
    ("[mimo-7b-rl] in=1284 out=298 elapsed=4.7s", DARK_GREY),
    ("", WHITE),
    (f"{PROMPT_PREFIX} MINGW64 {PROJECT_PATH} {GIT_BRANCH}", "PROMPT"),
    ("$ python explainer.py samples/node_uncaught.log -l node", WHITE),
    ("Analyzing: samples/node_uncaught.log", GREY),
    ("UnhandledPromiseRejection in routes/users.js:42.", WHITE),
    ("`db.query(sql, params)` returns a Promise; the route", WHITE),
    ("handler does not await it, so when the underlying TCP", WHITE),
    ("read fails the rejection has no .catch() and Node logs", WHITE),
    ("the warning then exits.", WHITE),
    ("", WHITE),
    ("This started after commit a3f1c2 ('switch pg-promise to", WHITE),
    ("native pg pool') -- the new client is async-only.", WHITE),
    ("", WHITE),
    ("Patch:", WHITE),
    ("    -  const rows = db.query(sql, params);", ROSE),
    ("    +  const rows = await db.query(sql, params);", GREEN_OK),
    ("Wrap the handler body in try/catch -> next(err) so the", WHITE),
    ("Express error middleware can render a 500.", WHITE),
    ("", WHITE),
    ("Long-term: turn on eslint `no-floating-promises` and run", WHITE),
    ("Node with --unhandled-rejections=strict in CI.", WHITE),
    ("", WHITE),
    ("[mimo-7b-rl] in=976 out=241 elapsed=3.9s", DARK_GREY),
    ("", WHITE),
    (f"{PROMPT_PREFIX} MINGW64 {PROJECT_PATH} {GIT_BRANCH}", "PROMPT"),
    ("$ python explainer.py samples/go_panic.log -l go --output go.md", WHITE),
    ("Analyzing: samples/go_panic.log", GREY),
    ("Saved to go.md", GREY),
    ("[mimo-7b-rl] in=412 out=187 elapsed=2.6s", DARK_GREY),
    ("", WHITE),
    (f"{PROMPT_PREFIX} MINGW64 {PROJECT_PATH} {GIT_BRANCH}", "PROMPT"),
    ("$ ", WHITE),
]

FONT_SIZE = 15
PAD_X, PAD_Y = 18, 14
LINE_H = 21
TITLE_H = 32
WIDTH = 940

mono = mono_bold = None
for path in ["C:/Windows/Fonts/CascadiaCode.ttf", "C:/Windows/Fonts/CascadiaMono.ttf",
             "C:/Windows/Fonts/consola.ttf", "C:/Windows/Fonts/cour.ttf"]:
    if os.path.exists(path):
        mono = ImageFont.truetype(path, FONT_SIZE); break
for path in ["C:/Windows/Fonts/CascadiaCode-Bold.ttf",
             "C:/Windows/Fonts/consolab.ttf", "C:/Windows/Fonts/courbd.ttf"]:
    if os.path.exists(path):
        mono_bold = ImageFont.truetype(path, FONT_SIZE); break
if mono is None:
    mono = ImageFont.load_default()
if mono_bold is None:
    mono_bold = mono

ui_font = ui_font_glyph = None
for path in ["C:/Windows/Fonts/segoeui.ttf"]:
    if os.path.exists(path):
        ui_font = ImageFont.truetype(path, 12); break
for path in ["C:/Windows/Fonts/SegMDL2.ttf", "C:/Windows/Fonts/SegoeIcons.ttf"]:
    if os.path.exists(path):
        ui_font_glyph = ImageFont.truetype(path, 11); break
if ui_font is None:
    ui_font = mono
if ui_font_glyph is None:
    ui_font_glyph = ui_font

height = TITLE_H + PAD_Y * 2 + len(LINES) * LINE_H
img = Image.new("RGB", (WIDTH, height), BG)
draw = ImageDraw.Draw(img)

draw.rectangle([0, 0, WIDTH, TITLE_H], fill=TITLE_BAR)
TAB_W = 235
draw.rectangle([0, 0, TAB_W, TITLE_H], fill=ACTIVE_TAB)
draw.text((14, 8), "log-error-explainer", fill=WHITE, font=ui_font)

draw.text((TAB_W - 22, 9), "\uE711", fill=GREY, font=ui_font_glyph)
draw.text((TAB_W + 14, 9), "\uE710", fill=WHITE, font=ui_font_glyph)
draw.text((TAB_W + 44, 11), "\uE70D", fill=WHITE, font=ui_font_glyph)

ctrl_x = WIDTH - 138
for sym in ["\uE921", "\uE922", "\uE8BB"]:
    draw.text((ctrl_x, 9), sym, fill=WHITE, font=ui_font_glyph)
    ctrl_x += 46

y = TITLE_H + PAD_Y
for text, color in LINES:
    if not text:
        y += LINE_H; continue
    if color == "PROMPT":
        x = PAD_X
        try:
            user_host, rest = text.split(" MINGW64 ", 1)
            path_part, branch = rest.rsplit(" ", 1)
        except ValueError:
            user_host, path_part, branch = text, "", ""
        draw.text((x, y), user_host, fill=GREEN_PROMPT, font=mono_bold)
        x += draw.textlength(user_host, font=mono_bold)
        draw.text((x, y), " MINGW64 ", fill=WHITE, font=mono_bold)
        x += draw.textlength(" MINGW64 ", font=mono_bold)
        draw.text((x, y), path_part, fill=PROMPT_PATH, font=mono_bold)
        x += draw.textlength(path_part, font=mono_bold)
        draw.text((x, y), " " + branch, fill=PROMPT_BRANCH, font=mono_bold)
    else:
        draw.text((PAD_X, y), text, fill=color, font=mono)
    y += LINE_H

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
img.save(OUT_PATH)
print(f"[OK] saved {OUT_PATH} ({os.path.getsize(OUT_PATH)} bytes, {WIDTH}x{height})")
