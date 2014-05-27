# http://www.pygame.org/wiki/FastPixelPerfect

def get_alpha_hitmask(image, alpha=0):
    """returns a hitmask using an image's alpha.
       image->pygame Surface,
       alpha->the alpha amount that is invisible in collisions"""
    rect=image.get_rect()
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for y in range(rect.height):
            mask[x].append(not image.get_at((x,y))[3]==alpha)
    return mask

def get_full_hitmask(rect):
    """returns a completely full hitmask that fits the image,
       without referencing the images colorkey or alpha."""
    mask=[]
    for x in range(rect.width):
        mask.append([])
        for __y in range(rect.height):
            mask[x].append(True)
    return mask

def PPCollision(obj1,obj2):
    """checks if two objects have collided, using hitmasks"""
    rect1=obj1.rect
    rect2=obj2.rect
    hm1=obj1.hitmask
    hm2=obj2.hitmask
    
    rect=rect1.clip(rect2)
    if rect.width==0 or rect.height==0:
        return False
    
    # bug: (a veces) IndexError: list index out of range
    #print(str(rect)+" , "+str(rect1)+" , "+str(rect2))
    
    x1=rect.x-rect1.x   # 128-111
    y1=rect.y-rect1.y   # 438-438
    x2=rect.x-rect2.x   # 128-128
    y2=rect.y-rect2.y   # 438-416    por ej.
    
    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hm1[x1+x][y1+y] and hm2[x2+x][y2+y]:
                return True
    return False