class Square:

    def __init__(self, x, y):
        self.size_x = x
        self.size_y = y
        self.position_x=-1
        self.position_y=-1
        self.bin_index=-1
    
    def square_area(self):
        return self.size_x*self.size_y

    def rotate_square(self):
        tmp=self.size_x 
        self.size_x=self.size_y
        self.size_y=tmp

    def __le__ (self,other):
        if (self.size_x<other.size_x):
            return True
        if (self.size_x==other.size_x):
            return self.size_y<other.size_y
        return False

    def __gt__ (self,other):
        if (self.size_x>other.size_x):
            return True
        if (self.size_x==other.size_x):
            return self.size_y>other.size_y
        return False

    def __eq__(self,other):
        return (self.size_x==other.size_x and self.size_y==other.size_y)

    def __str__(self):
        return f'({self.size_x},{self.size_y})'
       
    def set_position(self,x,y):
        self.position_x=x
        self.position_y=y

    