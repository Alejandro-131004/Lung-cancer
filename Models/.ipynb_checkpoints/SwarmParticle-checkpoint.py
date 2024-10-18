class SwarmParticle:
    """
    This is a 'particle' object with member properties.
    Initial parameters: 'velocity' and 'position'.
    """
    
    def __init__(self, velocity, position):
        """
        Constructor to initialize the particle's velocity, position, and best position.
        :param velocity: list, velocity of the particle in 2 dimensions (GAMMA(0), NU(1))
        :param position: list, position of the particle in 2 dimensions (GAMMA(0), NU(1))
        """
        self.velocity = velocity            # Initialize velocity
        self.position = position            # Initialize position
        self.best_position = position[:]    # Make a copy of the current position (not a reference)
        self.fitness = [0.0, 0.0]           # Initialize fitness with default values (2D)
        self.best_fitness = [0.0, 0.0]      # Initialize best fitness with default values (2D)
        self.percentage_fitness = 0.0       # Initialize percentage_fitness
        self.percentage_best_fitness = 0.0  # Initialize percentage_best_fitness

    # Getter and setter methods for velocity
    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    # Getter and setter methods for position
    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    # Getter and setter methods for best position
    def get_best_position(self):
        return self.best_position

    def set_best_position(self, best_position):
        self.best_position = best_position

    # Getter and setter methods for fitness
    def get_fitness(self):
        return self.fitness

    def set_fitness(self, fitness):
        self.fitness = fitness
        self.set_fitness_percentage(self.get_percentage(fitness))

    # Getter and setter methods for best fitness
    def get_best_fitness(self):
        return self.best_fitness

    def set_best_fitness(self, best_fitness):
        self.best_fitness = best_fitness
        self.set_best_fitness_percentage(self.get_percentage(best_fitness))

    # Getter and setter methods for percentage fitness
    def get_percentage_fitness(self):
        return self.percentage_fitness

    def set_fitness_percentage(self, percentage_fitness):
        self.percentage_fitness = percentage_fitness

    # Getter and setter methods for percentage best fitness
    def get_percentage_best_fitness(self):
        return self.percentage_best_fitness

    def set_best_fitness_percentage(self, percentage_best_fitness):
        self.percentage_best_fitness = percentage_best_fitness

    # Method to calculate fitness percentage based on the fitness values
    def get_percentage(self, fitness):
        a = fitness[0]
        b = fitness[1]
        percentage = ((a + b) / 2) * 100
        return percentage
