# Also need one for graphs
class ComplexMap():
    def __init__(self,lines,element_type,use_diag=False):
        self.dim_X,self.dim_Y = len(lines),len(lines[0])
        self.use_diag = use_diag
     
        self.__map_set= set([(i+1j*j,element_type(lines[i][j])) for i in range(self.dim_X) for j in range(self.dim_Y)])
        self.__map_dict = {coord:val for coord,val in self.__map_set}
        self.__all_coords = set(coord for coord,_ in self.__map_set)
        self.__element_type = element_type
        
    def copy(self):
        lines=self.print_me(do_print=False)
        my_copy = ComplexMap(lines,self.__element_type,self.use_diag)
        return my_copy

    def get_value(self,coord,filler=None):
        return self.__map_dict.get(coord,filler)
    
    def map_as_set(self):
        return self.__map_set

    def map_as_dict(self):
        return self.__map_dict

    def map_all_coords(self):
        return self.__all_coords

    # could be class method?
    @staticmethod
    def directions_updown():
        return set([1,-1,1j,-1j])
    
    @staticmethod
    def directions_diag():
        return set([-1-1j,-1+1j,1-1j,1+1j])
    
    @staticmethod
    def directions_updowndiag(cls):
        return cls.directions_diag.union(cls.directions_updown)

    @staticmethod
    def is_smaller(c1,c2):
        return c1.real < c2.real and c1.imag < c2.imag

    @staticmethod
    def is_smaller_partial(c1,c2,check_real):
        if check_real:
            return c1.real < c2.real 
        else:
            return c1.imag < c2.imag

    @staticmethod
    def order_numbers(c_nums,direction):
        """ 1: ascending, -1: descending
            1j: ascending, -1j: edscending 
        """

        if direction.imag == 0:
            order = sorted(c_nums,key=lambda x:direction.real*x.real)
        else:
            order = sorted(c_nums,key=lambda x: direction.imag*x.imag)
        
        return order
    
    
    def are_neighbours(self,c1,c2):
        return (c1-c2) in self.get_neighbour_directions()

    def is_valid(self,c1):
        return c1 in self.__all_coords

    def get_neighbour_directions(self):
        if self.use_diag: 
            return self.directions_updowndiag()
        else:
            return self.directions_updown()
    
    def get_neighbours(self,c1):
        directions = self.get_neighbour_directions()
        return set([c1+d for d in directions]).intersection(self.__all_coords)

    def get_neighbours_withvals(self,c1):
        directions = self.get_neighbour_directions()
        res = set((x,val) for x,val in self.__map_set if (x-c1) in directions) 
        return res

    def change_value_many(self,coord_val_pairs):
        for coord,val in coord_val_pairs:
            self.change_value(coord,val,update_map=False)
        self.__map_set = set(self.__map_dict.items())
    
    def change_value(self,coord,val,update_map=True):
        self.__map_dict[coord]=val
        self.__map_set = set(self.__map_dict.items())

    def print_me(self, do_print=True):
        line = ["."]*self.dim_Y
        area = [line.copy() for _ in range(self.dim_X)]
        for coord,val in self.__map_dict.items():
            line = area[int(coord.real)] 
            line[int(coord.imag)]=val
            area[int(coord.real)]=line
        area_pr =["".join(l) for l in area]

        if do_print:
            print("\n".join(area_pr))
        return area_pr
        
# assert ComplexMap.are_neighbours_nodiag(2j,2j+1) == True
# assert ComplexMap.are_neighbours_nodiag(2j,2j+2) == False
# assert ComplexMap.are_neighbours_nodiag(2j,3j) == True
# assert ComplexMap.are_neighbours_nodiag(2j,3j+1) == False

# assert ComplexMap.are_neighbours_withdiag(2j,2j+1) == True
# assert ComplexMap.are_neighbours_withdiag(2j,2j+2) == False
# assert ComplexMap.are_neighbours_withdiag(2j,3j) == True
# assert ComplexMap.are_neighbours_withdiag(2j,3j+1) == True