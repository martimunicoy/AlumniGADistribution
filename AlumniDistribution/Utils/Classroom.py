import random


class Classroom(object):
    def __init__(self, name):
        self._name = name
        self._alumni = set()

    @property
    def name(self):
        return self._name

    @property
    def alumni(self):
        return self._alumni

    def __iter__(self):
        self.__current = 0
        self.__alumni_list = list(self._alumni)
        return self

    def __next__(self):
        if (self.__current == len(self.__alumni_list)):
            raise StopIteration
        else:
            self.__current += 1
            return self.__alumni_list[self.__current - 1]

    def __str__(self):
        output = "Classe {}\n".format(self.name)
        for alumnus in self.alumni:
            output += " - {}\n".format(alumnus.name)

        return output[:-1]

    def addAlumnus(self, alumnus):
        self._alumni.add(alumnus)
        alumnus.setClassroom(self)

    def contains(self, alumnus):
        return alumnus in self.alumni

    def containsName(self, alumnus_name):
        return alumnus_name in [i.name for i in self.alumni]


class ClassDistribution(object):
    def __init__(self, alumni, classroom_names, seed=None, verbose=False):
        self._alumni = alumni
        self._conditions = []
        self.verbose = verbose

        if (len(classroom_names) < 2):
            raise NameError("Com a mínim, s\'ha de crear dues classes")
        self._classroom_names = classroom_names

        # Initiate random generator
        random.seed(seed)

    @property
    def alumni(self):
        return self._alumni

    @property
    def conditions(self):
        return self._conditions

    @property
    def classroom_names(self):
        return self._classroom_names

    def addCondition(self, condition):
        self._conditions.append(condition)

    def removeConditions(self, conditions):
        self._conditions = []

    def distributeAlumni(self):
        # Unset classroom for all alumni
        for alumnus in self.alumni:
            alumnus.unsetClassroom()

        # Create classrooms
        classrooms = []
        for name in self.classroom_names:
            classrooms.append(Classroom(name))

        # Get number of classrooms
        n_classrooms = len(classrooms)

        # First, apply conditions
        if (self.verbose):
            print(" - Aplicant les condicions prèvies")
        for condition in self.conditions:
            condition.applyTo(classrooms)

        # Secondly, assign the rest of alumni to classrooms
        alumni_not_assigned_yet = []
        for alumnus in self.alumni:
            if (alumnus.hasAClassroomAssigned()):
                continue
            alumni_not_assigned_yet.append(alumnus)

        # Randomly shuffle them
        random.shuffle(alumni_not_assigned_yet)

        alumni_divisions = [alumni_not_assigned_yet[i::n_classrooms]
                            for i in range(n_classrooms)]

        for alumni_division, classroom in zip(alumni_divisions, classrooms):
            for alumnus in alumni_division:
                classroom.addAlumnus(alumnus)

        return classrooms

    def getAlumnusByName(self, alumnus_name):
        for alumnus in self.alumni:
            if (alumnus.name.upper() == alumnus_name.upper()):
                return alumnus

        raise NameError("No s\'ha trobat cap alumne amb el nom " +
                        "{}".format(alumnus_name))


def conditionBuilder(condition_type, alumnus1, alumnus2):
    if (condition_type == "JUNTS"):
        return TogetherCondition(alumnus1, alumnus2)

    if (condition_type == "SEPARATS"):
        return SplittedCondition(alumnus1, alumnus2)

    raise TypeError("Tipus de condició desconeguda: {}".format(
        condition_type))


def addConditionsFromFile(path, class_distribution):
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()

            if ((len(line.split(',')) < 3) or (len(line.split(',')) > 3)):
                continue

            condition_type, alumnus_name1, alumnus_name2 = line.split(',')

            alumnus1 = class_distribution.getAlumnusByName(alumnus_name1)
            alumnus2 = class_distribution.getAlumnusByName(alumnus_name2)

            condition = conditionBuilder(condition_type, alumnus1, alumnus2)

            print("Afegint la condició ->", condition)
            class_distribution.addCondition(condition)


