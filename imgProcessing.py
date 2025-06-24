import cv2
import numpy as np
import sys
import os
import inspect
import glob
import random as rng

rng.seed(12345)

_EXTENSIONS_ = ["jpg", "png", "jpeg", "JPG", "PNG", "JPEG"]

#######################################################################
# Helper Functions                                 
#######################################################################
def __ending_slash(path):
    if path[-1] != '/':
        path += '/'
    return path

def __check_directory(dirName):
    return os.path.exists(__ending_slash(dirName))

def __create_sub_directory(dirName):
    if not __check_directory(dirName):
        os.makedirs(dirName)
        print(f'Created sub directory: {dirName}')
    else:
        print(f'Sub directory exists: {dirName}')
        

def __find_file(file):
    print(f'Searching for file: {file}')
    if os.path.exists(file):
        print(f'File found: {file}')
        return True
    else:
        print(f'File not found: {file}')
        return False

def __check_valid_image(file):
    if __find_file(file) and file.split(".")[1] in _EXTENSIONS_:
        print (f'File is a valid image: {file}')
        return True
    else:
        print (f'File is not a valid image: {file}, only {", ".join(_EXTENSIONS_)} files are allowed.')
        return False

def __make_processing_file_name(file, sub_dir = '', suffix = '_processed', fileType = 'jpg'):
    if sub_dir != '':
        return __ending_slash(sub_dir) + file.split(".")[0] + suffix + '.' + fileType
    return file.split(".")[0] + suffix + '.' + fileType

def __prepare_image(file, dirName = '', suffix = '', fileType = 'jpg'):
    if __check_valid_image(file):
        return __make_processing_file_name(file, dirName, suffix, fileType)
        
    


#######################################################################
# Image Processing Functions                                  
#######################################################################
def contrastImage(file, dirName = '', fileType = 'jpg', showImage = False):
    newImage = __prepare_image(file, dirName, suffix = '_contrast', fileType = fileType)

    image = cv2.imread(cv2.samples.findFile(file))
    alpha = 2.0 
    beta = 0  
    
    new_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    if showImage:
        cv2.imshow('Original Image', image)
        cv2.imshow('New Image', new_image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    cv2.imwrite(newImage, new_image)
    print(f'Contrasted image saved as: {newImage}')
    return

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
        print(f"#################   {name}   #################")
        print(f"arguments: {' '.join(arguments)}")
        print(f"returns: {f.__doc__ or '?'}")
        print(f"Command: python3 {script_name} {name} <{' '.join(arguments)}>")
        print()


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
