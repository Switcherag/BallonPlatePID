import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



class Optimization:
    #faire une Adam
    def __init__(self, MySimulation, MyPID):

        self.MySimulation = MySimulation
        
    def random_search(self, num_iterations):
        # Random search
        best_kp = 0
        best_ki = 0
        best_kd = 0
        best_error = float("inf")
        for i in range(num_iterations):
            #add loading bar \r
            print(f"iteration {i+1}/{num_iterations}", end="\r")
            kp = random.uniform(0, 30)
            ki = random.uniform(0, 30)
            kd = random.uniform(0, 30)
            self.MyPID.kp = kp
            self.MyPID.ki = ki
            self.MyPID.kd = kd
            self.MySimulation.MyPID = self.MyPID
            self.MySimulation.euler_integration()
            error = self.MySimulation.quadratic_error()
            if error < best_error:
                best_error = error
                best_kp = kp
                best_ki = ki
                best_kd = kd
                print(f"best parameters: kp = {best_kp:.3f}, ki = {best_ki:.3f}, kd = {best_kd:.3f}")
                print(f"best error: {best_error:.3f}")
       
        return best_kp, best_ki, best_kd
    
    def sgd(self, learning_rate, num_iterations):
        
        
        kp = random.uniform(0, 1)
        ki = 0
        kd = random.uniform(0, 1)
        print(f"initial parameters: kp = {kp:.3f}, ki = {ki:.3f}, kd = {kd:.3f}")
        for i in range(num_iterations):
            #add loading bar \r
            print(f"iteration {i+1}/{num_iterations}", end="\r")
            
            kp_gradient, ki_gradient, kd_gradient = self.cost_gradient( kp, ki, kd)
            kp -= learning_rate * kp_gradient
            ki -= learning_rate * ki_gradient
            kd -= learning_rate * kd_gradient
            #print current parameters  
            print(f"current parameters: kp = {kp:.3f}, ki = {ki:.3f}, kd = {kd:.3f}", end="\r")
            
        print(f"final parameters: kp = {kp:.3f}, ki = {ki:.3f}, kd = {kd:.3f}")
        return kp, ki, kd

    def cost(self,kp, ki, kd):
        # compute the cost of kp, ki, kd on the training data
        self.MyPID.kp = kp
        self.MyPID.ki = ki
        self.MyPID.kd = kd
        self.MySimulation.MyPID = self.MyPID
        self.MySimulation.euler_integration()
        return self.MySimulation.quadratic_error()
    
    def cost_gradient(self, kp, ki, kd):
        # compute the gradient of the cost function at (kp, ki, kd)
        h = 0.001
        grad_kp, grad_ki, grad_kd = \
               (self.cost(kp + h, ki, kd) - self.cost(kp, ki, kd)) / h, \
               (self.cost(kp, ki + h, kd) - self.cost(kp, ki, kd)) / h, \
               (self.cost(kp, ki, kd + h) - self.cost(kp, ki, kd)) / h  
    
        return grad_kp, grad_ki, grad_kd

    def plot2D(self):
        # création de tableaux de valeurs pour Kp et Kd

        a = 0
        b = 3.5

        Kp_values = np.linspace(a, b, num=200)
        Kd_values = np.linspace(a, b, num=200)
        Ki_values = 0

        # initialisation d'un tableau pour stocker les valeurs de la fonction de coût
        cost_values = np.zeros((len(Kp_values), len(Kd_values)))

        # calcul des valeurs correspondantes de la fonction de coût pour chaque paire de valeurs de Kp et Kd
        for i, Kp in enumerate(Kp_values):
            #add loading bar \r
            print(f"iteration {i+1}/{len(Kp_values)}", end="\r")
            for j, Kd in enumerate(Kd_values):
                
                cost_values[i, j] = self.cost(Kp, 0, Kd)**4

        # tracé de la carte de chaleur
        plt.imshow(cost_values, cmap='rainbow', aspect='auto',origin='lower',extent=[a,b,a,b], vmin=np.min(cost_values), vmax=2*np.min(cost_values))
        plt.colorbar()
        plt.xlabel('Kd')
        plt.ylabel('Kp')
        plt.title('Carte de chaleur de la fonction de coût pour Ki = 0')
        plt.show()

    def adam(self, num_iterations=1000, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        """
        Implements the Adam optimization algorithm to minimize a cost function.

        Args:
            cost_function: A function that takes in parameters a, b, and c and returns a scalar cost.
            initial_params: A numpy array of shape (3,) containing the initial parameter values for a, b, and c.
            num_iterations: The number of iterations to run the optimizer for (default 1000).
            learning_rate: The learning rate to use for the optimizer (default 0.001).
            beta1: The decay rate for the first moment estimates (default 0.9).
            beta2: The decay rate for the second moment estimates (default 0.999).
            epsilon: A small value to avoid division by zero (default 1e-8).

        Returns:
            The optimized parameter values for Kp, Ki, and Kd.
        """
        # Initialize the parameters to random values
        kp = random.uniform(0, 1000)
        ki = random.uniform(0, 1000)
        kd = random.uniform(0, 1000)
        initial_params = np.array([kp, ki, kd])
        # Initialize the first and second moment estimates to zero
        m = np.zeros_like(initial_params)
        v = np.zeros_like(initial_params)

        # Initialize the parameter values to the initial values
        params = initial_params

        # Run the optimizer for the specified number of iterations
        for i in range(num_iterations):
            # Compute the cost and gradient of the cost with respect to the parameters
            cost = self.cost(*params)
            gradient = np.array([self.cost(params[0]+epsilon,params[1],params[2])-cost,
                                self.cost(params[0],params[1]+epsilon,params[2])-cost,
                                self.cost(params[0],params[1],params[2]+epsilon)-cost])/epsilon

            # Update the first moment estimate
            m = beta1 * m + (1 - beta1) * gradient

            # Update the second moment estimate
            v = beta2 * v + (1 - beta2) * gradient**2

            # Bias correction for the first moment estimate
            m_hat = m / (1 - beta1**(i+1))

            # Bias correction for the second moment estimate
            v_hat = v / (1 - beta2**(i+1))

            # Update the parameters
            params -= learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
            # Print the optimized parameters \r
           
            print(f"iteration {i+1}/{num_iterations}   optimized parameters: kp = {params[0]:.3f}, ki = {params[1]:.3f}, kd = {params[2]:.3f}  optimized error: {cost:.3f}", end="\r")
            
        self.MySimulation.MyPID.kp = params[0]
        self.MySimulation.MyPID.ki = params[1]
        self.MySimulation.MyPID.kd = params[2]

        self.MySimulation.euler_integration()
        self.MySimulation.plot1D()
        return params
        