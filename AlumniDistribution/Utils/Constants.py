NUMBER_OF_CHOICES_PER_FIELD = 3
FIELDS = ["NOM", "TREBALLA MILLOR AMB", "TREBALLA PITJOR AMB",
          "JUGA MILLOR AMB", "JUGA PITJOR AMB"]
AFFINITY_TYPES = ["TREBALLA MILLOR AMB", "TREBALLA PITJOR AMB",
                  "JUGA MILLOR AMB", "JUGA PITJOR AMB"]
AFFINITY_WEIGTHS = {"TREBALLA MILLOR AMB": +20.,
                    "TREBALLA PITJOR AMB": -1.,
                    "JUGA MILLOR AMB": +15.,
                    "JUGA PITJOR AMB": -1.}
MATCH_EQUILIBRIUM_WEIGTH = 10
