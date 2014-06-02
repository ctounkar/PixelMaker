from PIL import Image
from Pixelmaker.PixelmakerFunctions import *
from Pixelmaker.PixelmakerColor import colors_in_range
from Pixelmaker.PixelmakerRange import *

class PixelMaker:

    transformations = ['full','circle','ring','square','couteau','bande','gradient squares']

    # ================================================================================
    def __init__(self, imageloc):
        self.image = Image.open(imageloc)
        self.size = self.image.size
        #self.mask = maskname
        #maskoptions = maskoptions # center, corners, orientation, etc
        #self.pixelzone = pixelzone #inside or outside
        #self.coloropion = coloroption #refer to color_pixel
        #self.basecolor = basecolor

    # ================================================================================
    def __getattr__(self, item):
        print("I don't know this {}".format(item))


    # ================================================================================
    def pixellize(self, maskname, mask_options, zone = 'in', color_option = 0, color = [0,0,0]):
        new_img = self.image.copy()

        # return the list of big pixels
        if maskname == 'circle':
            maskarea = pixelcircle(self, mask_options, zone)
        elif maskname == 'ring':
            maskarea = pixelring(self, mask_options, zone)
        elif maskname == 'square':
            maskarea = pixelsquare(self, mask_options, zone)
        elif maskname == 'bande':
            maskarea = pixelstripe(self, mask_options, zone)
        elif maskname == 'gradient squares':
            maskarea = pixelgradsquares(self, mask_options)
        elif maskname == 'couteau':
            maskarea = pixelcouteau(self, mask_options)
        elif maskname == 'full':
            maskarea = pixelfull(self, mask_options['step'])
        else:
            maskarea = pixelfull(self, mask_options['step'])


        if color_option not in [0,1,2,3,4]:
            option = 0 # while waiting for a proper error handling
        else:
            option = color_option

        new_img = colors_in_range(new_img, maskarea, maskname, option, color)

        return new_img

    # ================================================================================
    def pixellize_multi(self, maskname, mask_options, zone = 'in', color_option = 0, color = [0,0,0]):
        width = self.size[0]
        height = self.size[1]
        factor = fgcd(width, height) #factor lis should be in input
        
        new_width = width * len(factor)
        new_height = height
        new_img = Image.new('RGB', (new_width, new_height))
        
        i = 0
        
        for step in factor:
            new_box = (i*width, 0)
            new_img.paste(self.pixellize(step, maskname, mask_options, zone, color_option, color), new_box)
            i += 1
            
        return new_img
    
