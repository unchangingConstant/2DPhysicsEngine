#Will handle logic for collisions
import numpy as np
import math as m
import environment
import entity

def normalize(vector: np.array) -> np.array:
    '''
    Normalizes the given vector.

    :param vector: A 2 dimensional vector.
    :type vector: ``np.array``
    :return: The given vector normalized.
    :rtype: ``np.array``
    '''

    normalizedVector = vector / np.sqrt(np.sum(vector ** 2))
    return normalizedVector

def findNormalForce(motionVector: np.array, surface: environment.Surface) -> np.array:
    '''
    Takes a motionVector (representing the vector formed by an entity's
    _priorPosition and _position) and a surface object, then returns the
    component of the motionVector normal to the surface.

    :param motionVector: A 2 dimensional vector.
    :param surface: A surface object.
    :type motionVector: ``np.array``
    :type surface: ``environment.Surface``
    :return: The component of the motionVector normal to the surface.
    :rtype: ``np.array``
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

def pointInBounds(point: np.array, xBounds: list[float], yBounds: list[float]) -> bool:
    """
    Takes a point and two tuples, representing upper/lower x/y bounds, respectively, and returns a boolean
    indicating whether the point is located in those bounds. It will return true even if the point is one
    pixel out of bounds in either direction.

    :param point: A point in 2D space.
    :param xBounds: The lower/upper x bounds (order doesn't matter)
    :param yBounds: The lower/upper y bounds (order doesn't matter)
    :type point: np.array
    :type xBounds: ``list[float]``
    :type yBounds: ``list[float]``
    :return: A boolean indicating whether the point is in the given bounds.
    :rtype: ``bool``
    """
    xBounds.sort()
    yBounds.sort()

    inXBounds = (point[0] >= xBounds[0] - 0.1 and point[0] <= xBounds[1] + 0.1)
    inYBounds = (point[1] >= yBounds[0] - 0.1 and point[1] <= yBounds[1] + 0.1)

    if (inXBounds and inYBounds):
        return True
    return False

def findCollisionPoint(entity: entity.EntityInterface, surface: environment.Surface) -> np.array:
    """
    Finds the collision point of an entity's trajectory and an surface. If there is no collision point, 
    the function returns NoneType.

    :param entity: The entity that might collied with a surface
    :param surface: The surface that the entity might collide with
    :type entity: ``entity.EntityInterface``
    :type surface: ``environment.Surface``
    :return: If there is a collision point, a ``np.array`` with the point. Otherwise, ``None``.
    :rtype: ``np.array`` | ``None``
    """

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

        xPathBound = [entity.getPriorPosition()[0], entity.getPosition()[0]]
        yPathBound = [entity.getPriorPosition()[1], entity.getPosition()[1]]

        xSurfaceBound = [surface.edge1[0], surface.edge2[0]]
        ySurfaceBound = [surface.edge1[1], surface.edge2[1]]

        entityPathIntersects = pointInBounds(collisionPoint, xPathBound, yPathBound)
        surfaceIntersects = pointInBounds(collisionPoint, xSurfaceBound, ySurfaceBound)

        if entityPathIntersects and surfaceIntersects:
            return collisionPoint
        return None

    except np.linalg.LinAlgError:
        return None

def findClosestPoint(objectPosition: np.array, positions: list[np.array]) -> np.array:
    """
    Takes a  position and a list of points. Then finds the point in the list closest to the given position.

    :param objectPosition: The position
    :param positions: The list of positions you want to search
    :type objectPosition: ``np.array``
    :type positions: ``list[np.array]``
    :return: The point in the list closest to the object position
    :rtype: ``np.array``
    """

    closestPoint = positions[0]
    for position in positions:
        distance = np.linalg.norm(objectPosition - position)
        closestPointDistance = np.linalg.norm(objectPosition - closestPoint)
        if distance < closestPointDistance:
            closestPoint = position
    
    return closestPoint

def findNumpyArrayIndex(list: np.array, item: int | float) -> int:
    """
    Finds the index of an item within a numpy array

    :param list: The numpy array
    :param item: The item within the numpy array whose index you want to find
    :type list: ``np.array``
    :type item: ``int | float``
    :return: The index of the item within the array
    :rtype: ``int | float``
    """

    for i in range(0, len(list)):
        if (item == list[i]).all():
            return i

def resolveMotion(entity: entity.EntityInterface, environment: list[environment.Surface]):
    """
    Takes an entity and an environment. The environment will be a list of surface objects to represent
    the "environment". It then calculates all collisions and entity movements that will take place within
    a single frame and applies them.
    :param entity: The entity whose motion you want to resolve
    :param environment: A list of surface objects to represent the entity's environment
    :type entity: ``entity.EntityInterface``
    :type environment: ``list[environment.Surface]``
    """

    remainingFrametime = 1

    while remainingFrametime > 0:
        
        entity.move(entity.getVelocity() * remainingFrametime)
        potentialCollisionPoints = []
        potentialSurfaces = []

        for surface in environment:
            potentialCollisionPoint = findCollisionPoint(entity, surface)
            if potentialCollisionPoint is not None:
                potentialCollisionPoints.append(potentialCollisionPoint)
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