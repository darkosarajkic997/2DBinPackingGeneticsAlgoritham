from square import Square
from bin_packing import BinPacking
from geneticsAlgoritham import GeneticsAlgoritham
from PIL import Image, ImageDraw

import copy
import math
import random
import pickle
import matplotlib.pyplot as plt 



def draw_bins(squares,number_of_bins,bin_size_x,bin_size_y):
    step=10
    im_dim_x=(bin_size_x+2)*step
    im_dim_y=((bin_size_y+1)*number_of_bins+1)*step
    im = Image.new('RGB', (im_dim_x, im_dim_y), (256, 256, 256))
    draw = ImageDraw.Draw(im)
    index=0
    number_of_drawn_bins=0
    while(number_of_drawn_bins<number_of_bins):
        bin_pos_x=step
        bin_pos_y=step+(number_of_drawn_bins*((bin_size_y+1)*step))
        draw.rectangle((bin_pos_x, bin_pos_y, bin_pos_x+bin_size_x*step, bin_pos_y+bin_size_y*step), fill=(51, 102, 255), outline=(0, 0, 26))
        squares_for_bin=list(filter(lambda x: x.bin_index== index, squares))
        if(len(squares_for_bin)>0):
            draw_squares(squares_for_bin,step,draw,bin_pos_x,bin_pos_y)
            number_of_drawn_bins+=1
        index+=1    
    
    im.save('bins.jpg', quality=95)



def draw_squares(squares_for_bin,step,draw,bin_pos_x,bin_pos_y):
    for square in squares_for_bin:
        lc_x=bin_pos_x+square.position_x*step
        lc_y=bin_pos_y+square.position_y*step
        rc_y=lc_y+square.size_y*step
        rc_x=lc_x+square.size_x*step
        draw.rectangle((lc_x, lc_y, rc_x, rc_y), fill=(153, 255, 102), outline=(0, 26, 9))

def use_genetics(squares,number_of_bins,generation_size,recombination,mutation,size_down,max_generations,stop_criterium,bin_size_x, bin_size_y,draw_bin=False):
    ga=GeneticsAlgoritham(generation_size, recombination, mutation, size_down, max_generations, stop_criterium, squares, number_of_bins, bin_size_x, bin_size_y)
    best_chromosome=ga.find_best_solution()
    bin=BinPacking(squares,max(best_chromosome.gene)+1,best_chromosome.gene,bin_size_x,bin_size_y)
    bin.pack_squares_in_bins()

    if(draw_bin):
        draw_bins(bin.squares,-(math.floor(best_chromosome.fitness)),bin_size_x,bin_size_y,)
    return ga.log




