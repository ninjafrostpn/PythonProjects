import pygame, os
from fpdf import FPDF
pygame.init()

tagpath = "D:\\Users\\Charles Turvey\\Documents\\SRobo\\SourceBots\\AprilTags\\New\\SB-AprilTags\\SB-AprilTags\\tag36_11_"
fontpath = "D:\\Users\\Charles Turvey\\Documents\\Python\\Projects\\OpenSans-Regular.ttf"
papertypes = {"A4": (297, 210), "A3": (420, 297), "SQUARE": (100, 100)}
presets = {"LARGE": ["A3 page with 25cm marker", 5, "A3", 25],
           "SMALL": ["A4 page with 10cm marker", 5, "A4", 10],
           "SQUARE": ["Just markers (does not produce PDF)", 5, "SQUARE", 10]}

pageset = 0

while True:
    preset = input("Select preset or build custom:\n%s\nCUSTOM\n-Select the parameters separately\n>> " %
                   "\n".join(["%s\n-%s" % (i, presets[i][0]) for i in list(presets.keys())])).upper()
    
    if preset not in list(presets.keys()):
        mmscalein = input("Scale (Pixels per mm)\n>> ")
        mmscale = int(mmscalein)
        papertype = input("Paper type\nOne from: %s\n>> " % ", ".join(list(papertypes.keys()))).upper()
        dims = papertypes[papertype]
        w = dims[0] * mmscale
        h = dims[1] * mmscale
        if papertype == "SQUARE":
            tagedge = w
        else:
            tagedgein = input("Side length of Tag, in cm\n>> ")
            tagedge = int(float(tagedgein) * mmscale * 10)
    else:
        preset = presets[preset]
        mmscale = preset[1]
        papertype = preset[2]
        dims = papertypes[papertype]
        w = dims[0] * mmscale
        h = dims[1] * mmscale
        tagedge = int(preset[3] * mmscale * 10)
    
    if papertype != "SQUARE":
        textfont = pygame.font.Font(fontpath, 15 * mmscale)
    
    page = pygame.Surface((w, h))
    
    while True:
        taginput = input("Tag Numbers\nComma-separated single numbers or inclusive ranges of form a-b\n>> ")
        if taginput == "":
            break
        tagnos = [i for i in taginput.split(",")]
        tags = []
        
        if papertype != "SQUARE":
            pdf = FPDF(orientation="L", format=papertype)
            
        i = 0
        while i < len(tagnos):
            tagno = tagnos[i]
            if "-" in tagno:
                fromno, tono = tagno.split("-")
                nos = [j for j in range(int(fromno), int(tono) + 1)]
                nos.reverse()
                tagnos.remove(tagno)
                for no in nos:
                    tagnos.insert(i, str(no))
            else:
                tags.append(pygame.transform.scale(pygame.image.load_extended(tagpath + "%05d.png" % (int(tagno))),
                                                   (tagedge, tagedge)))
                i += 1
            
        lft = int((w - tagedge)/2)
        top = int((h - tagedge)/2)
        rgt = int((w + tagedge)/2)
        btm = int((h + tagedge)/2)
        
        while os.path.exists("Set%03d\\" % pageset):
            pageset += 1

        os.makedirs("Set%03d\\" % pageset, exist_ok=True)
        for i in range(len(tags)):
            page.fill((255, 255, 255))
            page.blit(tags[i], (lft, top))
            if w != tagedge:
                pygame.draw.line(page, 0, (lft, top), (lft, btm))
                pygame.draw.line(page, 0, (rgt, top), (rgt, btm))
            if h != tagedge:
                pygame.draw.line(page, 0, (lft, top), (rgt, top))
                pygame.draw.line(page, 0, (lft, btm), (rgt, btm))
            if papertype != "SQUARE":
                number = textfont.render("- %s -" % tagnos[i], 0, (0,0,0))
                page.blit(number, ((w - number.get_width())/2, btm))
            pygame.image.save(page, "Set%03d\\%s(Tag%s).png" % (pageset, i, tagnos[i]))
            if papertype != "SQUARE":
                pdf.add_page()
            pdf.image("Set%03d\\%s(Tag%s).png" % (pageset, i, tagnos[i]), 0, 0, dims[0], dims[1])
        if papertype != "SQUARE":
            pdf.output("Set%03d\\Tags.pdf" % pageset, "F")
        pageset += 1
