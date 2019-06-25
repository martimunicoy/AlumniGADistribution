from Utils.Evaluation import ScoreCalculator


class Optimizer(object):
    def __init__(self, class_distribution, iterations):
        self._class_distribution = class_distribution
        self._score_calculator = ScoreCalculator()
        self._best_score = None
        self._best_classrooms = None
        self._iterations = iterations

    @property
    def class_distribution(self):
        return self._class_distribution

    @property
    def score_calculator(self):
        return self._score_calculator

    @property
    def best_score(self):
        return self._best_score

    @property
    def best_classrooms(self):
        return self._best_classrooms

    @property
    def iterations(self):
        return self._iterations

    @property
    def type(self):
        return self._type


class BruteForceOptimizer(Optimizer):
    def __init__(self, class_distribution, iterations):
        Optimizer.__init__(self, class_distribution, iterations)
        self._type = "FORÇA BRUTA"

    def optimize(self):
        print("Optimitzant amb {}:".format(self.type.lower()))

        for iteration in range(0, self.iterations):
            classrooms = self.class_distribution.distributeAlumni()

            total_score = 0.
            for classroom in classrooms:
                self.score_calculator.setClassroom(classroom)
                self.score_calculator.calculate()
                total_score += self.score_calculator.getClassroomResult()

            if (self.best_score is None or self.best_score < total_score):
                if (self.best_score is None):
                    print(" - Iteració {:6d}: ".format(iteration) +
                          "            {: 8.2f}".format(total_score))
                else:
                    print(" - Iteració {:6d}: ".format(iteration) +
                          "{: 8.2f} -> {: 8.2f}".format(self.best_score,
                                                        total_score))

                self._best_score = total_score
                self._best_classrooms = classrooms

    def showResults(self):
        if (self.best_classrooms is None):
            return

        for classroom in self.best_classrooms:
            print(classroom)

        for classroom in self.best_classrooms:
            self.score_calculator.setClassroom(classroom)
            self.score_calculator.calculate()
            self.score_calculator.showResults()

    def writeBestClassDistribution(self, path):
        if (self.score_calculator.results is None):
            return

        output = ""
        total_score = 0.

        for classroom in self.best_classrooms:
            output += "-------------------------------------------\n|"
            if ((43 - len(classroom.name)) % 2 != 0):
                extra = 1
            else:
                extra = 0
            for i in range(0, int((43 - len(classroom.name)) / 2.) - 1):
                output += " "
            output += classroom.name
            for i in range(0,
                           int((43 - len(classroom.name)) / 2.) - 1 + extra):
                output += " "
            output += "|\n-------------------------------------------\n"
            self.score_calculator.setClassroom(classroom)
            self.score_calculator.calculate()
            for alumnus, score in self.score_calculator.results.items():
                output += " - {}: ".format(alumnus.name)
                for i in range(len(alumnus.name), 30):
                    output += " "
                output += "{: 8.2f}\n".format(score)
            total_score += self.score_calculator.getClassroomResult()
            output += "-------------------------------------------\n"
            output += " - Total de la classe:             {: 8.2f}\n".format(
                self.score_calculator.getClassroomResult())
            output += "-------------------------------------------\n"
            output += '\n'

        output += "-------------------------------------------\n"
        output += " - Puntuació global:               {: 8.2f}\n".format(
            total_score)
        output += "-------------------------------------------\n"
        output += '\n'

        with open(path, 'w') as file:
            file.write(output)

        print("Resultats guardats a: \'{}\'".format(path))
