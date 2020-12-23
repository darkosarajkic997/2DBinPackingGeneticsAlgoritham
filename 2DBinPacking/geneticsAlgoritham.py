from chromosome import Chromosome
from bin_packing import BinPacking
import functools 
import random
import bisect
import math

class GeneticsAlgoritham:

    def __init__ (self,generation_size,recombination,mutation,size_down,max_generations,stop_criterium,squares,number_of_bins,bin_size_x, bin_size_y):
        self.squares=squares
        self.chromosomes=[]
        self.generation_size=generation_size
        self.number_of_squares=len(squares)
        self.number_of_bins=number_of_bins
        for index in range(0,generation_size):
            self.chromosomes.append(Chromosome(self.number_of_squares,number_of_bins))
        self.recombination=recombination
        self.mutation=mutation
        self.size_down=size_down
        self.max_generations=max_generations
        self.stop_criterium=stop_criterium**2
        self.best_chromosome=None
        self.best_fitness=1
        self.bin_size_x=bin_size_x
        self.bin_size_y=bin_size_y
        self.log=[]


    def find_best_solution(self):
        number_of_generation=0
        self.find_best_fitness_for_generation()
        self.log.append(self.best_fitness)
        while(self.max_generations>number_of_generation and self.stop_criterium>self.find_usage()):
            
            self.chromosomes.sort(reverse=True)
            if(number_of_generation%20==0):
                print(f'Generation {number_of_generation}: Best fitness: {self.best_fitness}')
            #if(number_of_generation%5==0):
            
            number_of_generation+=1

            elite_number=int(self.generation_size-self.generation_size*self.recombination)
            new_generation=self.chromosomes[:elite_number]

            roulette_wheel=self.generate_roulette_wheel()
            new_generation_size=len(new_generation)

            while(new_generation_size<self.generation_size):
                parents=self.generate_parents(roulette_wheel)
                child1,child2=self.generate_children( parents[0],parents[1],self.mutation,self.size_down) 
                new_generation.append(child1)
                new_generation.append(child2)
                new_generation_size+=2
            
            if(new_generation_size<self.generation_size):
                new_generation_size.pop()

            self.chromosomes=new_generation
            self.find_best_fitness_for_generation()
            self.log.append(self.best_fitness)
        
        return self.best_chromosome

    def find_usage(self):
        value=math.modf(self.best_fitness)
        return (1+value[0])


    def find_best_fitness_for_generation(self):
        generation_best_fitness=1
        best_chromosome_in_generation=None
        for chromosome in self.chromosomes:
            max_bin=max(chromosome.gene)+1
            pack=BinPacking(self.squares,max_bin,chromosome.gene,self.bin_size_x,self.bin_size_y)
            pack.pack_squares_in_bins()
            chromosome.fitness=pack.fitness_check()   
            if(generation_best_fitness==1 or generation_best_fitness<chromosome.fitness):
                generation_best_fitness= chromosome.fitness
                best_chromosome_in_generation=chromosome

        if(generation_best_fitness>self.best_fitness or self.best_fitness==1):
            self.best_fitness=generation_best_fitness
            self.best_chromosome=best_chromosome_in_generation
        return generation_best_fitness

    def generate_roulette_wheel(self):
        roulette_wheel=[]
        edge=0
        min_value=math.floor(self.chromosomes[-1].fitness)
        sum_of_fitness=sum(chromosome.fitness for chromosome in self.chromosomes)-(min_value*len(self.chromosomes))
        for index,chromosome in enumerate(self.chromosomes):
            edge+=((chromosome.fitness-min_value)/sum_of_fitness)
            roulette_wheel.append(edge)
        return roulette_wheel
        
    def generate_parents(self,roulette_wheel):
        selector=random.uniform(0, 1)
        a=self.chromosomes[bisect.bisect_left(roulette_wheel, selector)]
        selector=random.uniform(0, 1)
        b=self.chromosomes[bisect.bisect_left(roulette_wheel, selector)]
        return a,b

    def generate_children(self,parent1,parent2, mutation, size_down):
        child1=Chromosome(self.number_of_squares,self.number_of_bins)
        child2=Chromosome(self.number_of_squares,self.number_of_bins)
        break_point=random.randint(0,self.number_of_squares-1)
        child1.set_gene(parent1.gene[:break_point]+parent2.gene[break_point:])
        child2.set_gene(parent2.gene[:break_point]+parent1.gene[break_point:])
        
        rand_mutation=random.uniform(0, 1)
        if(rand_mutation<mutation):
            rand_position=random.randint(0,self.number_of_squares-1)
            last_bin=max(child1.gene)
            child1.gene[rand_position]=random.randint(0,last_bin)
            rand_position=random.randint(0,self.number_of_squares-1)
            last_bin=max(child2.gene)
            child2.gene[rand_position]=random.randint(0,last_bin)
        
        rand_size_down=random.uniform(0, 1)
        if(rand_size_down<size_down):
            if(self.best_fitness>0):
                print('a')
            max_bin=math.floor(-self.best_fitness)+1
            child1=Chromosome(self.number_of_squares,max_bin)

        return child1,child2
        


            

