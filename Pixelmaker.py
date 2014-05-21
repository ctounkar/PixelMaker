import random
from PIL import Image, ImageDraw
from fractions import gcd
from functools import reduce

# List of basic functions
def iter_frames(img):
    try:
        i= 0
        while 1:
            img.seek(i)
            imframe = img.copy()
            if i == 0: 
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass
    
# ================================================================================  
def fgcd(vala,valb):
    val = gcd(vala,valb)
    factors = reduce(list.__add__, ([i, val//i] for i in range(1, int(val**0.5) + 1) if val % i == 0))
    factors.sort()
    if len(factors) > 1:
        del factors[0] # first factor is always 1
    
    return factors

# ================================================================================
def pixellize(my_img, step, option = 0): 
    img = my_img.convert('RGB')
    
    width = img.size[0]
    height = img.size[1]
    
    my_count = step ** 2
    
    new_img = Image.new('RGB', (width,height))
    draw = ImageDraw.Draw(new_img)
    
    if option not in [0,1,2,3]:
        option = 0 # while waiting for a proper error handling
    
    if option == 1:
        factor = [random.randrange(255),random.randrange(255),random.randrange(255)]
    
    pxl_avg = [0,0,0]
    
    for i in range(0,height,step): # row by row
        if option == 2:
            factor = [random.randrange(255),random.randrange(255),random.randrange(255)]
                     
        for j in range(0,width,step): # column by column
            if option == 3:
                factor = [random.randrange(255),random.randrange(255),random.randrange(255)]
            
            # Iterate through the block to find color average
            for k in range(i,i+step,1): 
                for p in range(j,j+step,1):
                    pxl_r, pxl_g, pxl_b = img.getpixel((p,k))
                    pxl_avg [0] += pxl_r
                    pxl_avg [1] += pxl_g
                    pxl_avg [2] += pxl_b
            
            if option == 0:
                new_pxl_r = pxl_avg[0]//my_count
                new_pxl_g = pxl_avg[1]//my_count
                new_pxl_b = pxl_avg[2]//my_count
            else:
                new_pxl_r = ((pxl_avg[0]//my_count) + factor[0]) // 2
                new_pxl_g = ((pxl_avg[1]//my_count) + factor[1]) // 2
                new_pxl_b = ((pxl_avg[2]//my_count) + factor[2]) // 2
                
            # my block = 1 pixel
            my_pixel = (new_pxl_r, new_pxl_g, new_pxl_b)
            #print(my_pixel)
            my_block = [(j,i),(j+step,i+step)]
            draw.rectangle(my_block, fill = my_pixel)
            
            pxl_avg = [0,0,0]
            
    del draw
       
    return new_img

# ================================================================================
def pixellize_multi(img,option=0):
    width = img.size[0]
    height = img.size[1]
    factor = fgcd(width,height)
    
    new_width = width * len(factor)
    new_height = height
    new_img = Image.new('RGB', (new_width, new_height))
    
    i = 0
    
    for step in factor:
        new_box = (i*width,0)
        new_img.paste(pixellize(img,step,option),new_box)
        i +=1
        
    return new_img


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
