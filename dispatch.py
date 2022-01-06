# from httplib import HTTPResponse
# from wx.lib.agw import cubecolourdialog
# from colorama.ansi import Back


def dispatch(parm={}):
    httpResponse = {}
    if(not('op' in parm)):
        httpResponse['status'] =  'error: op code is missing'
    elif(parm['op'] == ''):
        httpResponse['status'] =  'error: op code is missing'
    elif(parm['op'] != '' and parm['op'] != 'check' and parm['op'] != 'create' and parm['op'] != 'rotate'):
        httpResponse['status'] =  'error: op code is missing'
#         httpResponse['status'] = checkCondition(parm,'status')
#         if httpResponse['status'][0:6] != 'error:':
#             httpResponse['cube'] = checkCondition(parm,'cube')
    elif(parm['op'] == 'create'):
        httpResponse['status'] =  createCube(parm,'status')
        if httpResponse['status'] != 'error: at least two faces have the same color':
            httpResponse['cube'] = createCube(parm, 'cube')
    elif(parm['op'] == 'check'):
        httpResponse['status'] = checkCube(parm)
    elif(parm['op'] == 'rotate'):
        face = ['f','F','r','R','b','B','l','L','t','T','u','U']
        if('cube' in parm):
            if(not('face' in parm)):
                httpResponse['status'] = 'error: face is missing'
                return httpResponse
        if('face' in parm):
            if(not('cube' in parm)):
                httpResponse['status'] = 'error: cube is missing'
                return httpResponse
        if(not('cube' in parm)):
            if(not('face' in parm)):
                httpResponse['status'] = 'error: cube and face missing'
                return httpResponse
        if(not(parm['face'] in face)):
            httpResponse['status'] = "error: face is unknown"
            
        else:
            check = checkCube(parm)
            if(check == "error:  unsolvable cube configuration" ):
                httpResponse['status'] = 'error:  unsolvable cube configuration'
                return httpResponse

            httpResponse['status'] = 'rotated'
            httpResponse['cube'] = rotateCube(parm, 'cube')
    return httpResponse

def createCube(parm,condition):
    if condition == 'status':
        status = ''
        defaultFaceColor = {'f':'green','r':'yellow','b':'blue','l':'white','t':'red','u':'orange'}

        assignedColor = set()
        for key in defaultFaceColor.keys():
            if key in parm:
                assignedColor.add(parm[key])
            else:
                assignedColor.add(defaultFaceColor[key])
        if len(assignedColor) < 6:
            status = status +  'error: at least two faces have the same color'
        else:
            status = status +  'created'
        return status

    elif condition == 'cube' :
        cube = []

        if(not('f' in parm)):
            for _ in range(9):
                cube.append('green')
        else:
            if(parm['f'] == ''):
                return 'error: face color is missing'
            else:
                for _ in range(9):
                    cube.append(parm['f'])

        if(not('r' in parm)):
            for _ in range(9):
                cube.append('yellow')
        else:
            for _ in range(9):
                cube.append(parm['r'])

        if(not('b' in parm)):
            for _ in range(9):
                cube.append('blue')
        else:
            for _ in range(9):
                cube.append(parm['b'])

        if(not('l' in parm)):
            for _ in range(9):
                cube.append('white')
        else:
            for _ in range(9):
                cube.append(parm['l'])

        if(not('t' in parm)):
            for _ in range(9):
                cube.append('red')
        else:
            for _ in range(9):
                cube.append(parm['t'])

        if(not('u' in parm)):
            for _ in range(9):
                cube.append('orange')
        else:
            for _ in range(9):
                cube.append(parm['u'])
        return cube
    

