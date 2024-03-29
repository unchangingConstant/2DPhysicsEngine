#Will handle logic for collisions
import numpy as np
import math as m
import environment
import entity

def normalize(vector: np.array([float, float])):
    '''
    Normalizes the given vector.

    :param vector: A 2 dimensional vector.
    :type vector: np.array([float, float])
    :return: The given vector normalized.
    :rtype: np.array([float, float])

    '''

    normalizedVector = vector / np.sqrt(np.sum(vector ** 2))
    return normalizedVector

def findNormalForce(motionVector: np.array([float, float]), surface: environment.Surface):
    '''
    Takes a motionVector (representing the vector formed by an entity's
    ``_priorPosition`` and ``_position``) and a surface object, then returns the
    component of the motionVector normal to the surface.

    :param motionVector: A 2 dimensional vector.
    :param surface: A surface object.
    :type motionVector: np.array([float, float])
    :type surface: environment.surface()
    :return: The component of the motionVector normal to the surface.
    :rtype: np.array([float, float])

    '''

    surfaceVector = normalize(np.array([surface.edge1[1] - surface.edge2[1], surface.edge2[0] - surface.edge1[0]]))

    print(surface.edge1[1], end = ' - ')
    print(surface.edge2[1], end = ' = ')
    print(surfaceVector[0], end = ': ')
    print(surfaceVector, end = ' ')
    print("surface vector!")

    motionSurfaceDotProduct = np.dot(motionVector, surfaceVector)
    surfaceVectorDot = np.dot(surfaceVector, surfaceVector)

    normalForce = (motionSurfaceDotProduct / surfaceVectorDot) * surfaceVector * - 1

    return normalForce

def pointInBounds(point: np.array([float, float]), xBounds: (float, float), yBounds: (float, float)):
    """
    Takes a point and two tuples, representing upper/lower x/y bounds, respectively, and returns a boolean
    indicating whether the point is located in those bounds.

    :param point: A point in 2D space.
    :param xBounds: The upper/lower x bounds (the order doesn't matter)
    :param yBounds: The upper/lower y bounds (the order doesn't matter)
    :type point: np.array(float, float)
    :type xBounds: (float, float)
    :type yBounds: (float, float)
    :return: A boolean indicating whether the point is in the given bounds.
    :rtype: bool

    """

    inXBounds1 = (point[0] <= xBounds[0] and point[0] >= xBounds[1])
    inXBounds2 = (point[0] >= xBounds[0] and point[0] <= xBounds[1])

    inYBounds1 = (point[1] <= yBounds[0] and point[1] >= yBounds[1])
    inYBounds2 = (point[1] >= yBounds[0] and point[1] <= yBounds[1])

    if not (inXBounds1 or inXBounds2):
        return False
    if not (inYBounds1 or inYBounds2):
        return False
    return True

def collisionDetected(entity: entity.EntityInterface, surface: environment.Surface):

    eDeltaX = entity.getVelocity()[0]
    eDeltaY = entity.getVelocity()[1]
    motionTrace = np.array([eDeltaX, - eDeltaY])
    eConstant = (eDeltaX * entity.getPriorPosition()[1]) - (eDeltaY * entity.getPriorPosition()[0])

    sDeltaX = surface.edge2[0] - surface.edge1[0]
    sDeltaY = surface.edge2[1] - surface.edge1[1]
    edgeTrace = np.array([sDeltaX, - sDeltaY])
    sConstant = (sDeltaX * surface.edge1[1]) - (sDeltaY * surface.edge1[0])

    motionTrace = (motionTrace[0], motionTrace[1])
    edgeTrace = (edgeTrace[0], edgeTrace[1])

    collisionMatrix = np.array([motionTrace, edgeTrace])
    eVector = np.array([eConstant, sConstant])

    try:
        collisionPoint = np.linalg.solve(collisionMatrix, eVector)
        collisionPoint = np.array([collisionPoint[1], collisionPoint[0]])

        xPathBound = (entity.getPriorPosition()[0], entity.getPosition()[0])
        yPathBound = (entity.getPriorPosition()[1], entity.getPosition()[1])

        xSurfaceBound = (surface.edge1[0], surface.edge2[0])
        ySurfaceBound = (surface.edge1[1], surface.edge2[1])

        entityPathIntersects = pointInBounds(collisionPoint, xPathBound, yPathBound)
        surfaceIntersects = pointInBounds(collisionPoint, xSurfaceBound, ySurfaceBound)

        if entityPathIntersects and surfaceIntersects:
            return (True, collisionPoint)
        return (False, 0)

    except np.linalg.LinAlgError:
        return (False, 0)

def findClosestPoint(objectPosition, positions):
    
    closestPoint = positions[0]
    for position in positions:
        distance = np.linalg.norm(objectPosition - position)
        closestPointDistance = np.linalg.norm(objectPosition - closestPoint)
        if distance < closestPointDistance:
            closestPoint = position
    
    return position

def findNumpyArrayIndex(list, item):

    for i in range(0, len(list)):
        if (item == list[i]).all():
            return i

def resolveMotion(entity, environment):
    
    remainingFrametime = 1

    while remainingFrametime > 0:
        
        entity.setPriorPosition(entity.getPosition())
        entity.modPosition(entity.getVelocity() * remainingFrametime)
        potentialCollisionPoints = []
        potentialSurfaces = []

        for surface in environment:
            colTuple = collisionDetected(entity, surface)
            if colTuple[0]:
                potentialCollisionPoints.append(colTuple[1])
                potentialSurfaces.append(surface)

        if len(potentialCollisionPoints) == 0:
            break
        
        collisionPoint = findClosestPoint(entity.getPosition(), potentialCollisionPoints)
        surface = potentialSurfaces[findNumpyArrayIndex(potentialCollisionPoints, collisionPoint)]

        entity.setPosition(collisionPoint)
        distanceTravelled = np.linalg.norm(entity.getPriorPosition() - collisionPoint)
        remainingFrametime -= distanceTravelled / m.sqrt(np.dot(entity.getVelocity(), entity.getVelocity()))

        normalForce = findNormalForce(entity.getVelocity(), surface)
        entity.modVelocity(normalForce * (1 + entity.elasticity))
        entity.modPosition(normalize(normalForce))