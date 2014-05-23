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
    width = my_img.size[0]
    height = my_img.size[1]
    draw = ImageDraw.Draw(my_img)
    
    if option not in [0,1,2,3,4]:
        option = 0 # while waiting for a proper error handling
    
    if option == 0:
        factor = [0,0,0]
        for i in range(0,height,step): # row by row        
            for j in range(0,width,step):
                my_block = (i,j,i+step,j+step)
                my_pixel = color_pixel(my_block, my_img, factor)
                draw.rectangle(my_block, fill = my_pixel)
                
        
    elif option == 1:
        factor = [random.randrange(255),random.randrange(255),random.randrange(255)]
        for i in range(0,height,step): # row by row        
            for j in range(0,width,step):
                my_block = (i,j,i+step,j+step)
                my_pixel = color_pixel(my_block, my_img, factor)
                draw.rectangle(my_block, fill = my_pixel)
    
    elif option == 2:
        for i in range(0,height,step): # row by row        
            factor = [random.randrange(255),random.randrange(255),random.randrange(255)]
            for j in range(0,width,step):
                my_block = (i,j,i+step,j+step)
                my_pixel = color_pixel(my_block, my_img, factor)
                draw.rectangle(my_block, fill = my_pixel)
                             
    elif option == 3:
        for j in range(0,width,step): # column by column
            factor = [random.randrange(255),random.randrange(255),random.randrange(255)]
            for i in range(0,height,step):
                my_block = (i,j,i+step,j+step)
                my_pixel = color_pixel(my_block, my_img, factor)
                draw.rectangle(my_block, fill = my_pixel)
                
    del draw

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
def choose_factor(a,b):
    ## Ask user to provide a pixellization factor
    list_factor = fgcd(a,b)
    while len(list_factor) < 2:
        a -= 1
        list_factor = fgcd(a,b)
        
    factor_in = False
    
    while not factor_in:
        print('Veuillez choisir la taille de votre pixel : ', str(list_factor))
        try:
            factor = int(input())
            factor_in = (factor in list_factor)
            if not factor_in:
                print("cette valeur n'est pas dans la liste")
        except ValueError:
            print("Ceci n'est pas une entrée valide")
        pass          
    
    return factor
        

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
