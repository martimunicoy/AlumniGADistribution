
class Score(object):
    def __init__(self, score_value):
        self._value = score_value

    @property
    def value(self):
        return self._value


class ScoreCalculator(object):
    def __init__(self, classroom=None):
        self._classroom = classroom
        self._results = None

    @property
    def classroom(self):
        return self._classroom

    @property
    def results(self):
        return self._results

    def setClassroom(self, classroom):
        self._results = None
        self._classroom = classroom

    def calculate(self):
        if (self._classroom is None):
            return None

        self._results = {}

        for alumnus in self._classroom:
            self._results[alumnus] = self.getAlumnusScore(alumnus)

    def getAlumnusScore(self, alumnus):
        score = 0.
        for affinity in alumnus.affinity_data:
            for priority, mate_name in affinity:
                if (self.classroom.containsName(mate_name)):
                    score += float(affinity.weigth) / float(priority)

        return score

    def showResults(self):
        if (self.results is None):
            return

        print("Resultats de la classe {}:".format(self.classroom.name))
        for alumnus, score in self.results.items():
            print(" - {}: {}".format(alumnus.name, score))
        print(" - Total score: {}".format(self.getClassroomResult()))


    def getClassroomResult(self):
        total_score = 0.
        for score in self.results.values():
            total_score += score

        return total_score
