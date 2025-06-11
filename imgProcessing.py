import cv2
import sys
import os
import inspect
import glob

_EXTENSIONS_ = ["jpg", "png", "jpeg", "JPG", "PNG", "JPEG"]

#######################################################################
# Image Processing Functions                                  
#######################################################################
def blurImage(file, dirName = ''):
    """Blurs an image using Gaussian blur."""
    filePath = file
    blurName = ''
    if dirName != '':
        if dirName[-1] != '/':
            dirName += '/'
        filePath = dirName + file
        blurName = dirName + file.split(".")[0] + '_blurred' + '.jpg'
    else:
        blurName = file.split(".")[0] + '_blurred' + '.jpg'
    
    img = cv2.imread(cv2.samples.findFile(filePath))

    if img is None:
        sys.exit("Could not read the image.")
    else:
        blur = cv2.GaussianBlur(img, (451, 451), 0)
        cv2.imwrite(blurName, blur)
        print('Blurred image saved as: ' + blurName)
    return
    
def blurAllImages(dirName):
    """Creates a blurred image using Gaussian blur for each image in the directory."""
    if dirName[-1] != '/':
        dirName += '/'
    print('Blurring all images in directory: ' + dirName)
    files = []
    [files.extend(glob.glob(dirName + '*.' + e)) for e in _EXTENSIONS_]
    for file in files:
        print('Blurring image: ' + file)
        fileName = os.path.basename(file)
        blurImage(fileName, dirName)
    return

#######################################################################
# Find and Display Functions                                  
#######################################################################

def _get_local_functions():
    local_functions = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isfunction(obj) and not name.startswith('_') and obj.__module__ == __name__:
            local_functions[name] = obj
    return local_functions


def _list_functions(script_name):
    print(f"Available functions in {script_name}:")
    for name, f in _get_local_functions().items():
        print()
        arguments = inspect.signature(f).parameters
        print(f"{name}")
        print(f"arguments: {' '.join(arguments)}")
        print(f"returns: {f.__doc__ or '?'}")
        print(f"Command: python3 {script_name} {name} <{' '.join(arguments)}>")


#######################################################################
# Entry Point                                 
#######################################################################

if __name__ == '__main__':
    script_name, *args = sys.argv
    if args:
        functions = _get_local_functions()
        function_name = args.pop(0)
        if function_name in functions:
            function = functions[function_name]
            function(*args)
        else:
            print(f"Function {function_name} not found")
            _list_functions(script_name)
    else:
        _list_functions(script_name)
