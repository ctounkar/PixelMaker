import random
from math import floor
from PIL import ImageDraw

# ================================================================================
def color_proximity(color, ref, sens = 0.1):
    clr_pxm = False
    
    r = (color[0] - ref[0])/ref[0]
    g = (color[1] - ref[1])/ref[1]
    b = (color[2] - ref[2])/ref[2]
    
    if abs(r) <= sens and abs(g) <= sens and abs(b) <= sens:
        clr_pxm = True
    
    return clr_pxm

# ================================================================================
def color_picker(basecolor = None, factor = 0.5, ncolor = 1):
    if basecolor:
        if ncolor == 1:
            my_color = basecolor
        else:
            my_color = []
            my_color.append(basecolor)
            for i in range(ncolor):
                acolor = []
                acolor[0] = floor(factor*basecolor[0] + (1-factor)*random.randrange(255))
                acolor[1] = floor(factor*basecolor[1] + (1-factor)*random.randrange(255))
                acolor[2] = floor(factor*basecolor[2] + (1-factor)*random.randrange(255))
                my_color.append(acolor)

    else:
        my_color = [random.randrange(255),random.randrange(255),random.randrange(255)]

    return my_color

# ================================================================================
def color_average(square, img, color = None, solid = False):
    count = 0
    pxl_avg = [0,0,0]
    for i in range(square[0], square[2], 1): # row by row
        for j in range(square[1], square[3], 1): # column by column
            pxl_r, pxl_g, pxl_b = img.getpixel((i,j))
            pxl_avg[0] += pxl_r
            pxl_avg[1] += pxl_g
            pxl_avg[2] += pxl_b
            count += 1

    if not solid:
        if color:
            new_pxl_r = ((pxl_avg[0]//count) + color[0]) // 2
            new_pxl_g = ((pxl_avg[1]//count) + color[1]) // 2
            new_pxl_b = ((pxl_avg[2]//count) + color[2]) // 2
        else:
            new_pxl_r = pxl_avg[0]//count
            new_pxl_g = pxl_avg[1]//count
            new_pxl_b = pxl_avg[2]//count
    else:
        new_pxl_r = color[0]
        new_pxl_g = color[1]
        new_pxl_b = color[2]

    return new_pxl_r, new_pxl_g, new_pxl_b

# ================================================================================
def colors_in_range(img, zone, maskname, option = 0, color = None, factor = 0.9, ncolor = 9):
    draw = ImageDraw.Draw(img)

    if maskname == 'gradient square':
        for upelt in zone:
            for elt in upelt:
                if option == 0: # pixellization without any color modification
                    my_pixel = color_average((elt[0][0],elt[0][1],elt[1][0],elt[1][1]), img)
                else: # 1 color for all zone whatever the value of options
                    my_pixel = color_average((elt[0][0],elt[0][1],elt[1][0],elt[1][1]), img, color)

                draw.rectangle(elt, fill = my_pixel)

    else:
        if option == 0: # pixellization without any color modification
            for elt in zone:
                my_pixel = color_average((elt[0][0],elt[0][1],elt[1][0],elt[1][1]), img)
                draw.rectangle(elt, fill = my_pixel)

        elif option == 1: # 1 color for all zone
            for elt in zone:
                my_pixel = color_average((elt[0][0],elt[0][1],elt[1][0],elt[1][1]), img, color)
                draw.rectangle(elt, fill = my_pixel)

        else:
            my_pixels = {} #list of colors, indexed by row or column
            my_colors = color_picker(color, factor, ncolor)

            for elt in zone:
                if option == 2: #1 color by vertical strip
                    if elt[0][0] in my_pixels.keys():
                        color = my_pixels[elt[0][0]]
                    else:
                        color = random.choice(my_colors)
                        my_pixels[elt[0][0]] = color # add element to the dict, indexed by column

                elif option == 3: #1 color by horizontal strip
                    if elt[0][1] in my_pixels.keys():
                        color = my_pixels[elt[0][1]]
                    else:
                        color = random.choice(my_colors)
                        my_pixels[elt[0][1]] = color # add element to the dict, indexed by row

                elif option == 4: #1 random color by pixel
                    color = random.choice(my_colors)

                my_pixel = color_average((elt[0][0],elt[0][1],elt[1][0],elt[1][1]),img,color)
                draw.rectangle(elt, fill = my_pixel)

    del draw

    return img
