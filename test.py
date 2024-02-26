
class ahh():

    def __init__(self):
        self.val1 = "green"
        self.val2 = "blue"
        self.val3 = "red"

    def ListVars(self):
        print(dir(self))

class bhh(ahh):

    def __init__(self):
        self.val4 = "yellow"

    def ListVars(self):
        print(dir(self))

val5 = "purple"
val6 = "orange"

Ahh = ahh()
Bhh = bhh()

print("locals() in test.py:")
dir()
print("locals() in ahh:")
Ahh.ListVars()
print("locals() in bhh:")
Bhh.ListVars()
