from Pixelmaker.PixelmakerLines import inclined_range, between_bars
from Pixelmaker.PixelmakerGeometry import circle_range, square_range

# ================================================================================
# functions ---------------
# ================================================================================
def pixelfull(my_img, my_step):
    my_area = []
    xstep = my_img.size[0] // my_step
    ystep = my_img.size[1] // my_step
    for i in range(0, xstep, 1):
        for j in range(0, ystep, 1):
            topx = max(0, i * my_step)
            topy = max(0, j * my_step)
            botx = min(my_img.size[0], (i + 1) * my_step)
            boty = min(my_img.size[1], (j + 1) * my_step)
            my_block = (topx, topy, botx, boty)
            my_area.append(my_block)

    return my_area


# ================================================================================
def pixelcircle(my_img, mask_options, pixelzone):
    my_area = []
    my_block = [(0, 0), (0, 0)]
    # ------------------------------------------------------------------------------
    my_step = mask_options['step']
    xstep = my_img.size[0] // my_step
    ystep = my_img.size[1] // my_step
    for i in range(0, xstep, 1):
        for j in range(0, ystep, 1):
            if pixelzone == 'in' and circle_range(((i + 1 / 2) * my_step, (j + 1 / 2) * my_step),
                                                  mask_options['center'], mask_options['radius']):
                topx = max(0, i * my_step)
                topy = max(0, j * my_step)
                botx = min(my_img.size[0], (i + 1) * my_step)
                boty = min(my_img.size[1], (j + 1) * my_step)
                my_block = (topx, topy, botx, boty)
                my_area.append(my_block)

            elif pixelzone == 'out' and not circle_range(((i + 1 / 2) * my_step, (j + 1 / 2) * my_step),
                                                         mask_options['center'], mask_options['radius']):
                topx = max(0, i * my_step)
                topy = max(0, j * my_step)
                botx = min(my_img.size[0], (i + 1) * my_step)
                boty = min(my_img.size[1], (j + 1) * my_step)
                my_block = (topx, topy, botx, boty)
                my_area.append(my_block)

    return my_area


# ================================================================================
def pixelring(my_img, mask_options, pixelzone):
    my_area = []
    my_block = [(0, 0), (0, 0)]
    # ------------------------------------------------------------------------------
    my_step = mask_options['step']
    xstep = my_img.size[0] // my_step
    ystep = my_img.size[1] // my_step
    for i in range(0, xstep, 1):
        for j in range(0, ystep, 1):
            test_inner = circle_range(((i + 1 / 2) * my_step, (j + 1 / 2) * my_step), mask_options['center'],
                                      mask_options['radius'], 'out')
            test_outer = circle_range(((i + 1 / 2) * my_step, (j + 1 / 2) * my_step), mask_options['center'],
                                      mask_options['radius'] + mask_options['width'], 'in')
            test = test_inner and test_outer

            if pixelzone == 'in' and test:
                topx = max(0, i * my_step)
                topy = max(0, j * my_step)
                botx = min(my_img.size[0], (i + 1) * my_step)
                boty = min(my_img.size[1], (j + 1) * my_step)
                my_block = (topx, topy, botx, boty)
                my_area.append(my_block)
                my_area.append(my_block)

            elif pixelzone == 'out' and not test:
                topx = max(0, i * my_step)
                topy = max(0, j * my_step)
                botx = min(my_img.size[0], (i + 1) * my_step)
                boty = min(my_img.size[1], (j + 1) * my_step)
                my_block = (topx, topy, botx, boty)
                my_area.append(my_block)
                my_area.append(my_block)

    return my_area


