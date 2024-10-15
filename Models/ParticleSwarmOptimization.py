import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import pandas as pd
import SwarmParticle

class ParticleSwarmOptimization:
    W = 0.729
    P = 1.49445
    G = 1.49445
    maxV = 2 ** 0.25
    minV = 2 ** -0.25
    maxX = -1.0381852225093116E9 + 2e-2
    minX = -1.0381852225093116E9 + 2e-2
    dim = 2  # Dimension of position and velocity vectors

    def __init__(self, size, no_of_iteration):
        self.swarm = [None] * size
        self.g_Best = None
        self.data = self.load_data()  # Load data from file or generate random data
        self.param = SVC()  # Replacing libsvm with scikit-learn's SVM
        self.initialize_swarm()
        self.start_iteration(no_of_iteration)

    def load_data(self):
        # Load dataset using pandas or any similar library (you can change the file path)
        try:
            dataset = pd.read_csv('CSCtest.data', header=None)
            X = dataset.iloc[:, :-1].values
            y = dataset.iloc[:, -1].values
            return (X, y)
        except FileNotFoundError:
            print("Data file not found. Please check the file path.")
            return None

    def initialize_swarm(self):
        for i in range(len(self.swarm)):
            X_position = [self.minX + (np.random.rand() * (self.maxX - self.minX)) for _ in range(self.dim)]
            V_velocity = [self.minV + (np.random.rand() * (self.maxV - self.minV)) for _ in range(self.dim)]

            # Initialize particle's velocity and position
            self.swarm[i] = SwarmParticle(V_velocity, X_position)

            # Evaluate fitness
            self.set_and_evaluate_fitness(self.swarm[i])

            # Initialize best fitness with current fitness value
            self.swarm[i].set_best_fitness(self.swarm[i].fitness)

            # Initialize g-best to the first particle, update when a better one is met
            if i == 0:
                self.g_Best = SwarmParticle(self.swarm[0].velocity, self.swarm[0].position)
                self.g_Best.set_fitness(self.swarm[0].fitness)
                self.g_Best.set_best_fitness(self.g_Best.fitness)
            else:
                if self.swarm[i].percentage_best_fitness > self.g_Best.percentage_best_fitness:
                    self.g_Best = SwarmParticle(self.swarm[i].velocity, self.swarm[i].position)
                    self.g_Best.set_fitness(self.swarm[i].fitness)
                    self.g_Best.set_best_fitness(self.g_Best.fitness)

        print("\n>>>> All particles initialized <<<<<<")
        print(f"G-best ===> {self.g_Best.percentage_best_fitness}%")

    def set_and_evaluate_fitness(self, particle):
        c = particle.position[0]
        gamma = particle.position[1]

        # Train SVM with 'C' and 'GAMMA' values
        fitness = self.train_svm(c, gamma)

        # Set its fitness
        particle.set_fitness(fitness)

    def train_svm(self, c, gamma):
        # Set SVM parameters using scikit-learn's SVM
        self.param.C = c
        self.param.gamma = gamma
        X, y = self.data

        # Perform cross-validation
        scores = cross_val_score(self.param, X, y, cv=3)
        accuracy_a = scores.mean()

        val = [accuracy_a, accuracy_a]  # Placeholder for accuracy for two classes
        print(f"C ==> {c:.5f}  Gamma ==> {gamma:.5f} \t| Accuracy: {accuracy_a:.5f}")
        return val

    def start_iteration(self, no_of_iteration):
        for _ in range(no_of_iteration):
            for j in range(len(self.swarm)):
                r_p = np.random.rand()
                r_g = np.random.rand()

                # Update velocity
                for k in range(self.dim):
                    v = self.swarm[j].velocity[k]
                    x = self.swarm[j].position[k]
                    bp = self.swarm[j].best_position[k]
                    gbp = self.g_Best.best_position[k]

                    v = (self.W * v) + ((self.P * r_p) * (bp - x)) + ((self.G * r_g) * (gbp - x))
                    self.swarm[j].velocity[k] = np.clip(v, self.minV, self.maxV)

                # Update position
                for k in range(self.dim):
                    v = self.swarm[j].velocity[k]
                    x = self.swarm[j].position[k]

                    self.swarm[j].position[k] = np.clip(x + v, self.minX, self.maxX)

                # Set and evaluate fitness
                self.set_and_evaluate_fitness(self.swarm[j])

                # Check if best position is updated
                if self.swarm[j].percentage_fitness > self.swarm[j].percentage_best_fitness:
                    self.swarm[j].set_best_fitness(self.swarm[j].fitness)
                    if self.swarm[j].percentage_best_fitness > self.g_Best.percentage_best_fitness:
                        self.g_Best = SwarmParticle(self.swarm[j].velocity, self.swarm[j].position)
                        self.g_Best.set_fitness(self.swarm[j].fitness)
                        self.g_Best.set_best_fitness(self.g_Best.fitness)

            print(f"G-best ===> {self.g_Best.percentage_best_fitness}% "
                  f"{{C={self.g_Best.position[0]}, Gamma={self.g_Best.position[1]}}}")


if __name__ == "__main__":
    ParticleSwarmOptimization(30, 200)