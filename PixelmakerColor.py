import random
from PIL import ImageDraw
from Pixelmaker.PixelmakerRange import squares_in_range

# ================================================================================
def color_pixel(square, img, color):
    i = 0
    j = 0
    count = 0
    pxl_avg = [0,0,0]
    for i in range(square[0],square[2],1): # row by row 
        for j in range(square[1],square[3],1): # column by column
            pxl_r, pxl_g, pxl_b = img.getpixel((i,j))
            pxl_avg [0] += pxl_r
            pxl_avg [1] += pxl_g
            pxl_avg [2] += pxl_b
            count += 1

    if color != [0,0,0]:            
        new_pxl_r = ((pxl_avg[0]//count) + color[0]) // 2
        new_pxl_g = ((pxl_avg[1]//count) + color[1]) // 2
        new_pxl_b = ((pxl_avg[2]//count) + color[2]) // 2
    else:
        new_pxl_r = pxl_avg[0]//count
        new_pxl_g = pxl_avg[1]//count
        new_pxl_b = pxl_avg[2]//count
    
    return (new_pxl_r, new_pxl_g, new_pxl_b)

# ================================================================================
def colors_in_range(img, mask, option = 0):
    draw = ImageDraw.Draw(img)
    zone = squares_in_range(img, mask) 
    
    if option == 0: # 1 color for all zone
        color = [0,0,0]
        for elt in zone:
            my_pixel = color_pixel((elt[0][0],elt[0][1],elt[1][0],elt[1][1]),img,color)
            draw.rectangle(elt, fill = my_pixel)
    else:
        if mask['type'] == 'gradient square':
            for upelt in zone:
                color = [random.randrange(255),random.randrange(255),random.randrange(255)]
                for elt in upelt:
                    my_pixel = color_pixel((elt[0][0],elt[0][1],elt[1][0],elt[1][1]),img,color)
                    draw.rectangle(elt, fill = my_pixel)
                        
        else:
            if option == 1: # 1 color for all zone
                color = [random.randrange(255),random.randrange(255),random.randrange(255)]
                for elt in zone:
                    my_pixel = color_pixel((elt[0][0],elt[0][1],elt[1][0],elt[1][1]),img,color)
                    draw.rectangle(elt, fill = my_pixel)
    
            elif option == 2: #1 color by vertical strip
                column = {}
                color = [0,0,0]
                for elt in zone:
                    if elt[0][0] in column.keys():
                        color = column[elt[0][0]]
                    else:
                        color = [random.randrange(255),random.randrange(255),random.randrange(255)]
                        column[elt[0][0]] = color
                        
                    my_pixel = color_pixel((elt[0][0],elt[0][1],elt[1][0],elt[1][1]),img,color)
                    draw.rectangle(elt, fill = my_pixel)
                                
            elif option == 3: #1 color by horizontal strip
                row = {}
                color = [0,0,0]
                for elt in zone:
                    if elt[0][1] in row.keys():
                        color = row[elt[0][1]]
                    else:
                        color = [random.randrange(255),random.randrange(255),random.randrange(255)]
                        row[elt[0][1]] = color
                        
                    my_pixel = color_pixel((elt[0][0],elt[0][1],elt[1][0],elt[1][1]),img,color)
                    draw.rectangle(elt, fill = my_pixel)
                                
            elif option == 4: #1 color by pixel
                for elt in zone:
                    color = [random.randrange(255),random.randrange(255),random.randrange(255)]
                    my_pixel = color_pixel((elt[0][0],elt[0][1],elt[1][0],elt[1][1]),img,color)
                    draw.rectangle(elt, fill = my_pixel)            
    
    del draw
