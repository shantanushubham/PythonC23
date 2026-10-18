class DemocraticCountry:

    def __init__(self, name, president, vice_president):
        self.name = name
        self.government = self.Government(president, vice_president)

    def get_name(self):
        return self.name

    class Government:
        def __init__(self, president, vice_president):
            self.president = president
            self.vice_president = vice_president


class DictatorshipCountry:

    def __init__(self, name, dictator):
        self.name = name
        self.government = self.Government(dictator)

    def get_name(self):
        return self.name

    class Government:
        def __init__(self, dictator):
            self.dictator = dictator
            

democratic_country = DemocraticCountry("United States", "Donald Trump", "Mike Pence")
print(democratic_country.government.president)

dictatorship_country = DictatorshipCountry("North Korea", "Kim Jong Un")
print(dictatorship_country.government.dictator)

print(type(democratic_country.government) == type(dictatorship_country.government))