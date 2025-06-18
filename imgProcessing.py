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
    blurDir = 'blurred/'
    if dirName != '':
        if dirName[-1] != '/':
            dirName += '/'
        filePath = dirName + file
        blurName = dirName + blurDir + file.split(".")[0] + '_blurred' + '.jpg'
    else:
        blurName =  blurDir + file.split(".")[0] + '_blurred' + '.jpg'

    img = cv2.imread(cv2.samples.findFile(filePath))

    if img is None:
        sys.exit(f"Could not read the image: {filePath}")
        return

    if not os.path.exists(dirName + blurDir):
        os.makedirs(dirName + blurDir)
        print(f'Created directory for blurred images: {dirName}{blurDir}')

    blur = cv2.GaussianBlur(img, (451, 451), 0)
    cv2.imwrite(blurName, blur)
    print(f'Blurred image saved as: {blurName}')
    return
    
def blurAllImages(dirName):
    """Creates a blurred image using Gaussian blur for each image in the directory."""
    if dirName[-1] != '/':
        dirName += '/'
    print(f'Blurring all images in directory: {dirName}')
    files = []
    [files.extend(glob.glob(f'{dirName}*.{e}')) for e in _EXTENSIONS_]
    for file in files:
        print(f'Blurring image: {file}')
        fileName = os.path.basename(file)
        blurImage(fileName, dirName)
    return

def resizeImage(file, newHeight = 0, newWidth = 0, dirName = ''):
    """Resizes an image. If no height or width is given, the image is resized to height 1000 and width/height ratio."""
    filePath = file
    resizeDir = 'resized/'
    if dirName != '':
        if dirName[-1] != '/':
            dirName += '/'
        filePath = dirName  + file
        resizeName = dirName + resizeDir + file.split(".")[0] + '.jpg'
    else:
        resizeName = resizeDir + file.split(".")[0] + '.jpg'

    img = cv2.imread(cv2.samples.findFile(filePath))

    if img is None:
        sys.exit(f"Could not read the image: {filePath}")
        return

    if not os.path.exists(dirName + resizeDir):
        os.makedirs(dirName + resizeDir)
        print(f'Created directory for resized images: {dirName}{resizeDir}')

    imgHeight, imgWidth = img.shape[:2]
    if newHeight == 0 and newWidth == 0:
        newHeight = 1000
        newWidth = int(newHeight * imgWidth / imgHeight)
    if newHeight != 0 and newWidth == 0:
        newWidth = int(newHeight * imgWidth / imgHeight)
    if newHeight == 0 and newWidth != 0:
        newHeight = int(newWidth * imgHeight / imgWidth)
    resize = cv2.resize(img, (newWidth, newHeight))
    cv2.imwrite(resizeName, resize)
    print(f'Resized image saved as: {resizeName}')
    return

def resizeAllImages(dirName):
    """Creates a resized image for each image in the directory."""
    if dirName[-1] != '/':
        dirName += '/'
    print(f'Resizing all images in directory: {dirName}')
    files = []
    [files.extend(glob.glob(f'{dirName}*.{e}')) for e in _EXTENSIONS_]
    for file in files:
        print(f'Resizing image: {file}')
        fileName = os.path.basename(file)
        resizeImage(fileName, 0, 0, dirName)
    return
#######################################################################
# Find and Display Functions                                  
#######################################################################

def _get_local_functions():
    return {
        name: obj
        for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isfunction(obj)
        and not name.startswith('_')
        and obj.__module__ == __name__
    }


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
