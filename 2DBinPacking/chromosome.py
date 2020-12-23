import random

class Chromosome:
    
    def __init__(self,size,number_of_bins):
        self.gene=list(random.randrange(0,number_of_bins) for i in range(size))
        self.fitness=1

    def set_gene(self,gene):
        self.gene=gene

    def size_down_gene(self):
        last_bin=max(self.gene)
        new_gene=[]
        if(last_bin>0):
            new_gene=list(map(lambda x: x if x<last_bin else random.randint(0,last_bin-1),self.gene))
        self.gene=new_gene

    def __lt__(self,other):
        if(self.fitness<other.fitness):
            return True
        return False
    
    def __eq__(self,other):
        return self.fitness==other.fitness

   