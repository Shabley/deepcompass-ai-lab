from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

W, H = 1200, 630
out = Path('images/og-card.png')
font_bold = 'C:/Windows/Fonts/malgunbd.ttf'
font = 'C:/Windows/Fonts/malgun.ttf'

img = Image.new('RGB', (W, H), '#0D1B2E')
d = ImageDraw.Draw(img)

# gradient background
for y in range(H):
    r = int(13 + y/H * 18)
    g = int(27 + y/H * 30)
    b = int(46 + y/H * 55)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# soft circles
for xy, color in [((-180, -140, 380, 420), (0, 200, 232)), ((820, 220, 1420, 820), (201, 168, 76)), ((690, -260, 1260, 300), (30, 90, 145))]:
    layer = Image.new('RGBA', (W, H), (0,0,0,0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse(xy, fill=color + (42,))
    layer = layer.filter(ImageFilter.GaussianBlur(34))
    img = Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB')
    d = ImageDraw.Draw(img)

# left logo panel
panel = Image.new('RGBA', (360, 360), (255,255,255,235))
pd = ImageDraw.Draw(panel)
pd.rounded_rectangle((0,0,360,360), radius=44, fill=(255,255,255,235))
logo = Image.open('images/logo.png').convert('RGBA')
logo.thumbnail((250,250))
panel.alpha_composite(logo, ((360-logo.width)//2, 38))
small_font = ImageFont.truetype(font_bold, 29)
pd.text((180, 300), 'DEEP COMPASS', font=small_font, fill='#0D3B5A', anchor='mm')
img.paste(panel, (72, 135), panel)

def fit_text(text, max_width, size, min_size=28, bold=True):
    fpath = font_bold if bold else font
    while size >= min_size:
        f = ImageFont.truetype(fpath, size)
        bbox = d.textbbox((0,0), text, font=f)
        if bbox[2]-bbox[0] <= max_width:
            return f
        size -= 2
    return ImageFont.truetype(fpath, min_size)

x = 490
d.text((x, 110), 'Deep Compass AI Lab', font=ImageFont.truetype(font_bold, 38), fill='#7FD8C4')
d.text((x, 180), 'AI 시대,', font=ImageFont.truetype(font_bold, 72), fill='white')
d.text((x, 265), '방향을 아는 사람이', font=fit_text('방향을 아는 사람이', 630, 62), fill='white')
d.text((x, 345), '앞서갑니다', font=ImageFont.truetype(font_bold, 72), fill='#C9A84C')

# separator
for i in range(4):
    d.line((x, 444+i, 1090, 444+i), fill=(127,216,196,90))

d.text((x, 478), '딥컴퍼스AI연구소 | 고연심 소장', font=ImageFont.truetype(font_bold, 38), fill='white')
d.text((x, 535), '생성형 AI · AI 프롬프트 · AI 에이전트 실무 교육', font=ImageFont.truetype(font, 28), fill='#DDEAF2')

out.parent.mkdir(exist_ok=True)
img.save(out, quality=95)
print(out)