# ================================================================================
def pixelstripe(my_img, mask_options, pixelzone):
    my_area = []
    my_block = [(0, 0), (0, 0)]
    # ------------------------------------------------------------------------------
    my_step = mask_options['step']
    xstep = my_img.size[0] // my_step
    ystep = my_img.size[1] // my_step

    if mask_options['orientation'] == 0 or mask_options['orientation'] == 180:
        # bande horizontale
        for j in range(0, ystep, 1):
            if pixelzone == 'in' and (j * my_step >= mask_options['start'] and j * my_step <= (
                        mask_options['start'] + mask_options['width'])):
                for i in range(0, xstep, 1):
                    topx = i * my_step
                    topy = j * my_step
                    botx = (i + 1) * my_step
                    boty = (j + 1) * my_step
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)

            elif pixelzone == 'out' and (j * my_step <= mask_options['start'] or j * my_step >= (
                        mask_options['start'] + mask_options['width'])):
                for i in range(0, xstep, 1):
                    topx = i * my_step
                    topy = j * my_step
                    botx = (i + 1) * my_step
                    boty = (j + 1) * my_step
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)

    elif mask_options['orientation'] == 90:
        # bande verticale
        for i in range(0, xstep, 1):
            if pixelzone == 'in' and (i * my_step >= mask_options['start'] and i * my_step <= (
                        mask_options['start'] + mask_options['width'])):
                for j in range(0, ystep, 1):
                    topx = i * my_step
                    topy = j * my_step
                    botx = (i + 1) * my_step
                    boty = (j + 1) * my_step
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)

            elif pixelzone == 'out' and (i * my_step <= mask_options['start'] or i * my_step >= (
                        mask_options['start'] + mask_options['width'])):
                for j in range(0, ystep, 1):
                    topx = i * my_step
                    topy = j * my_step
                    botx = (i + 1) * my_step
                    boty = (j + 1) * my_step
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)


    else:
        for i in range(0, xstep, 1):
            for j in range(0, ystep, 1):
                if pixelzone == 'in' and between_bars((i * my_step, j * my_step), mask_options['start'],
                                                      mask_options['start'] + mask_options['width'],
                                                      mask_options['orientation']):
                    topx = i * my_step
                    topy = j * my_step
                    botx = (i + 1) * my_step
                    boty = (j + 1) * my_step
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)

                elif pixelzone == 'out' and not between_bars((i * my_step, j * my_step), mask_options['start'],
                                                             mask_options['start'] + mask_options['width'],
                                                             mask_options['orientation']):
                    topx = i * my_step
                    topy = j * my_step
                    botx = (i + 1) * my_step
                    boty = (j + 1) * my_step
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)

    return my_area


# ================================================================================
def pixelcouteau(my_img, mask_options):
    my_area = []
    my_block = [(0, 0), (0, 0)]
    # ------------------------------------------------------------------------------
    my_step = mask_options['step']
    xstep = my_img.size[0] // my_step
    ystep = my_img.size[1] // my_step

    for i in range(0, xstep, 1):
        for j in range(0, ystep, 1):
            if inclined_range((i * my_step, j * my_step), mask_options['start'], mask_options['orientation'],
                              mask_options['direction']):
                #print('c')
                topx = i * my_step
                topy = j * my_step
                botx = (i + 1) * my_step
                boty = (j + 1) * my_step
                my_block = (topx, topy, botx, boty)
                my_area.append(my_block)

    return my_area


# ================================================================================
def pixelsquare(my_img, mask_options, pixelzone):
    my_area = []
    my_block = [(0, 0), (0, 0)]
    # ------------------------------------------------------------------------------
    if my_img.maskname == 'square':
        my_step = mask_options['step']
        xstep = my_img.size[0] // my_step
        ystep = my_img.size[1] // my_step
        for i in range(0, xstep, 1):
            for j in range(0, ystep, 1):
                if pixelzone == 'in' and square_range((i * my_step, j * my_step), mask_options['corners']):
                    topx = max(0, i * my_step)
                    topy = max(0, j * my_step)
                    botx = min(my_img.size[0], (i + 1) * my_step)
                    boty = min(my_img.size[1], (j + 1) * my_step)
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)

                elif pixelzone == 'out' and not square_range((i * my_step, j * my_step), mask_options['corners']):
                    topx = max(0, i * my_step)
                    topy = max(0, j * my_step)
                    botx = min(my_img.size[0], (i + 1) * my_step)
                    boty = min(my_img.size[1], (j + 1) * my_step)
                    my_block = (topx, topy, botx, boty)
                    my_area.append(my_block)

    return my_area


# ================================================================================
def pixelgradsquares(my_img, mask_options):
    my_area = []
    my_block = [(0, 0), (0, 0)]
    # ------------------------------------------------------------------------------
    my_step = mask_options['step']
    nbr_regions = range(0, len(my_step), 1)
    total_width = mask_options['corners'][2] - mask_options['corners'][0]
    total_height = mask_options['corners'][3] - mask_options['corners'][1]

    if mask_options['direction'] == 0:
        width = total_width // len(nbr_regions)
        height = total_height

        for k in nbr_regions:
            my_subarea = []

            xstep = width // my_step[k]
            ystep = height // my_step[k]

            xstart = mask_options['corners'][0] + k * width
            xend = mask_options['corners'][0] + (k + 1) * width
            ystart = mask_options['corners'][1]
            yend = mask_options['corners'][3]

            my_zone = [xstart, ystart, xend, yend]
            #print(my_zone)
            for i in range(0, xstep, 1):
                for j in range(0, ystep, 1):
                    topx = max(0, xstart + i * my_step[k])
                    topy = max(0, ystart + j * my_step[k])
                    botx = min(my_img.size[0], xstart + (i + 1) * my_step[k])
                    boty = min(my_img.size[1], ystart + (j + 1) * my_step[k])
                    my_block = (topx, topy, botx, boty)
                    my_subarea.append(my_block)

            my_area.append(my_subarea)

    return my_area

# ------------------------------------------------------------------------------
#if my_img.maskname == 'strips': #stripped

#------------------------------------------------------------------------------
#if my_img.maskname == 'cross': #cross