def checkCube(parm):
    if(not('cube' in parm)):
        return 'error: Cube must be specified'
    else:
        list1 = parm['cube']
        list1 =  list1.split(',')
        checkColors = set(list1)
        if(len(checkColors) != 6):
            return "error: Can only use 6 different types of color in a cube"

            
        
        if(len(list1) != 54):
            return "error: Cube is not sized properly"
        else:
            #checking for the center cube of each side
            frontFace = list1[0:9]
            rightFace = list1[9:18]
            backFace = list1[18:27]
            leftFace = list1[27:36]
            topFace = list1[36:45]
            underFace = list1[45:54]
            countFront = frontFace.count(frontFace[0])
            countRight = rightFace.count(rightFace[0])
            countBack = backFace.count(backFace[0])
            countLeft = leftFace.count(leftFace[0])
            countTop = topFace.count(topFace[0])
            countUnder = underFace.count(underFace[0])
            frontCorners = set([frontFace[0], frontFace[2], frontFace[6], frontFace[8]])
            frontCrosses =  set([frontFace[1],frontFace[3],frontFace[4],frontFace[5], frontFace[7]])
            rightCorners = set([rightFace[0], rightFace[2], rightFace[6], rightFace[8]])
            rightCrosses = set([rightFace[1], rightFace[3],rightFace[4],rightFace[5], rightFace[7]])
            backCorners = set([backFace[0], backFace[2], backFace[6], backFace[8]])
            backCrosses = set([backFace[1], backFace[3],backFace[4], backFace[5], backFace[7]])
            leftCorners = set([leftFace[0], leftFace[2], leftFace[6], leftFace[8]])
            leftCrosses = set([leftFace[1], leftFace[3],leftFace[4],leftFace[5], leftFace[7]])
            topCorners = set([topFace[0], topFace[2], topFace[6], topFace[8]])
            topCrosses = set([topFace[1], topFace[3], topFace[4],topFace[5], topFace[7]])
            underCorners = set([underFace[0], underFace[2], underFace[6], underFace[8]])
            underCrosses = set([underFace[1], underFace[3], underFace[4], underFace[5], underFace[7]])
            
            #Check check for full
            if(countFront == 9 and countRight == 9 and countBack == 9 and countLeft == 9 and countTop == 9 and countUnder == 9):
                return "full"
            
            #Check for spots
            if(not(frontFace[4] in frontFace[0:4] and frontFace[5:9]) and frontFace[0:4] == frontFace[5:9]):
                if(not(rightFace[4] in rightFace[0:4] and rightFace[5:9]) and rightFace[0:4] == rightFace[5:9]):
                    if(not(backFace[4] in backFace[0:4] and backFace[5:9]) and backFace[0:4] == backFace[5:9]):
                        if(not(leftFace[4] in leftFace[0:4] and leftFace[5:9]) and leftFace[0:4] == leftFace[5:9]):
                            if(not(topFace[4] in topFace[0:4] and topFace[5:9]) and topFace[0:4] == topFace[5:9]):
                                if(not(underFace[4] in underFace[0:4] and underFace[5:9]) and underFace[0:4] == underFace[5:9]):
                                    return "spots"
            

                
            #check for Cross condition
            if(len(frontCorners) ==  1 and len(frontCrosses) == 1):
                if (len(rightCorners)== 1 and len(rightCrosses) == 1):
                    if(len(backCorners) == 1 and len(backCrosses) == 1):
                        if(len(leftCorners) == 1 and len(leftCrosses)== 1):
                            if(len(topCorners) == 1 and len(topCrosses) == 1):
                                if(len(underCorners)==1 and len(underCrosses) == 1):
                                    return "crosses"

#check for illegal cube


        corner1 = [list1[0], list1[29], list1[42]]
        corner2 = [list1[2], list1[9], list1[44]]
        corner3 = [list1[6], list1[35], list1[45]]
        corner4 = [list1[8], list1[15], list1[47]]
        corner5 = [list1[18], list1[11], list1[38]]
        corner6 = [list1[20], list1[27], list1[36]]
        corner7 = [list1[24], list1[17], list1[53]]
        corner8 = [list1[26], list1[33], list1[51]]
                
        if len(set(map(frozenset, [corner1, corner2, corner3, corner4, corner5, corner6, corner7, corner8]))) != 8:
            return "error:  unsolvable cube configuration"
