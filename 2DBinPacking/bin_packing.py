import copy

class BinPacking:
    def __init__(self,squares,number_of_bins,squares_allocation,bin_size_x,bin_size_y):
        self.squares=copy.deepcopy(squares)
        self.squares_allocation=squares_allocation
        self.used_indexes=list(set(self.squares_allocation))
        self.number_of_bins=len(self.used_indexes)
        self.bin_size_x=bin_size_x
        self.bin_size_y=bin_size_y
        

    def pack_squares_in_bins(self): 
        for index,square in enumerate(self.squares):
            square.bin_index=self.squares_allocation[index]

        for bin_index in self.used_indexes:
            squares_for_bin=list(filter(lambda x: x.bin_index== bin_index, self.squares))
            self.pack_squares_in_single_bin(squares_for_bin,bin_index)

        while(not self.check_if_all_are_packed()):
            squares_for_extra_bin=list(filter(lambda x: x.bin_index== -1, self.squares))
            self.pack_squares_in_single_bin(squares_for_extra_bin,self.find_free_index())
            
            
    def find_free_index(self):
        index=0
        while(index in self.used_indexes):
            index+=1
        self.used_indexes.append(index)
        self.number_of_bins+=1
        return index


    def fitness_check(self):
        bin_area=self.bin_size_x*self.bin_size_y
        used_in_bins=[0]*(max(self.used_indexes)+1)

        for square in self.squares:
            used_in_bins[square.bin_index]+=square.size_x*square.size_y

        used_in_bins.sort(reverse=True)
        used_in_bins=[(x*x)/(bin_area*bin_area) for x in used_in_bins]
        used_in_bins=list(filter(lambda x: x != 0, used_in_bins))
        sum=0
        if self.number_of_bins==1:
            return -self.number_of_bins+used_in_bins[0]
        else:
            for index in range(0,len(used_in_bins)-1):
                sum+=used_in_bins[index]
            return -self.number_of_bins+(sum/(self.number_of_bins-1))
        

    def reduce_bin(self,index):
        for square in self.squares:
            if(square.bin_index>index):
                square.bin_index-=1

    def check_if_all_are_packed(self):
        for square in self.squares:
            if(square.bin_index==-1):
                return False
        return True
    
    def pack_squares_in_single_bin(self,squares, bin_index):
        free_spaces=[self.bin_size_y]*self.bin_size_x
        gap_height=self.bin_size_y
        gap_width=self.bin_size_x
        gap_index=0
        remaining_squares=len(squares)
        while(gap_height>0 and remaining_squares>0):

            index=self.find_index_of_best_fit(squares,gap_width,gap_height)
            
            if(index>-1 and gap_width==squares[index].size_x)or(index>-1 and squares[index].size_x<gap_width):
                self.add_square_to_bin(free_spaces,squares[index],gap_index, bin_index)
                remaining_squares-=1
                squares.pop(index)

            elif(index>-1 and gap_width==squares[index].size_y)or(index>-1 and squares[index].size_y<gap_width):
                squares[index].rotate_square()
                self.add_square_to_bin(free_spaces,squares[index],gap_index, bin_index)
                remaining_squares-=1
                squares.pop(index)

            else:
                self.fill_unusable_gap(free_spaces)

            gap_width=self.find_lowest_gap_width(free_spaces)
            gap_height=self.find_lowest_gap_heigth(free_spaces)
            gap_index=self.find_lowest_gap_index(free_spaces)
        
        for square in squares:
            square.bin_index=-1

            
    def add_square_to_bin(self,free_spaces,square,index, bin_index):
        square.bin_index=bin_index
        square.set_position(index,self.bin_size_y-free_spaces[index])
        for i in range(0,square.size_x):
            free_spaces[i+index]-=square.size_y


    def find_index_of_best_fit(self,squares,gap_width,gap_height):
        best_index=-1
        index=0        
        best_fit_width=0
        number_of_squares=len(squares)
        while(index<number_of_squares):

            width=squares[index].size_x
            height=squares[index].size_y

            if(width==gap_width and height<=gap_height) or (height==gap_width and width<=gap_height):
                return index

            if(width<gap_width and width>best_fit_width and height<=gap_height):
                best_index=index
                best_fit_width=width

            elif(height<gap_width and height>best_fit_width and width<=gap_height):
                best_index=index
                best_fit_width=height
            index+=1

        return best_index



    def find_lowest_gap_heigth(self,free_spaces):
        return max(free_spaces)
    
    def find_lowest_gap_index(self,free_spaces):
        return free_spaces.index(max(free_spaces))
    
    def find_lowest_gap_width(self,free_spaces):
        height=self.find_lowest_gap_heigth(free_spaces)
        index=self.find_lowest_gap_index(free_spaces)
        width=1
        while(index+width<self.bin_size_x and free_spaces[index+width]==height):
            width+=1
        return width

    def fill_unusable_gap(self,free_spaces):
        index=self.find_lowest_gap_index(free_spaces)
        height=free_spaces[index]
        while(index<self.bin_size_x and free_spaces[index]==height):
            free_spaces[index]-=1
            index+=1

    def get_allocations(self):
        allocations=[]
        for square in self.squares:
            allocations.append(square.bin_index)
        return allocations






    
