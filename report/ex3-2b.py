from src.minority_game import  MinorityGameWithStrategyTable
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    # set agent num
    agent_num = 201
    # set round number from 10000 to 100000
    round_num = 20
    depth_grid = range(3,11)
    strategy_num = [3,4,8,16,32,64]
    stdd_list = []
    # Run the game for different round number
    for depth in depth_grid:
        for sn in strategy_num
        game = MinorityGameWithStrategyTable(agent_num, round_num,depth,sn)
        game.run_game()
        mean,stdd = game.score_mean_std
        mean_list.append(mean)
        stdd_list.append(stdd)

    # print result
    print(mean_list)
    print(stdd_list)
    # plot mean
    fig = plt.figure(figsize=(10, 4))
    plt.plot(depth_grid,mean_list)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    fig.suptitle('Mean Value')
    plt.xlabel('Depth')
    plt.ylabel('Average numbers of winners')
    fig.savefig('ex3-2-depth-mean.jpg')

    # plot SD
    fig2 = plt.figure(figsize=(10, 4))
    plt.plot(depth_grid,stdd_list)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    fig2.suptitle('Standard Deviation')
    plt.xlabel('Depth')
    plt.ylabel('Average numbers of winners')
    fig2.savefig('ex3-2-depth-std.jpg')