#             if(frontFace[5] == backFace[4] and frontFace[5] != backFace[0] and len(backCorners) != 1):
#                 return "illegal cube"
        return "unknown"
        
def rotateCube(parm,condition):
    cube = parm['cube']
    cube =  cube.split(',')
    checkColors = set(cube)
    if(len(checkColors) != 6):
        return "error: Use exactly 6 different types of color in a cube"
    if(len(cube) != 54):
        return "error: cube is not sized properly"
    frontFace = cube[0:9]
    tempFrontFace = cube[0:9]
    rightFace = cube[9:18]
    tempRightFace = cube[9:18]
    backFace = cube[18:27]
    tempBackFace = cube[18:27]
    leftFace = cube[27:36]
    tempLeftFace = cube[27:36]
    topFace =  cube[36:45]
    tempTopFace = cube[36:45]
    underFace = cube[45:54]
    tempUnderFace = cube[45:54]
    if(parm['face'] == 'f'):
        rightFace[0:9:3] = tempTopFace[6:9]
        underFace[0:3] = tempRightFace[0:9:3]
        leftFace[2:9:3] = tempUnderFace[:3]
        topFace[6:9] = tempLeftFace[2:9:3]
        frontFace[0:3] = tempFrontFace[0:9:3][::-1]
        frontFace[0:9:3] = tempFrontFace[6:9]
        frontFace[6:9] = tempFrontFace[2:9:3][::-1]
        frontFace[2:9:3] = tempFrontFace[0:3]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'F'):
        topFace[6:9] = tempRightFace[0:9:3]
        rightFace[0:9:3] = tempUnderFace[:3]
        underFace[0:3] = tempLeftFace[2:9:3]
        leftFace[2:9:3] = tempTopFace[6:9]
        frontFace[0:3] = tempFrontFace[2:9:3]
        frontFace[2:9:3] = tempFrontFace[6:9][::-1]
        frontFace[6:9] = tempFrontFace[0:9:3]
        frontFace[0:9:3] = tempFrontFace[0:3][::-1]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'r'):
        backFace[0:9:3] = tempTopFace[2:9:3]
        underFace[2:9:3] = tempBackFace[0:9:3]
        frontFace[2:9:3] = tempUnderFace[2:9:3]
        topFace[2:9:3] = tempFrontFace[2:9:3]
        rightFace[0:3] = tempRightFace[0:9:3][::-1]
        rightFace[0:9:3] = tempRightFace[6:9]
        rightFace[6:9] = tempRightFace[2:9:3][::-1]
        rightFace[2:9:3] = tempRightFace[0:3]        
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'R'):
        topFace[2:9:3] = tempBackFace[0:9:3]
        backFace[0:9:3] = tempUnderFace[2:9:3]
        underFace[2:9:3] = tempFrontFace[2:9:3]
        frontFace[2:9:3] = tempTopFace[2:9:3]
        rightFace[0:3] = tempRightFace[2:9:3]
        rightFace[2:9:3] = tempRightFace[6:9][::-1]
        rightFace[6:9] = tempRightFace[0:9:3]
        rightFace[0:9:3] = tempRightFace[0:3][::-1]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'b'):
        leftFace[0:9:3] = tempTopFace[0:3]
        topFace[0:3] = tempRightFace[2:9:3]
        underFace[6:9] = tempLeftFace[0:9:3]
        rightFace[2:9:3] = tempUnderFace[6:9]
        backFace[0:3] = tempBackFace[0:9:3][::-1]
        backFace[0:9:3] = tempBackFace[6:9]
        backFace[6:9] = tempBackFace[2:9:3][::-1]
        backFace[2:9:3] = tempBackFace[0:3]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'B'):
        topFace[0:3] = tempLeftFace[0:9:3]
        rightFace[2:9:3] = tempTopFace[0:3]
        leftFace[0:9:3] = tempUnderFace[6:9]
        underFace[6:9] = tempRightFace[2:9:3]
        backFace[0:3] = tempBackFace[2:9:3]
        backFace[2:9:3] = tempBackFace[6:9][::-1]
        backFace[6:9] = tempBackFace[0:9:3]
        backFace[0:9:3] = tempBackFace[0:3][::-1]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'l'):
        frontFace[0:9:3] = tempTopFace[0:9:3]
        topFace[0:9:3] = tempBackFace[2:9:3]
        backFace[2:9:3] = tempUnderFace[0:9:3]
        underFace[0:9:3] = tempFrontFace[0:9:3]
        leftFace[0:3] = tempLeftFace[0:9:3][::-1]
        leftFace[0:9:3] = tempLeftFace[6:9]
        leftFace[6:9] = tempLeftFace[2:9:3][::-1]
        leftFace[2:9:3] = tempLeftFace[0:3]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'L'):
        topFace[0:9:3] = tempFrontFace[0:9:3]
        frontFace[0:9:3] = tempUnderFace[0:9:3]
        underFace[0:9:3] = tempBackFace[2:9:3]
        backFace[2:9:3] = tempTopFace[0:9:3]
        leftFace[0:3] = tempLeftFace[2:9:3]
        leftFace[2:9:3] = tempLeftFace[6:9][::-1]
        leftFace[6:9] = tempLeftFace[0:9:3]
        leftFace[0:9:3] = tempLeftFace[0:3][::-1]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 't'):
        frontFace[0:3] = tempRightFace[:3]
        rightFace[0:3] = tempBackFace[:3]
        backFace[0:3] = tempLeftFace[:3]
        leftFace[0:3] = tempFrontFace[:3]
        topFace[0:3] = tempTopFace[0:9:3][::-1]
        topFace[0:9:3] = tempTopFace[6:9]
        topFace[6:9] = tempTopFace[2:9:3][::-1]
        topFace[2:9:3] = tempTopFace[0:3]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'T'):
        frontFace[0:3] = tempLeftFace[:3]
        leftFace[0:3] = tempBackFace[:3]
        backFace[0:3] = tempRightFace[:3]
        rightFace[0:3] = tempFrontFace[:3]
        topFace[0:3] = tempTopFace[2:9:3]
        topFace[2:9:3] = tempTopFace[6:9][::-1]
        topFace[6:9] = tempTopFace[0:9:3]
        topFace[0:9:3] = tempTopFace[0:3][::-1]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    elif(parm['face'] == 'u'):
        frontFace[6:9] = tempLeftFace[6:9]
        leftFace[6:9] = tempBackFace[6:9]
        backFace[6:9] = tempRightFace[6:9]
        rightFace[6:9] = tempFrontFace[6:9]
        underFace[0:3] = tempUnderFace[0:9:3][::-1]
        underFace[0:9:3] = tempUnderFace[6:9]
        underFace[6:9] = tempUnderFace[2:9:3][::-1]
        underFace[2:9:3] = tempUnderFace[0:3]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    
    elif(parm['face'] == 'U'):
        frontFace[6:9] = tempRightFace[6:9]
        rightFace[6:9] = tempBackFace[6:9]
        backFace[6:9] = tempLeftFace[6:9]
        leftFace[6:9] = tempFrontFace[6:9]
        underFace[0:3] = tempUnderFace[2:9:3]
        underFace[2:9:3] = tempUnderFace[6:9][::-1]
        underFace[6:9] = tempUnderFace[0:9:3]
        underFace[0:9:3] = tempUnderFace[0:3][::-1]
        rotatedCube = frontFace + rightFace + backFace + leftFace + topFace + underFace
    return rotatedCube


    
