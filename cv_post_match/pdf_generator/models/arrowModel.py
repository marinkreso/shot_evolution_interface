class ArrowModel:
    def __init__(self):
        self.name = ""
        self.alpha = ""
        self.red = ""
        self.green = ""
        self.blue = ""
        self.x1 = ""
        self.y1 = ""
        self.x2 = ""
        self.y2 = ""
        self.width = ""
        self.path = ""

    def set_color(self, alpha, red, green, blue):
        self.alpha = alpha
        self.red = red
        self.green = green
        self.blue = blue

    def set_data(self, x1, y1, x2, y2, width, name):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.name = name

    def get_name(self):
        return self.name

    def get_width(self):
        return self.width

    def get_color(self):
        return self.alpha + " " + self.red + " " + self.green + " " + self.blue + " "

    def get_data(self):
        return (
            self.x1
            + " "
            + self.y1
            + " "
            + self.x2
            + " "
            + self.y2
            + " "
            + self.width
            + " "
            + self.name
            + " "
        )
