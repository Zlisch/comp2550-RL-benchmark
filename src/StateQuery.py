import time

from Box2D import b2PolygonShape, b2Vec2, b2Shape, b2QueryCallback, b2AABB


def testPointPolygon(shape: b2PolygonShape, rel_point: b2Vec2, pos: b2Vec2):
    """
    Checks if the given point is inside the shape
    Imagine that you draw a line from the point you are testing
    straight upwards, then if that line intersects an odd
    numbers of times, then you know the point is in the shape.
    An even number of times means entry(1) + exit(1) = 2 hence outside
    """

    # Iterate over edges and test for intersections:
    # odd number of intersections means inside. even number means outside
    intersections = 0
    for i in range(0, len(shape.vertices)):
        if (rel_point[0] < min(shape.vertices[i][0], shape.vertices[i - 1][0])) or \
                (rel_point[0] > max(shape.vertices[i][0], shape.vertices[i - 1][0])):
            continue
        grad = (shape.vertices[i][1] - shape.vertices[i - 1][1]) / (shape.vertices[i][0] - shape.vertices[i - 1][0])
        int_y = shape.vertices[i][1] - (shape.vertices[i][0] * grad) + (rel_point[0] * grad)
        if int_y > rel_point[1]:
            intersections += 1
    # print("Intersections: " + str(intersections))
    return (intersections % 2) == 1


def getBoundingBox(shape: b2PolygonShape):
    """ Assumes the type of the object is a polygon """
    if shape.type != b2Shape.e_polygon:
        return

    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0

    # Loop over vertices
    for v in shape.vertices:
        if v[0] < xmin:
            xmin = v[0]
        elif v[0] > xmax:
            xmax = v[0]

        if v[1] < ymin:
            ymin = v[1]
        elif v[1] > ymax:
            ymax = v[1]

    return (xmin, xmax, ymin, ymax)


def queryPointShape(shape: b2Shape, point: b2Vec2, pos: b2Vec2) -> bool:
    """
    Returns true if the point is contained in the shape
    """

    if shape.type == b2Shape.e_circle:
        # Circle is easy:
        radius = shape.radius
        # Get euclidean distance:
        dis = pow(((point[0] - pos[0]) ** 2) + ((point[1] - pos[1]) ** 2), 0.5)
        return dis < radius
    elif shape.type == b2Shape.e_polygon:
        # First check bounding box:
        (xmin, xmax, ymin, ymax) = getBoundingBox(shape)
        # Get relative point:
        rel_point = (point[0] - pos[0], point[1] - pos[1])
        if (xmin <= rel_point[0]) & (xmax >= rel_point[0]) & (ymin <= rel_point[1]) & (ymax >= rel_point[1]):
            # Do more thorough intersection test:
            print("Doing more thorough test")
            return testPointPolygon(shape, rel_point, pos)
        else:
            return False

    return


def queryPoint2(self, point: b2Vec2):
    vec = [0, 0, 0, 0]

    timeprev = time.time()

    # Statics:
    for b in self.static_objects:
        exitloop = False
        for f in b.fixtures:
            if queryPointShape(f.shape, point, b.position):
                vec[0] = 1
                exitloop = True
                break  # exit loop
        if exitloop: break

    # Dynamic Blues:
    for b in self.safe_objects:
        exitloop = False
        for f in b.fixtures:
            if queryPointShape(f.shape, point, b.position):
                vec[1] = 1
                exitloop = True
                break  # exit loop
        if exitloop: break

    # Dynamic Reds:
    for b in self.danger_objects:
        exitloop = False
        for f in b.fixtures:
            if queryPointShape(f.shape, point, b.position):
                vec[2] = 1
                exitloop = True
                break  # exit loop
        if exitloop: break

    # Agent:
    if queryPointShape(self.agent.fixtures[0].shape, point, b.position):
        vec[3] = 1

    timetaken = time.time() - timeprev
    timetaken *= 10 ** 3

    return vec


def queryPoint(self, point: b2Vec2):
    """
    Return a one-hot vector (list) representing the
    objects present at a given point (b2Vec is the same as a pair)
    (static, safe, danger, agent)
    """

    potential_bodies = []

    class myQueryCallback(b2QueryCallback):
        """ Helps reduce computation time by only checking necessary bodies """

        def __init__(self):
            b2QueryCallback.__init__(self)

        def ReportFixture(self, fixture):
            potential_bodies.append(fixture.body)
            return True

    query = myQueryCallback()

    timeprev = time.time()

    self.world.QueryAABB(query, b2AABB(lowerBound=(point[0] - 0.0001, point[1] - 0.0001),
                                       upperBound=(point[0] + 0.0001, point[1] + 0.0001)))

    timetaken = time.time() - timeprev
    timetaken *= 10 ** 3
    # print("Time to query AABB: " + str(timetaken) + " millis. Num: " + str(len(potential_bodies)))
    # if timetaken > 0.01:
    #     print("Time to query AABB: " + str(timetaken) + " millis. Num: " + str(len(potential_bodies)))

    vec = [0, 0, 0, 0]

    # print("Number of potential objects: " + str(len(potential_bodies)))

    for b in potential_bodies:
        exitloop = False
        for f in b.fixtures:
            tp = f.shape.TestPoint(point)
            if tp:
                if b in self.static_objects:
                    vec[0] = 1
                elif b in self.safe_objects:
                    vec[1] = 1
                elif b in self.danger_objects:
                    vec[2] = 1
                elif b == self.agent:
                    vec[3] = 1
                exitloop = True
                break  # exit loop
        if exitloop: break

    return vec

    """
    # Statics:                
    for b in self.static_objects:   
        exitloop = False
        for f in b.fixtures:  
            if f.TestPoint(point):            
                vec[0] = 1
                exitloop = True
                break   # exit loop
        if exitloop: break

    # Dynamic Blues:        
    for b in self.safe_objects:   
        exitloop = False
        for f in b.fixtures:  
            if f.TestPoint(point):            
                vec[1] = 1
                exitloop = True
                break   # exit loop
        if exitloop: break

    # Dynamic Reds:
    for b in self.danger_objects:   
        exitloop = False
        for f in b.fixtures:  
            if f.TestPoint(point):            
                vec[2] = 1
                exitloop = True
                break   # exit loop
        if exitloop: break

    # Agent:
    if self.agent.fixtures[0].TestPoint(point):
        vec[3] = 1

    return vec
    """