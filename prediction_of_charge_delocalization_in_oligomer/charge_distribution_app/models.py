#from django.db import models
import numpy as np
from .utils import *

# Create your models here. These are not database models.


class Hamiltonian:
    """
    Class for the Hamiltonian matrix for a single x value
    
    No modifications are allowed after the Hamiltonian is solved.
    """

    def __init__(self, n=None):
        self.n = n
        self.H = np.zeros((n, n))
        self.H_x = np.zeros(n)
        self.H_system = np.zeros((n, n))
        self.wf = np.zeros((n, n))
        self.energies = np.zeros(n)
        self.x = None
        self.solved = False

    # decorator to prevent modification of the Hamiltonian after it is solved
    def _check_solved(func):
        def wrapper(self, *args, **kwargs):
            if self.solved:
                raise Exception('No modifications are allowed after the Hamiltonian is solved!')
            return func(self, *args, **kwargs)
        return wrapper

    def _not_solved(func):
        def wrapper(self, *args, **kwargs):
            if not self.solved:
                raise Exception('The Hamiltonian is not solved yet!')
            return func(self, *args, **kwargs)
        return wrapper

    def __repr__(self):
        s = f'Hamiltonian(n={self.n}, x={self.x})'
        if self.n < 10:
            s += '\n---'
            for row in (self.H_system + np.diag(self.H_x)):
                s += '\n' + ' '.join(['%.3f' % el if el != 0 else '  .  ' for el in row])
            s += '\n---'

        if self.solved:
            s += '\nSolved!'
            # show x, ground, and excited states
            s += f'\nGround state: {self.get_energy(1):.3f}'
            s += f'\nExcited state: {self.get_energy(2):.3f}'
            # show charges
            s += '\nCharges:'
            # Show each value in %.2f format
            s += ' '.join(['%.3f' % charge for charge in self.get_charges(1)])
        else:
            s += '\nNot solved'
        return s

    @_check_solved
    def set_H_element(self, i, j, v):
        """
        Symmetrically set the Hamiltonian matrix element
        :param i: column index
        :param j: row index
        :param v: value
        :return: Nothing
        """
        self.H_system[i, j] = self.H_system[j, i] = v

    @_check_solved
    def set_couplings(self, couplings):
        """
        Set couplings between the diabatic states
        Values are set that in each subdiagonal, all elements will be the same.
        Truncated couplings are allowed, e.g. for n = 5, couplings = [1, 2, 3] gives the following Hamiltonian:
            . 1 2 3 .
            . . 1 2 3
            . . . 1 2
            . . . . 1
            . . . . .
        Example input matrix:
            . 1 2 3 4
            . . 1 2 3
            . . . 1 2
            . . . . 1
            . . . . .
        :param couplings: list of couplings
        :return: None
        """
        #assert len(couplings) == self.n - 1, 'Number of couplings must be equal to n - 1'
        # loop over each diagonal
        for i in range(self.n - 1):
            for j in range(i + 1, self.n):
                if j - i - 1 < len(couplings):
                    self.set_H_element(i, j, couplings[j - i - 1])

    @_check_solved
    def set_cp_all(self, cp_all):
        """
        Set all coupling elements
        e.g. cp_all = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] gives the following Hamiltonian:
            . 1 2 3 4
            . . 5 6 7
            . . . 8 9
            . . . . 10
            . . . . .
        :param cp_all: list of coupling elements
        :return: None
        """
        assert len(cp_all) == self.n * (self.n - 1) / 2, 'Number of coupling elements must be equal to n * (n - 1) / 2'
        indices = np.triu_indices_from(self.H_system, 1)
        self.H_system[indices] = cp_all
        self.H_system += self.H_system.T

    @_check_solved
    def set_H(self, H):
        """
        Set the Hamiltonian matrix
        e.g. H = np.array([[0, 1, 2, 3, 4],
                  [1, 0, 5, 6, 7],
                  [2, 5, 0, 8, 9],
                  [3, 6, 8, 0, 10],
                  [4, 7, 9, 10, 0]])
        :param H: Hamiltonian matrix
        :return: None
        """
        assert H.shape == (self.n, self.n), 'Hamiltonian matrix must be of size n x n'
        self.H_system = H.copy()

    @_check_solved
    def shift_ends(self, shift=(0, 0)):
        """
        Shift the first and the last elements of the Hamiltonian matrix
        :param shift: tuple with shift values
        :return: None
        """
        self.set_H_element(0, 0, shift[0])
        self.set_H_element(self.n - 1, self.n - 1, shift[1])

    @_check_solved
    def set_x(self, x, reorg_func='quadratic', Lambda=1.0):
        """
        Set diagonal elements of the Hamiltonian matrix
        :param x: coordinate of charge transfer
        :param reorg_func: reorganization function
        :return: None
        """
        self.x = x
        dist_i_x = np.arange(self.n) - x
        if reorg_func == 'quadratic':
            L = np.full(self.n, Lambda)
            h_ii = L * dist_i_x ** 2
        elif reorg_func == 'gaussian':
            # Not tested in the Python version
            a = 1.0 # lambda_G
            R_infl = 1.0
            b = 1 / (2 * R_infl ** 2)
            h_ii = a * (1 - np.exp(-b * dist_i_x ** 2))
        elif reorg_func == 'nelsen':
            # Not tested in the Python version
            C_nelsen = 0.2
            h_ii = Lambda * dist_i_x ** 2 / (1 + C_nelsen) * (1 + C_nelsen * dist_i_x ** 2)
        elif reorg_func == 'quad.1r':
            # Not tested in the Python version
            t = 1
            L = 1 / (3 * t ** 2)
            h_ii = np.where(np.abs(dist_i_x) > t,
                            1 - 2 * L * t ** 3 / np.abs(dist_i_x),
                            L * dist_i_x ** 2)
        self.H_x = h_ii

    @_check_solved
    def solve(self):
        """
        Solve the eigenvalue problem
        :return: eigenvalues and eigenvectors
        """
        self.H = self.H_system + np.diag(self.H_x)
        self.energies, self.wf = np.linalg.eigh(self.H)
        self.solved = True

    @_not_solved
    def get_charges(self, state=1, lean_right=True):
        """
        Get charges of the state
        :param state: state index, starting from 1
        :return: charges
        """
        charges = self.wf[:, state - 1] ** 2
        if lean_right:
            return lean_charges_right(charges)
        
        return charges

    @_not_solved
    def get_energy(self, state=1):
        """
        Get energy of the state
        :param state: state index, starting from 1
        :return: energies
        """
        return self.energies[state - 1]


