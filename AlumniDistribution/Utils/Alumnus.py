

class Alumnus(object):
    def __init__(self, name, affinity_data):
        self._name = name
        self._affinity_data = affinity_data

    @property
    def name(self):
        return self._name

    @property
    def affinity_data(self):
        return self._affinity_data


class AlumnusBuilder(object):
    def __init__(self, ordered_fields):
        self._ordered_fields = ordered_fields

    @property
    def ordered_fields(self):
        return self._ordered_fields

    def build(self, fields):
        if (len(fields) != self.ordered_fields):
            raise NameError("El numero de camps de la taula no coincideix " +
                            "amb la linia de l\'arxiu csv: " + fields)

        for ordered_field, field in zip(self.ordered_fields, fields):
            if (ordered_field.upper() == "NOM"):
                alumnus_name = field
                break
        else:
            raise NameError("El camp \'Nom\' es obligatori a la taula de "
                            "l\'arxiu csv. Camps llegits: " +
                            self.ordered_fields)

        # @TODO create affinities
        affinities_builder = affinitiesBuilder(orderd_fields, fields)
        affinities = affinities_builder.build()

        return Alumnus(alumnus_name, affinities)

