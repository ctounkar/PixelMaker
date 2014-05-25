from math import sqrt

# ================================================================================
# functions ---------------
# ================================================================================
def circle_range(point, center, radius, region = 'in'):
    in_circle = False
    
    distance = sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2)
    
    if region == 'in':
        in_circle = (distance <= radius)
    elif region == 'out':
        in_circle = (distance >= radius)
            
    return in_circle

# ================================================================================
def square_range(point,corners, region = 'in'):
    # corners = (x1,y1,x2,y2) avec x2 > x1 et y2 > y1
    if region == 'in':
        in_range = (point[0] >= corners[0]) and (point[1] >= corners[1]) and (point[0] <= corners[2]) and (point[1] <= corners[3])
    elif region == 'out':
        in_range = not ((point[0] >= corners[0]) and (point[1] >= corners[1]) and (point[0] <= corners[2]) and (point[1] <= corners[3]))
        #in_range = (point[0] <= corners[0]) or (point[1] <= corners[1]) or (point[0] >= corners[2]) or (point[1] >= corners[3])
        
    return in_range

#def ellipse_range(point, corners):
#    return in_range

#def losange_range(point, corners):
#    return in_range

#def rectangle_range(point, corners):
#    return in_range

#def triangle_range(point, corners):
#    return in_range

#def trapeze_range(point, corners):
#    return in_range