from PIL import Image, ImageDraw
from Pixelmaker.PixelmakerFunctions import *
from Pixelmaker.PixelmakerColor import colors_in_range
from Pixelmaker.PixelmakerRange import *


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


class PixelOne:
    '''
    Unit block for pixellizing an image.
    Block is made of:
    - the corners (xupper, yupper, xlower, ylower)
    - the color of the inside
    - the width of the outline
    - the color of the outline

    In the first implementation, the block is a rectangle and the color is uniform.
    Later development will be to have any shape and a pattern for the color
    '''

    def __init__(self, corners, colors_inside, width_outline=None, colors_outline=None):
        '''
        Block is made of:
        - self.corners = (xupper, yupper, xlower, ylower)
        - self.color_inside = (R,G,B)
        - self.external = (xupper, yupper, xlower, ylower, awidth)
        - self.color_outline = (R,G,B)
        '''
        if len(corners) > 1 and len(corners) < 5:
            try:
                xu = int(corners[0])
                yu = int(corners[1])

                if len(corners) == 2: # 1 pixel
                    xd = self.xu + 1
                    yd = self.yu + 1
                elif len(corners) == 3: # upper corner + width
                    xd = self.xu + int(corners[2])
                    yd = self.yu + int(corners[2])
                elif len(corners) == 4: # upper corner + lower corner
                    xd = int(corners[2])
                    yd = int(corners[3])

                if xu > xd:
                    xu, xd = xd, xu

                if yu > yd:
                    yu, yd = yd, yu

                self.corners = (xu, yu, xd, yd)

            except ValueError:
                print('One of the value is not an integer.')
        else:
            raise InputError(corners, 'is not a valid Input. You need at least 2, 3 or 4 numerical values.')

        if len(colors_inside) == 3:
            try:
                colors_r = int(colors_inside[0])
                colors_g = int(colors_inside[1])
                colors_b = int(colors_inside[2])
                self.color_inside = (colors_r,colors_g,colors_b)
            except ValueError:
                print('One of the value is not an integer.')
        else:
            raise InputError(corners, 'is not a valid Input. You need at least 3 numerical values.')

        if width_outline:
            try:
                awidth = int(width_outline)
                wd = self.corners[2] - self.corners[0]
                hg = self.corners[3] - self.corners[1]

                if (2*awidth < wd + 1) and (2*awidth < hg + 1):
                    self.external = self.corners, awidth
                    self.corners = (self.corners[0] + awidth, self.corners[1] + awidth, self.corners[2] - awidth, self.corners[3] - awidth)
                else:
                    raise InputError(width_outline,'is not a valid input. The value is too high compared to the size of the pixel.')

                '''color of the borders'''
                if colors_outline:
                    try:
                        cout_r = int(colors_outline[0])
                        cout_g = int(colors_outline[1])
                        cout_b = int(colors_outline[2])
                        self.color_outline = (cout_r, cout_g, cout_b)
                    except ValueError:
                        print('One of the value is not an integer.')
                else:
                    self.color_outline = (255, 255, 255)

            except ValueError:
                print('One of the value is not an integer.')

        else:
            self.external = None
            self.color_outline = None

    def draw_pixel(self, image):
        '''
        Specific function to replace the basic draw.rectangle from ImageDraw
        '''
        draw = ImageDraw.Draw(image)
        draw.rectangle(self.corners, fill=self.color_inside)
        if self.external:
            draw.rectangle(self.external, outline=self.color_outline)

        del draw

    def __add__(self, pix):
        '''
        Add a pixel to another pixel
        '''
        
        new_inside = self.color_inside
        new_outline = self.color_outline
        
        if self.corners == pix.corners:
            new_inside[0] += pix.color_inside[0]
            new_inside[1] += pix.color_inside[1]
            new_inside[2] += pix.color_inside[2]

            if self.external and pix.external:
                new_outline[0] += pix.color_outline[0]
                new_outline[1] += pix.color_outline[1]
                new_outline[2] += pix.color_outline[2]

            elif pix.external:
                new_outline[0] = pix.color_outline[0]
                new_outline[1] = pix.color_outline[1]
                new_outline[2] = pix.color_outline[2]

            new_pix = PixelOne(self.corners, new_inside, self.external, new_outline)
            return new_pix
        
        else:
            raise InputError(pix, "cannot be added to this value")

    def __radd__(self, pix):
        return self + pix

