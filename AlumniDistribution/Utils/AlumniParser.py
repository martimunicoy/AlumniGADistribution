from .Alumni import AlumnusBuilder
from . import Constants as co


class AlumniParser(object):
    def __init__(self, input_path):
        self._input_path = input_path

    @property
    def input_path(self):
        return self._input_path

    def _extractFieldFromLine(self, line):
        ordered_fields = []

        fields = line.split(',')

        for field in fields:
            if (len(field) == 0):
                continue
            if (field.upper() in co.FIELDS):
                ordered_fields.append(field)
                continue
            raise NameError("Un dels camps del fitxer csv es " +
                            "desconegut. Els camps coneguts son:" +
                            co.KEY_FIELDS)

        return ordered_fields

    def getAlumni(self):
        alumni = []

        with open(self.input_path, 'r') as f:
            # Read first line
            fields_line = f.readline()
            ordered_fields = self._extractFieldsFromLine(fields_line)

            alumnus_builder = AlumnusBuilder(ordered_fields)

            # Read all next lines
            for line in f:
                fields = line.split(',')
                alumnus = alumnus_builder(fields)
                alumni.append(alumnus)



        return


