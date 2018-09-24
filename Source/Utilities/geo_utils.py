def getrandom_id():
    random.seed()
    id = random.randrange(999999999999)
    return id


def random_color(id):
    random.seed(id+6843651)
    r = random.random()
    random.seed(id+9844318)
    g = random.random()
    random.seed(id+21684651)
    b = random.random()
    rgb = (r,g,b)
    return rgb


def set_polycolor(geo, color):
    mc.setAttr(geo + '.displayColors', 1)
    mc.polyOptions(geo, cm='diffuse')
    mc.polyColorPerVertex(geo, rgb=color)


def set_curvecolor(curveShape, color):
    mc.setAttr(curveShape + '.overrideEnabled', 1)
    mc.setAttr(curveShape + '.overrideRGBColors', 1)
    mc.setAttr(curveShape + '.overrideColorRGB', color[0], color[1], color[2])


def set_randomGeoColor(geo, seed):
    color = random_color(seed)
    set_polycolor(geo, color)


def clean(geo):
    mc.delete(geo, ch=True, icn=True)
    mc.xform(cp=True, ztp=True)
    return geo