class Condition(object):
    def __init__(self, alumnus1, alumnus2, verbose=False):
        self._alumnus1 = alumnus1
        self._alumnus2 = alumnus2
        self.verbose = verbose

    @property
    def type(self):
        return self._type

    @property
    def alumnus1(self):
        return self._alumnus1

    @property
    def alumnus2(self):
        return self._alumnus2

    def __str__(self):
        return "{}{}: {} - {}".format(self.type.upper()[0],
                                      self.type.lower()[1:],
                                      self.alumnus1.name,
                                      self.alumnus2.name)

    def _getOtherAlumnus(self, alumnus):
        if (alumnus == self.alumnus1):
            return self.alumnus2
        else:
            return self.alumnus1

    def _getOtherClassroom(self, classroom_to_ignore, classrooms):
        other_classrooms = []
        for classroom in classrooms:
            if (classroom == classroom_to_ignore):
                continue
            other_classrooms.append(classroom)

        return random.choice(other_classrooms)

    def _getPreconstrains(self, classrooms):
        preconstrains = {}

        for classroom in classrooms:
            if (classroom.contains(self.alumnus1)):
                preconstrains[self.alumnus1] = classroom
            if (classroom.contains(self.alumnus2)):
                preconstrains[self.alumnus2] = classroom

        return preconstrains

    def applyTo(self, classrooms):
        if (len(classrooms) < 2):
            raise NameError("Com a mínim hi ha d\'haver dues classes " +
                            "definides")

        # In case any alumnus has already been assigned in a classroom
        preconstrains = self._getPreconstrains(classrooms)

        self._placeAlumni(classrooms, preconstrains)


class TogetherCondition(Condition):
    def __init__(self, alumnus1, alumnus2, verbose=False):
        self._type = "JUNTS"
        Condition.__init__(self, alumnus1, alumnus2, verbose)

    def _checkPreconstrains(self, preconstrains):
        if (len(preconstrains) == 2):
            if (preconstrains[self.alumnus1] != preconstrains[self.alumnus2]):
                return False
        return True

    def _placeAlumni(self, classrooms, preconstrains):
        okay = self._checkPreconstrains(preconstrains)

        if (not okay):
            raise NameError("La condició \'{}\'' ".format(self) +
                            "està en conflicte amb les imposades anteriorment")

        if (len(preconstrains) == 0):
            # Assign a random classroom to alumni
            classroom = random.choice(classrooms)
            if (self.verbose):
                print("  - Afegint {} a {}".format(self.alumnus1.name,
                                                   classroom.name))
                print("  - Afegint {} a {}".format(self.alumnus2.name,
                                                   classroom.name))
            classroom.addAlumnus(self.alumnus1)
            classroom.addAlumnus(self.alumnus2)

        elif (len(preconstrains) == 1):
            # Use the already assigned classroom
            alumnus, classroom = list(preconstrains.items())[0]
            other_alumnus = self._getOtherAlumnus(alumnus)
            if (self.verbose):
                print("  - Afegint {} a {}".format(other_alumnus.name,
                                                   classroom.name))
            classroom.addAlumnus(other_alumnus)


class SplittedCondition(Condition):
    def __init__(self, alumnus1, alumnus2, verbose=False):
        self._type = "SEPARATS"
        Condition.__init__(self, alumnus1, alumnus2, verbose)

    def _checkPreconstrains(self, preconstrains):
        if (len(preconstrains) == 2):
            if (preconstrains[self.alumnus1] == preconstrains[self.alumnus2]):
                return False
        return True

    def _placeAlumni(self, classrooms, preconstrains):
        okay = self._checkPreconstrains(preconstrains)

        if (not okay):
            raise NameError("La condició \'{}\'' ".format(self) +
                            "està en conflicte amb les imposades anteriorment")

        if (len(preconstrains) == 0):
            # Assign a random classroom to an alumni
            classroom = random.choice(classrooms)
            alumnus = random.choice([self.alumnus1, self.alumnus2])
            if (self.verbose):
                print("  - Afegint {} a {}".format(alumnus.name,
                                                   classroom.name))
            classroom.addAlumnus(alumnus)

            # Assign another class to the other alumni
            other_classroom = self._getOtherClassroom(classroom, classrooms)
            other_alumnus = self._getOtherAlumnus(alumnus)
            if (self.verbose):
                print("  - Afegint {} a {}".format(other_alumnus.name,
                                                   other_classroom.name))
            other_classroom.addAlumnus(other_alumnus)

        elif (len(preconstrains) == 1):
            # Use the already assigned classroom
            alumnus, classroom = list(preconstrains.items())[0]

            # Assign another class to the other alumni
            other_classroom = self._getOtherClassroom(classroom, classrooms)
            other_alumnus = self._getOtherAlumnus(alumnus)
            if (self.verbose):
                print("  - Afegint {} a {}".format(other_alumnus.name,
                                                   other_classroom.name))
            other_classroom.addAlumnus(other_alumnus)
