# A place to keep the ghosts of old code that might return.

def click_event(event, x, y, flags, params):
    img = params

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f'{str(x)},{str(y)}', (x,y), font, 1, (255, 0, 0), 2)
        cv2.imshow('image', img)

def showImage(file, dirName = ''):
    """Displays an image."""
    filePath = file
    if dirName != '':
        if dirName[-1] != '/':
            dirName += '/'
        filePath = dirName + file
    img = cv2.imread(cv2.samples.findFile(filePath))
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
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

    alpha = 1.5 
    beta = -150
    
    # Load the pathToImage
    image = cv2.imread(filePath)
    cv2.imshow('image', image)
    cv2.waitKey()
    contrast = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    
    cv2.imshow('contrast', contrast)
    cv2.waitKey()
    gray = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('gray', gray)
    cv2.waitKey()
    # blur = cv2.GaussianBlur(gray, (11,11), 0)
    # retval, thresh = cv2.threshold(blur, 0, 200, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret,thresh1 = cv2.threshold(gray,230,255,cv2.THRESH_BINARY)
    
    cv2.imshow('thresh1', thresh1)
    cv2.waitKey()
    # # Two pass erode with horizontal and vertical kernel
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,5))
    erode = cv2.erode(thresh1, horizontal_kernel, iterations=2)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,9))
    erode = cv2.erode(erode, vertical_kernel, iterations=2)
    canny_output = cv2.Canny(erode, 0, ret)
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through individual contours
    for contour in contours:
        # Approximate contour to a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        # Calculate aspect ratio and bounding box
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # Draw bounding box
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)
            cv2.putText(
                image,
                "Rectangle",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # Display the result
    # cv2.imshow("Detected Rectangles", image)
    # cv2.imshow('image', image)
    # cv2.waitKey()
    # cv2.imshow('contrast', contrast)
    # cv2.waitKey()
    # cv2.imshow('gray', gray)
    # cv2.waitKey()
    # cv2.imshow('blur', blur)
    # cv2.waitKey()
    # cv2.imshow('Erode', erode)
    # cv2.waitKey()
    # cv2.imshow('canny_output', canny_output)
    # cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imwrite(contouredFileName, image)
    print(f'Contoured image saved as: {contouredFileName}')
    return
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
    blur = cv2.GaussianBlur(gray, (231,231), 0)
    retval, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    
    # Two pass erode with horizontal and vertical kernel
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,5))
    erode = cv2.erode(thresh, horizontal_kernel, iterations=2)
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,9))
    erode = cv2.erode(erode, vertical_kernel, iterations=2)
    canny_output = cv2.Canny(erode, 0, 255)
    contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    
    # contours_poly = [None]*len(contours)
    # boundRect = [None]*len(contours)
    # centers = [None]*len(contours)
    # radius = [None]*len(contours)
    # for i, c in enumerate(contours):
    #     contours_poly[i] = cv2.approxPolyDP(c, 3, True)
    #     boundRect[i] = cv2.boundingRect(contours_poly[i])
    #     centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])
        
    drawing = np.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=np.uint8)
    # for i in range(len(contours)):
    #     color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    #     # cv2.drawContours(drawing, contours_poly, i, color)
    #     cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
    #         (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)

    c = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)

    # draw the biggest contour (c) in green
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int64(box)
    cv2.drawContours(image,[box],0,(0,0,255),2)

    cv2.imshow('Contours', image)
    # cv2.imshow('canny_output', canny_output)
    cv2.waitKey()
    # contours, hierarchy = cv2.findContours(canny_output, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # with open('contours.txt', 'w') as f:
    #     f.write(f'Hierarchy: {hierarchy}' + '\n')
    #     f.write(f'Number of contours: {len(contours)}' + '\n')
    #     for contour in contours:
    #         f.write(str(contour) + '\n')
    #     f.close()
    # c = max(contours, key = cv2.contourArea)
    # x,y,w,h = cv2.boundingRect(c)
    # image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    # for c in contours:
        # perimeter = cv2.arcLength(c,True)
        # epsilon = 0.1*cv2.arcLength(c,True)
        # approx = cv2.approxPolyDP(c,epsilon,True)
        # cv2.drawContours(image, [c], -1, (36, 255, 12), 3)
        # x,y,w,h = cv2.boundingRect(c)
        # image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)


    # cv2.imshow('image', image)
    # cv2.waitKey()
    # cv2.imshow('gray', gray)
    # cv2.waitKey()
    # cv2.imshow('blur', blur)
    # cv2.waitKey()
    # cv2.imshow('thresh', thresh)
    # cv2.waitKey()
    # cv2.imshow('erode', erode)
    # cv2.waitKey()
    # cv2.imshow('canny_output', canny_output)
    # cv2.waitKey()

    cv2.imwrite(contouredFileName, image)
    print(f'Contoured image saved as: {contouredFileName}')
    return
