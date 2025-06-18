import cv2
import sys
import os
import inspect
import glob

_EXTENSIONS_ = ["jpg", "png", "jpeg", "JPG", "PNG", "JPEG"]

#######################################################################
# Image Processing Functions                                  
#######################################################################

def contourImage(file, dirName = ''):
    """Contours an image."""
    filePath = file
    contouredFileName = ''
    contourFileSuffix = '_contoured'
    contouredDir = 'contoured/'
    if dirName != '':
        if dirName[-1] != '/':
            dirName += '/'
        filePath = dirName + file
        contouredFileName = dirName + contouredDir + file.split(".")[0] + contourFileSuffix + '.jpg'
    else:
        contouredFileName =  contouredDir + file.split(".")[0] + contourFileSuffix + '.jpg'
    

    if not os.path.exists(dirName + contouredDir):
        os.makedirs(dirName + contouredDir)
        print(f'Created directory for blurred images: {dirName}{contouredDir}')

    # Load the pathToImage
    image = cv2.imread(filePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (13,13), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Two pass dilate with horizontal and vertical kernel
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,5))
    dilate = cv2.dilate(thresh, horizontal_kernel, iterations=2)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,9))
    dilate = cv2.dilate(dilate, vertical_kernel, iterations=2)

    # Find contours, filter using contour threshold area, and draw rectangle
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area > 20000:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)

    cv2.imshow('image', image)
    cv2.imshow('gray', gray)
    cv2.imshow('blur', blur)
    cv2.imshow('dilate', dilate)
    cv2.imshow('thresh', thresh)
    cv2.waitKey()

    cv2.imwrite(contouredFileName, thresh)
    print(f'Blurred image saved as: {contouredFileName}')
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