class Oligomer:
    """
    Represents solution on a range of x values
    """

    def __init__(self, n, dx=0.05, x_beyond=0.5, Lambda = 1.0):
        self.n = n
        self.xrange = np.arange(-x_beyond, n - 1 + x_beyond, dx)
        self.N = len(self.xrange)
        self.Hamiltonians = np.array([None,] * self.N)
        self.solved = False
        self.H_system = np.zeros((self.N, self.N))
        self.Lambda = Lambda

    def _check_solved(func):
        def wrapper(self, *args, **kwargs):
            if self.solved:
                raise Exception('No modifications are allowed after the Hamiltonian is solved!')
            return func(self, *args, **kwargs)
        return wrapper

    def _not_solved(func):
        def wrapper(self, *args, **kwargs):
            if not self.solved:
                raise Exception('The Hamiltonian is not solved yet!')
            return func(self, *args, **kwargs)
        return wrapper

    def json_output(self):
        output = {"Oligomer": f'Oligomer(n_units={self.n}, N_x={self.N})'}
        if self.solved:
            output["status"] = "Solved"
            output["Global Minimum"] = round(self.xrange[self.global_minimum(1)[0]], 3)
            output['Ground State'] = round(self.get_minima(1)[2][0], 3)
            output['Excited State'] = round(self.get_minima(2)[2][0], 3)
            output['Charges'] = ['%.3f' % charge for charge in self[self.global_minimum(1)[0]].get_charges(1)]
        return output


    def __repr__(self):
        s = f'Oligomer(n_units={self.n}, N_x={self.N})'
        if self.solved:
            s += '\nSolved!'
            # show x_range
            s += f'\nx_range: from {self.xrange[0]:.3f} to {self.xrange[-1]:.3f} with step {self.xrange[1] - self.xrange[0]:.3f}'
            
            # show x, ground, and excited states
            global_min_index = self.global_minimum(1)[0]
            
            s += f'\nGlobal minimum: {self.xrange[global_min_index]:.3f}'
            
            s += f'\nGround state: {self.get_minima(1)[2][0]:.3f} eV'
            s += f'\nExcited state: {self.get_minima(2)[2][0]:.3f} eV'
            # show charges
            s += '\nCharges:'
            # Show each value in %.2f format
            s += ' '.join(['%.3f' % charge for charge in self[global_min_index].get_charges(1)])
            
        else:
            s += '\nNot solved'
        return s
    
    @_check_solved
    def set_H_system(self, H_system):
        """
        Set the Hamiltonian matrix
        e.g. H = np.array([[0, 1, 2, 3, 4],
                  [1, 0, 5, 6, 7],
                  [2, 5, 0, 8, 9],
                  [3, 6, 8, 0, 10],
                  [4, 7, 9, 10, 0]])
        :param H: Hamiltonian matrix
        :return: None
        """
        self.H_system = H_system.copy()

    @_check_solved
    def solve(self):
        """
        Solve the eigenvalue problem for each x value
        :return: None
        """
        for i, x in enumerate(self.xrange):
            self.Hamiltonians[i] = Hamiltonian(n=self.n)
            self.Hamiltonians[i].set_x(x, Lambda=self.Lambda)
            self.Hamiltonians[i].set_H(self.H_system)
            self.Hamiltonians[i].solve()
        self.solved = True

    @_not_solved
    # get Hamiltonian by index
    def __getitem__(self, i):
        return self.Hamiltonians[i]

    @_not_solved
    def get_state_curve(self, state=1):
        """
        Get energy of the state as a function of x
        :param state: state index, starting from 1
        :return: energies
        """
        return np.array([H.get_energy(state) for H in self.Hamiltonians])

    @_not_solved
    def get_minima(self, state=1):
        """
        Get global minimum of the state
        :param state: state index, starting from 1
        :return: energies
        """
        # get energies of the ground state
        energies = self.get_state_curve(state)
        global_min = np.argmin(energies)
        local_minima = np.r_[True, energies[1:] < energies[:-1]] & np.r_[energies[:-1] < energies[1:], True]
        # return indices, x values, and energies of the local minima
        return np.where(local_minima)[0], self.xrange[local_minima], energies[local_minima]

    @_not_solved
    def global_minimum(self, state=1):
        """
        Get global minimum of the state
        :param state: state index, starting from 1
        :return: energies
        """
        # get energies of the ground state
        energies = self.get_state_curve(state)
        global_min = np.argmin(energies)
        return global_min, self.xrange[global_min], energies[global_min]

