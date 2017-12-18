import pygame

tagpath = "D:\\Users\\Charles Turvey\\Documents\\SRobo\\SourceBots\\AprilTags\\New\\SB-AprilTags\\SB-AprilTags\\tag36_11_"
papertypes = {"A4":(210, 297), "A3":(297, 420), "SQUARE":(100, 100)}

pageset = 0

while True:
    mmscalein = input("Scale (Pixels per mm)\n>> ")
    mmscale = int(mmscalein)
    
    while True:
        papertype = input("Paper type\nOne from: %s\n>> " % ", ".join(list(papertypes.keys()))).upper()
        
        if papertype == "":
            break
        
        dims = papertypes[papertype]
        w = dims[1] * mmscale
        h = dims[0] * mmscale
        
        if papertype == "SQUARE":
            tagedge = w
        else:
            tagedgein = input("Side length of Tag, in cm\n>> ")
            if tagedgein == "":
                break
            tagedge = int(float(tagedgein) * mmscale * 10)
        
        page = pygame.Surface((w, h))
        
        while True:
            tagnos = [i for i in input("Tag Numbers (comma-separated)\n>> ").split(",")]
            tags = []
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
                    tags.append(pygame.transform.scale(pygame.image.load_extended(tagpath + "%05d.png" %(int(tagno))),
                                                       (tagedge, tagedge)))
                    i += 1
                
            lft = int((w - tagedge)/2)
            top = int((h - tagedge)/2)
            rgt = int((w + tagedge)/2)
            btm = int((h + tagedge)/2)
            print(lft, top, rgt, btm)
            
            for i in range(len(tags)):
                tag = tags[i]
                page.fill((255, 255, 255))
                page.blit(tag, (lft, top))
                if w != tagedge:
                    pygame.draw.line(page, 0, (lft, top), (lft, btm))
                    pygame.draw.line(page, 0, (rgt, top), (rgt, btm))
                if h != tagedge:
                    pygame.draw.line(page, 0, (lft, top), (rgt, top))
                    pygame.draw.line(page, 0, (lft, btm), (rgt, btm))
                pygame.image.save(page, "D:\\Users\\Charles Turvey\\Documents\\SRobo\\SourceBots\\SB2018\\microgames\\%s-%s.png" % (pageset, i))
            pageset += 1
