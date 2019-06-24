from . import Constants as co


class Affinity(object):
    def __init__(self, affinity_type):
        if (affinity_type.upper() not in co.AFFINITY_TYPES):
            raise NameError("Tipus d\'afinitat desconeguda: " +
                            "{}".format(affinity_type))
        self._type = affinity_type
        self._priority = {}
        self._weigth = co.AFFINITY_WEIGTHS[affinity_type.upper()]

    @property
    def type(self):
        return self._type

    @property
    def priority(self):
        return self._priority

    @property
    def weigth(self):
        return self._weigth

    def __iter__(self):
        self.__current = 0
        return self

    def __next__(self):
        if (self.__current == len(self.priority)):
            raise StopIteration
        else:
            self.__current += 1
            return list(self.priority.items())[self.__current - 1]

    def __str__(self):
        output = "{}: ".format(self.type)

        for i, (priority, value) in enumerate(self.priority.items()):
            output += "{}.{} ".format(priority, value)

        return output

    def addPriority(self, priority_number, value):
        try:
            priority_number = int(priority_number)
            value = str(value)
        except TypeError:
            raise TypeError("Paràmetres de prioritat incorrectes")

        self._priority[priority_number] = value

    def resetPriority(self):
        self._priority = {}


class AffinitiesBuilder(object):
    def __init__(self, fields, field_values):
        self._fields = fields
        self._field_values = field_values

    @property
    def fields(self):
        return self._fields

    @property
    def field_values(self):
        return self._field_values

    def build(self):
        affinities = []
        field_index = 0

        for field in self.fields:
            field = field.strip()

            if (field.upper() == "NOM"):
                continue

            affinity = Affinity(field)

            for priority_number in range(0, co.NUMBER_OF_CHOICES_PER_FIELD):
                value_index = field_index * \
                    co.NUMBER_OF_CHOICES_PER_FIELD + priority_number
                field_value = self.field_values[value_index].strip()
                affinity.addPriority(priority_number + 1, field_value)

            affinities.append(affinity)
            field_index += 1

        return affinities