def main():

    squares=[]

    bin_size_x=45
    bin_size_y=15

    total_area_of_squares=0
    ##squares generation
    # for i in range(0,50):
    #     x=random.randrange(5,bin_size_x+1,5)
    #     y=random.randrange(5,bin_size_y+1,5)

    #     k=Square(x,y)
    #     total_area_of_squares+=k.square_area()
    #     squares.append(k)

    # for square in squares:
    #     if(square.size_x<square.size_y):
    #         square.rotate_square()

    # with open('outfile.pkl', 'wb') as fp:
    #     pickle.dump(squares, fp)

    with open ('outfile.pkl', 'rb') as fp:
        squares = pickle.load(fp)

    squares.sort(reverse=True)
    total_area_of_squares=0
    total_area_of_squares=sum(map(lambda x: x.size_x*x.size_y,squares))

    starting_number_of_bins=(total_area_of_squares//(bin_size_x*bin_size_y))*2

    generation_size=150
    recombination=0.8
    mutation=0.5
    size_down=0.4
    max_generations=350
    stop_criterium=1

    use_genetics(squares,starting_number_of_bins,generation_size,recombination,mutation,size_down,max_generations,stop_criterium,bin_size_x, bin_size_y,draw_bin=True)
    


    # #max_generations
    # max_generations=[50,150,250]

    # for variable_generations in max_generations:
    #     log=use_genetics(squares,starting_number_of_bins,generation_size,recombination,mutation,size_down,variable_generations,stop_criterium,bin_size_x, bin_size_y)
    #     y_axis=list(map(lambda x:(math.sqrt(x-math.floor(x))*100),log ))
    #     plt.plot(y_axis,label = f'max_generation:{variable_generations}') 
    
    # plt.xlabel('number of generations')
    # plt.ylabel('pct of used surface') 
    # plt.savefig('number_of_generations')
    # plt.legend()
    # plt.show() 


    # #gen_sizes
    # gen_sizes=[50,100,150]

    # for variable_gen_size in gen_sizes:
    #     log=use_genetics(squares,starting_number_of_bins,variable_gen_size,recombination,mutation,size_down,max_generations,stop_criterium,bin_size_x, bin_size_y)
    #     y_axis=list(map(lambda x:(math.sqrt(x-math.floor(x))*100),log ))
    #     plt.plot(y_axis,label = f'gen_size:{variable_gen_size}') 
    
    # plt.xlabel('number of generations')
    # plt.ylabel('pct of used surface') 
    # plt.savefig('gen_sizes')
    # plt.legend()
    # plt.show() 

    # #recombination
    # recombinations=[0.2,0.4,0.6,0.8]

    # for variable_recombination in recombinations:
    #     log=use_genetics(squares,starting_number_of_bins,generation_size, variable_recombination,mutation,size_down,max_generations,stop_criterium,bin_size_x, bin_size_y)
    #     y_axis=list(map(lambda x:(math.sqrt(x-math.floor(x))*100),log ))
    #     plt.plot(y_axis,label = f'recombination:{variable_recombination}') 
    
    # plt.xlabel('number of generations')
    # plt.ylabel('pct of used surface') 
    # plt.savefig('variable_recombination')
    # plt.legend()
    # plt.show() 

    # #mutation
    # mutations=[0.2,0.4,0.6,0.8]

    # for variable_mutation in mutations:
    #     log=use_genetics(squares,starting_number_of_bins,generation_size,recombination,variable_mutation,size_down,max_generations,stop_criterium,bin_size_x, bin_size_y)
    #     y_axis=list(map(lambda x:(math.sqrt(x-math.floor(x))*100),log ))
    #     plt.plot(y_axis,label = f'mutations:{variable_mutation}') 
    
    # plt.xlabel('number of generations')
    # plt.ylabel('pct of used surface') 
    # plt.savefig('variable_mutation')
    # plt.legend()
    # plt.show() 
     
     
    # #size_down
    # size_downs=[0.1,0.2,0.3,0.5]

    # for variable_size_down in size_downs:
    #     log=use_genetics(squares,starting_number_of_bins,generation_size,recombination,mutation,variable_size_down,max_generations,stop_criterium,bin_size_x, bin_size_y)
    #     y_axis=list(map(lambda x:(math.sqrt(x-math.floor(x))*100),log ))
    #     plt.plot(y_axis,label = f'size_down:{variable_size_down}') 
    
    # plt.xlabel('number of generations')
    # plt.ylabel('pct of used surface') 
    # #plt.savefig('variable_size_down')
    # plt.legend()
    # plt.show() 
    
    
    # #stop_criterium
    # stop_criteriums=[0.85,0.90,0.95,0.99,1]

    # for variable_stop_criterium in stop_criteriums:
    #     log=use_genetics(squares,starting_number_of_bins,generation_size,recombination,mutation,size_down,max_generations,variable_stop_criterium,bin_size_x, bin_size_y)
    #     y_axis=list(map(lambda x:(math.sqrt(x-math.floor(x))*100),log ))
    #     plt.plot(y_axis,label = f'stop_criterium:{variable_stop_criterium}') 
    
    # plt.xlabel('number of generations')
    # plt.ylabel('pct of used surface') 
    # plt.savefig('variable_stop_criterium')
    # plt.legend()
    # plt.show() 




if __name__ == "__main__":
    main()