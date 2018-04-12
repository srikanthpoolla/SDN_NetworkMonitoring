from parent import Parent


class Child(Parent):

    def __init__(self, name, age, qualification):
        Parent.__init__(self, name, age, qualification)


hero = Child("Billy", 28, 'Graduate')
print '------------- Details are-------------'
print hero.name
print hero.defense
print hero.health