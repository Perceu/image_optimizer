def resize_image(img, width=None, height=None):
    if width and height:
        img_resize = img.resize((width, height))
    else:
        original_width, original_height = img.size    
        img_resize = img.resize(resize_factory(original_width, original_height, width, height))
    return img_resize

def resize_factory(original_width, original_height,width,height):    
    if width:
        percent_change = (width*100)/original_width
        new_height = int(original_height*(percent_change/100))
        return (width, new_height)
    elif height:
        percent_change = (height*100)/original_height
        new_width = int(original_width*(percent_change/100))
        return (new_width, height)

def new_image_name_factory(name,file_extension,width,height):
    if width and height:
        new_name = "red_{}_{}_{}.{}".format(name,height,width,file_extension)
    elif width:
        new_name = "red_{}_w{}.{}".format(name,width,file_extension)
    elif height:
        new_name = "red_{}_h{}.{}".format(name,height,file_extension)
    return new_name