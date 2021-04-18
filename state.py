class State:

    def __init__(self, robot: tuple, butters=[]):
        self.robot = robot
        self.butters = butters

    def __eq__(self, other):
        return self.butters == other.butters and self.robot == other.robot

    def __str__(self):
        return 'Robot at: ' + str(self.robot) + ' Butters at: ' + str(self.butters)

    def __repr__(self):
        return self.__str__()
