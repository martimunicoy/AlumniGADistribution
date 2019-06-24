from .Affinities import AffinitiesBuilder
from . import Constants as co


class Alumnus(object):
    def __init__(self, name, affinity_data, alumnus_id=-1):
        self._name = name
        self._affinity_data = affinity_data
        self._id = alumnus_id
        self._classroom = None

    @property
    def name(self):
        return self._name

    @property
    def affinity_data(self):
        return self._affinity_data

    @property
    def id(self):
        return self._id

    @property
    def classroom(self):
        return self._classroom

    def __eq__(self, other):
        return (self.name, self.id) == (other.name, other.id)

    def __ne__(self, other):
        return not(self == other)

    def __hash__(self):
        return hash((self.name, self.id))

    def __str__(self):
        output = "ID {}: {}\n".format(self.id, self.name)
        for affinity in self.affinity_data:
            output += "  - {}\n".format(affinity)

        return output

    def setClassroom(self, classroom):
        self._classroom = classroom

    def unsetClassroom(self):
        self._classroom = None

    def hasAClassroomAssigned(self):
        return self.classroom is not None


class AlumnusBuilder(object):
    def __init__(self, fields):
        self._fields = list(fields)
        self.__counter = 0

    @property
    def fields(self):
        return self._fields

    def checkFieldValues(self, field_values):
        if ((len(self.fields) - 1) * co.NUMBER_OF_CHOICES_PER_FIELD + 1 !=
                len(field_values)):
            return False

        for value in field_values:
            if (len(value) == 0):
                return False

        return True

    def build(self, field_values):
        okay = self.checkFieldValues(field_values)
        if (not okay):
            raise NameError("El número de camps de la taula no coincideix " +
                            "amb la línia de l\'arxiu csv: " +
                            str(field_values))

        # Get name and remove it from field_values list
        for i, (ordered_field, field) in enumerate(zip(self.fields,
                                                       field_values)):
            if (ordered_field.upper() == "NOM"):
                alumnus_name = field
                del(field_values[i])
                break
        else:
            raise NameError("El camp \'Nom\' és obligatori a la taula de "
                            "l\'arxiu csv. Camps llegits: " +
                            str(self.fields))

        affinities_builder = AffinitiesBuilder(self.fields, field_values)
        affinities = affinities_builder.build()

        self.__counter += 1

        return Alumnus(alumnus_name, affinities, self.__counter)
