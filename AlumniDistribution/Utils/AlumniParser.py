from .Alumnus import AlumnusBuilder
from . import Constants as co


class AlumniParser(object):
    def __init__(self, input_path):
        self._input_path = input_path

    @property
    def input_path(self):
        return self._input_path

    def _extractFieldsFromLine(self, line):
        ordered_fields = []

        line = line.strip()
        fields = line.split(',')

        for field in fields:
            if (len(field) == 0):
                continue
            if (field.upper() in co.FIELDS):
                ordered_fields.append(field)
                continue
            raise NameError("Un dels camps del fitxer csv es " +
                            "desconegut: \'" + field +
                            "\'. Els camps coneguts son: " +
                            str(co.FIELDS))

        return ordered_fields

    def getAlumni(self):
        alumni = []

        with open(self.input_path, 'r') as f:
            # Read first line
            fields_line = f.readline()
            fields = self._extractFieldsFromLine(fields_line)

            alumnus_builder = AlumnusBuilder(fields)

            # Read all next lines
            for line in f:
                line = line.strip()
                field_values = line.split(',')

                okay = alumnus_builder.checkFieldValues(field_values)

                if (okay):
                    alumnus = alumnus_builder.build(field_values)
                    alumni.append(alumnus)
                else:
                    print("Atencio: ignorant linia amb un format inconsistent")
                    print(" \'" + line + "\'")

        return alumni
