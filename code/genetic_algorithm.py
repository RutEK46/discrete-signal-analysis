from numba import cuda, jit
from random import random, seed
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float64
from time import time
import math
import numpy as np


@cuda.jit(device=True)
def device_sigmoid(x):
    return 1 / (1 + math.exp(-x))


@jit(nopython=False, forceobj=True)
def genetic_algorithm(dataset, act_funcs, population_size, mutation_chance):
    seed()
    threads = 256, 256
    blocks = int(population_size / threads[0] + 1), int(len(dataset) / threads[1] + 1)

    population = np.array([[0.0 for _ in range(len(act_funcs))] for _ in range(population_size)], 'float64')
    cuda_population = cuda.to_device(population)

    rng_states = create_xoroshiro128p_states(threads[0] * blocks[0], seed=time())
    cuda_generate_new_population[threads[0], blocks[0]](cuda_population, rng_states)
    cuda.synchronize()

    cuda_dataset = cuda.to_device(dataset)
    cuda_dataset_activations = cuda.to_device(np.array([[act_funcs[j](dataset[i])
                                                        for j in range(len(act_funcs))] for i in range(len(dataset))], 'float64'))
    cuda_fitness = cuda.to_device(np.array([[0.0 for _ in range(len(dataset))] for _ in range(population_size)], 'float64'))

    fitness_avg = np.array([0.0 for i in range(population_size)], 'float64')
    cuda_fitness_avg = cuda.to_device(fitness_avg)

    while True:
        cuda_eval_fitness[threads, blocks](cuda_population, cuda_dataset, cuda_dataset_activations, cuda_fitness)
        cuda.synchronize()
        cuda_avg_fitness[threads[0], blocks[0]](cuda_fitness, cuda_fitness_avg)
        cuda.synchronize()
        cuda_fitness_avg.copy_to_host(fitness_avg)
        cuda_population.copy_to_host(population)

        population_ = sorted([[population[i], fitness_avg[i]] for i in range(population_size)], key=__get_2nd_el, reverse=True)

        yield population_[0][0], population_[0][1]

        survived_size = int(len(population)/2)
        for i in range(survived_size):
            population[i] = population_[i][0]

        for i in range(survived_size, len(population) - survived_size):
            s1 = population_[int(random() * survived_size)][0]
            s2 = population_[int(random() * survived_size)][0]

            new_chromosome = [w1 if random() < 0.5 else w2 for w1, w2 in zip(s1, s2)]
            population[i] = new_chromosome

        cuda_population = cuda.to_device(population)
        cuda_mutate_population[threads[0], blocks[0]](cuda_population, mutation_chance, rng_states)
        cuda.synchronize()


@cuda.jit('void(float64[:,:], float64[:,:], float64[:,:,:], float64[:,:])')
def cuda_eval_fitness(population, dataset, dataset_activations, fitness):
    tx = cuda.threadIdx.x
    bx = cuda.blockIdx.x
    dx = cuda.blockDim.x
    ty = cuda.threadIdx.y
    by = cuda.blockIdx.y
    dy = cuda.blockDim.y

    i = tx + bx * dx
    j = ty + by * dy
    if i < len(population) and j < len(dataset):

        current_money = 2000
        actions = 0
        for k in range(len(dataset[j])):
            act = 0.0
            for l in range(len(dataset_activations[j])):
                act += population[i, l] * dataset_activations[j, l, k]

            act = device_sigmoid(act)
            if act >= 0.5:
                new_actions = int(current_money / dataset[j, k])
                actions += new_actions
                current_money -= new_actions * dataset[j, k]
            else:
                current_money += actions * dataset[j, k]
                actions = 0

        current_money += actions * dataset[j, -1]
        fitness[i, j] = current_money


@cuda.jit('void(float64[:,:], float64[:])')
def cuda_avg_fitness(fitness, fitness_avg):
    tx = cuda.threadIdx.x
    bx = cuda.blockIdx.x
    dx = cuda.blockDim.x

    i = tx + bx * dx
    if i < len(fitness):
        sum_ = 0
        for j in range(len(fitness[i])):
            sum_ += fitness[i, j]

        fitness_avg[i] = sum_ / len(fitness[i])


@cuda.jit
def cuda_generate_new_population(population, rng_states):
    tx = cuda.threadIdx.x
    bx = cuda.blockIdx.x
    dx = cuda.blockDim.x

    i = tx + bx * dx
    if i < len(population):
        for j in range(len(population[i])):
            population[i][j] = math.atanh(2.0 * (xoroshiro128p_uniform_float64(rng_states, i) - 0.5))


@cuda.jit
def cuda_mutate_population(population, mutation_chance, rng_states):
    tx = cuda.threadIdx.x
    bx = cuda.blockIdx.x
    dx = cuda.blockDim.x

    i = tx + bx * dx
    if i < len(population):
        for j in range(len(population[i])):
            if xoroshiro128p_uniform_float64(rng_states, i) < mutation_chance:
                population[i][j] = math.atanh(2.0 * (xoroshiro128p_uniform_float64(rng_states, i) - 0.5))


def __get_2nd_el(el1):
    return el1[1]
