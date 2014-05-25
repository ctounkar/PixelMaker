import random
from PIL import ImageDraw
from Pixelmaker.PixelmakerLines import inclined_range, between_bars
from Pixelmaker.PixelmakerGeometry import circle_range, square_range

# ================================================================================
# functions ---------------
# ================================================================================
def squares_in_range(img, mask):
    i = 0
    my_area = []
    my_block = [(0, 0), (0, 0)]
    #------------------------------------------------------------------------------
    if mask['type'] == 'circle':
        step = mask['step']
        xstep = img.size[0]//step
        ystep = img.size[1]//step
        for i in range(0,xstep,1):
            for j in range(0,ystep,1):
                if circle_range(((i+1/2)*step, (j+1/2)*step), mask['center'], mask['radius']):
                    topx = max(0, i*step)
                    topy = max(0, j*step)
                    botx = min(img.size[0], (i + 1)*step)
                    boty = min(img.size[1], (j + 1)*step)
                    my_block = [(topx, topy), (botx, boty)]
    #------------------------------------------------------------------------------
    if mask['type'] == 'ring':
        step = mask['step']
        xstep = img.size[0]//step
        ystep = img.size[1]//step
        for i in range(0,xstep,1):
            for j in range(0,ystep,1):
                test_inner = circle_range(((i+1/2)*step, (j+1/2)*step), mask['center'], mask['radius'],'out')
                test_outer = circle_range(((i+1/2)*step, (j+1/2)*step), mask['center'], mask['radius'] + mask['width'],'in')
                if test_inner and test_outer:
                    topx = max(0, i*step)
                    topy = max(0, j*step)
                    botx = min(img.size[0], (i + 1)*step)
                    boty = min(img.size[1], (j + 1)*step)
                    my_block = [(topx, topy), (botx, boty)]
                    my_area.append(my_block)
                    my_area.append(my_block)
    
    #------------------------------------------------------------------------------
    if mask['type'] == 'bande':
        step = mask['step']
        xstep = img.size[0]//step
        ystep = img.size[1]//step
        
        if mask['orientation'] == 0 or mask['orientation'] == 180:
            # bande horizontale
            for j in range(0,ystep,1):
                if j*step >= mask['start'] and j*step <= (mask['start']+mask['width']):
                    for i in range(0,xstep,1):
                        topx = i*step
                        topy = j*step
                        botx = (i + 1)*step
                        boty = (j + 1)*step
                        my_block = [(topx, topy), (botx, boty)]
                        my_area.append(my_block)
        
        elif mask['orientation'] == 90:
            # bande verticale
            for i in range(0,xstep,1):
                if i*step >= mask['start'] and i*step <= (mask['start']+mask['width']):
                    for j in range(0,ystep,1):
                        topx = i*step
                        topy = j*step
                        botx = (i + 1)*step
                        boty = (j + 1)*step
                        my_block = [(topx, topy), (botx, boty)]
                        my_area.append(my_block)
        
        else:
            for i in range(0,xstep,1):
                for j in range(0,ystep,1):
                    if between_bars((i*step,j*step), mask['start'], mask['start']+mask['width'], mask['orientation']):
                        topx = i*step
                        topy = j*step
                        botx = (i + 1)*step
                        boty = (j + 1)*step
                        my_block = [(topx, topy), (botx, boty)]
                        my_area.append(my_block)
    
    #------------------------------------------------------------------------------
    if mask['type'] == 'couteau':
        step = mask['step']
        xstep = img.size[0]//step
        ystep = img.size[1]//step
        
        for i in range(0,xstep,1):
            for j in range(0,ystep,1):
                if inclined_range((i*step,j*step), mask['start'], mask['orientation'], mask['direction']):
                    #print('c')
                    topx = i*step
                    topy = j*step
                    botx = (i + 1)*step
                    boty = (j + 1)*step
                    my_block = [(topx, topy), (botx, boty)]
                    my_area.append(my_block)
        
    #------------------------------------------------------------------------------
    if mask['type'] == 'square':
        step = mask['step']
        xstep = img.size[0]//step
        ystep = img.size[1]//step
        for i in range(0,xstep,1):
            for j in range(0,ystep,1):
                if square_range((i*step, j*step), mask['corners']):
                    topx = max(0, i*step)
                    topy = max(0, j*step)
                    botx = min(img.size[0], (i + 1)*step)
                    boty = min(img.size[1], (j + 1)*step)
                    my_block = [(topx, topy), (botx, boty)]
                    my_area.append(my_block)        
    
    #------------------------------------------------------------------------------
    if mask['type'] == 'gradient square':
        step = mask['step']
        nbr_regions = range(0,len(step),1)
        total_width = mask['corners'][2] - mask['corners'][0]
        total_height  = mask['corners'][3] - mask['corners'][1]
        
        if mask['direction'] == 0:
            width = total_width // len(nbr_regions)
            height = total_height
            
            for k in nbr_regions:
                my_subarea = []
                
                xstep = width//step[k]
                ystep = height//step[k]
                
                xstart = mask['corners'][0] + k*width
                xend   = mask['corners'][0] + (k+1)*width
                ystart = mask['corners'][1]
                yend   = mask['corners'][3]
                
                my_zone = [xstart,ystart,xend,yend]
                print(my_zone)
                for i in range(0,xstep,1):
                    for j in range(0,ystep,1):
                        #if square_range((xstart + i*step[k], ystart + j*step[k]), my_zone):
                        topx = max(0, xstart + i*step[k])
                        topy = max(0, ystart + j*step[k])
                        botx = min(img.size[0], xstart + (i + 1)*step[k])
                        boty = min(img.size[1], ystart + (j + 1)*step[k])
                        my_block = [(topx, topy), (botx, boty)]
                        my_subarea.append(my_block)
        
                my_area.append(my_subarea)
            
    #------------------------------------------------------------------------------
    #if mask['type'] == 'strips': #stripped
            
    return my_area


