# Renders the paper figures to static/images/. Run from the website/ folder: python layoutrecall.github.io/scripts/render_figures.py
import pymupdf, sys
from PIL import Image
import io
CM = 72/2.54
jobs = [  # pdf, page, trim (l b r t) in bp, out
 ("paper/figures/fig_teaser.pdf", 0, (0,288,60.5,0), "teaser"),
 ("paper/figures/figures_paper.pdf", 0, (0,128.5,189.5,0), "method"),
 ("paper/figures/fig5.pdf", 0, (0,0,0,0), "multiround"),
 ("paper/figures/supp_mr.pdf", 0, (0,0,2*CM,0), "multiround_supp"),
]
for pdf, pg, (l,b,r,t), out in jobs:
    doc = pymupdf.open(pdf); p = doc[pg]; R = p.rect
    clip = pymupdf.Rect(R.x0+l, R.y0+t, R.x1-r, R.y1-b)
    zoom = 2600/clip.width
    pix = p.get_pixmap(matrix=pymupdf.Matrix(zoom,zoom), clip=clip, alpha=False)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    from PIL import ImageChops
    g = ImageChops.difference(im, Image.new("RGB", im.size, (255,255,255))).convert("L").point(lambda v: 255 if v>12 else 0)
    x0,y0,x1,y1 = g.getbbox(); pad=12
    im = im.crop((max(0,x0-pad),max(0,y0-pad),min(im.width,x1+pad),min(im.height,y1+pad)))
    if im.width>2400: im = im.resize((2400, round(im.height*2400/im.width)), Image.LANCZOS)
    path = f"layoutrecall.github.io/static/images/{out}.jpg"
    im.save(path, quality=88, optimize=True, progressive=True)
    print(out, R, len(doc), im.size)
