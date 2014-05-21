from math import sin

# ================================================================================
# functions ---------------
# ================================================================================
def inclined_range(point, start, angle, side):
    in_range = False
    
    if angle == 0 or angle == 180:
        if side == 'up':
            in_range = (point[1] <= start)        
        elif side == 'down':
            in_range = (point[1] >= start)
            
    elif angle == 90:
        if side == 'left':
            in_range = (point[0] <= start)
        elif side == 'right':
            in_range = (point[0] >= start)
    
    elif angle > 0 and angle < 90 :# y = (start - x) * sin(angle) 
        if side == 'up':
            in_range = (point[1] <= (start - point[0])*sin(angle))        
        elif side == 'down':
            in_range = (point[1] >= (start - point[0])*sin(angle))
        elif side == 'left':
            in_range = (point[0] <= start - point[1]/sin(angle))
        elif side == 'right':
            in_range = (point[0] >= start - point[1]/sin(angle))
    
    elif angle > 90 and angle < 180 :# y = (x - start) * sin(angle) 
        if side == 'up':
            in_range = (point[1] <= (point[0] - start)*sin(angle))        
        elif side == 'down':
            in_range = (point[1] >= (point[0] - start)*sin(angle))
        elif side == 'left':
            in_range = (point[0] <= start + point[1]/sin(angle))
        elif side == 'right':
            in_range = (point[0] >= start + point[1]/sin(angle))
        
    return in_range

# ================================================================================
def between_bars(point, start, end, angle):
    in_range = False
    
    # bande horizontale
    if angle == 0 or angle == 180:
        in_range = (point[1] >= start) and (point[1] <= end)
    
    # bande verticale
    elif angle == 90:
        in_range = (point[0] >= start) and (point[0] <= end)

    # bande oblique
    elif angle > 0 and angle < 90:
        ya = inclined_range(point, start, angle,'down')
        yb = inclined_range(point, end, angle,'up')
        xa = inclined_range(point, start, angle,'right')
        xb = inclined_range(point, end, angle,'left')
        
        in_range = xa and xb and ya and yb
    
    elif angle > 90 and angle < 180:
        ya = inclined_range(point, start, angle,'up')
        yb = inclined_range(point, end, angle,'down')
        xa = inclined_range(point, start, angle,'right')
        xb = inclined_range(point, end, angle,'left')
    
        in_range = xa and xb and ya and yb
    
    elif angle < 0:
        in_range = between_bars(point,start, end, angle % -180)

    elif angle > 180:
        in_range = between_bars(point,start, end, angle % 180)
        
    return in_range