class PixelBlock:
    '''
    Dictionary PixelOne:Color option
    Main advantage is to be able to associate different transformations to the same image.
    '''

    def __init__(self, previous_block = {}):
        '''
        Intialisation from a previous PixelBlock or individual pixels
        '''

        self._keys = []
        self._values = []

        if type(previous_block) == PixelBlock:
            for cle in previous_block.keys():
                #self[cle] = previous_block[cle]
                self._keys.append(cle)
                self._values.append(previous_block[cle])
        elif type(previous_block) == dict:
            for cle in previous_block.keys():
                self._keys.append(cle)
                self._values.append(PixelOne(cle, previous_block[cle]))
        else:
            raise InputError(previous_block, "is not the input expected")


    def __repr__(self):
        '''
        Display the dictionary of pixels
        '''
        chaine = "{"
        premier_passage = True

        for cle, valeur in self.items():
            if not premier_passage:
                chaine += ", "
            else:
                premier_passage = False
            chaine += repr(cle) + ": " + repr(valeur)

        chaine += "}"

        return chaine

    def __str__(self):
        '''
        Provide the text for print function
        '''
        return repr(self)

    def keys(self):
        '''return the list of keys'''
        return self._keys

    def values(self):
        '''return the list of values'''
        return self._values

    def items(self):
        '''return each tuple (Pixel, data)'''
        for i, cle in enumerate(self._keys):
            yield (cle, self._values[i])

    def __getitem__(self, item):
        return self._values[self._keys.index(item)]

    def __setitem__(self, key, pix):
        '''
        append a new pixel to the block
        current version does not replace an existing entry
        '''
        if type(pix) == PixelOne:
            if key not in self.keys():
                self._keys.append(key)
                self._values.append(PixelOne(key, pix.color_inside, pix.external, pix.color_outline))
            #TODO: handle an existing entry: merge?, duplicate?, replace?
            #else:
            #    raise InputError(key, "is already defined")
        else:
            raise InputError(pix, "is not the input expected")

    def __len__(self):
        '''return the number of blocks'''
        return len(self._keys)

    def __contains__(self, item):
        if type(item) == PixelOne:
            return (item in self._values)
        else:
            return False

    def insert(self, other):
        '''
        Add a dictionary of pixels to a Pixel Block
        '''
        if type(other) == dict:
            my_block = PixelBlock(other)
        elif type(other) == PixelBlock:
            my_block = other
        else:
            raise InputError(other, 'is not a valid input.')

        for cle in my_block.keys():
            self[cle] = my_block[cle]

    def pixellize(self, img, mask_options = None, color_options = None):
        '''
        Fill the PixelBlock with the correct couple of pixel:color
        '''
        if mask_options:
            # pixellisation based on options
            maskname = mask_options['type']
            zone = mask_options['zone']

            # return the list of big pixels
            if maskname == 'circle':
                maskarea = pixelcircle(img, mask_options, zone)
            elif maskname == 'ring':
                maskarea = pixelring(img, mask_options, zone)
            elif maskname == 'square':
                maskarea = pixelsquare(img, mask_options, zone)
            elif maskname == 'bande':
                maskarea = pixelstripe(img, mask_options, zone)
            elif maskname == 'gradient squares':
                maskarea = pixelgradsquares(img, mask_options)
            elif maskname == 'couteau':
                maskarea = pixelcouteau(img, mask_options)
            elif maskname == 'full':
                maskarea = pixelfull(img, mask_options['step'])

            # return the color
            option = color_options['option']
            color = color_options['color']

            if option not in [0,1,2,3,4]:
                option = 0 # while waiting for a proper error handling

        else:
            # default pixellization
            maskname = 'full'
            maskarea = pixelfull(img, 2)
            option = 0
            color = None

        # add the results of the pixellization
        self.insert(colors_in_range(img, maskarea, maskname, option, color))

    def commit(self, img):
        '''
        Draw the pixels created by pixellize function
        '''
        for cle in self._keys:
            self[cle].draw_pixel(img)

class PixelMaker:

    transformations = ['full', 'circle', 'ring', 'square', 'couteau', 'bande', 'gradient squares']

    # ================================================================================
    def __init__(self, imageloc):
        self.image = Image.open(imageloc)
        self.size = self.image.size


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
    
