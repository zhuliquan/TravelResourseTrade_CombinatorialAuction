import numpy as np
from pyscipopt import Model, quicksum
import itertools as it
import time

NUM_APPROX_VALS = 200
MILLIS_PER_SEC = 1000

def time_method(method, arguments=[]):
    start = time.clock()
    result = method(*arguments)
    end = time.clock()
    return result + (MILLIS_PER_SEC * (end - start),)

class CostFn(object):
    def __init__(self, coefficients, capacity):
        self.fn = np.polynomial.Polynomial(coefficients)
        self.capacity = capacity

    def eval(self, values):
        return np.vectorize(lambda x: self.fn(x) if x > 0 else 0, otypes=[np.float])(values)

    def get_capacity(self):
        return self.capacity

    def get_coef(self):
        return self.fn.coef

class Auction(object):
    def __init__(self, quota, cost_fns, approx_method = 'cap_least_squares'):
        self.quota = quota
        self.approx_method = approx_method

        self.cost_fns = cost_fns
        self.approx_cost_fns = self.approx_cost_fns(self.cost_fns)

        self.completed = False

    def get_num_bidders(self):
        return len(self.cost_fns)

    def get_quota(self):
        return self.quota

    def get_approx_cost_fns(self):
        return self.approx_cost_fns

    def get_results(self):
        return {'actual_success': self.actual_success, \
                'actual_soln': self.actual_soln, \
                'actual_cost': self.actual_cost, \
                'actual_time': self.actual_time, \

                'approx_success': self.approx_success, \
                'approx_soln': self.approx_soln, \
                'approx_cost': self.cost_w_approx_soln, \
                'approx_time': self.approx_time} if self.completed else None

    def run(self):
        if not self.completed:
            self.actual_success, self.actual_soln, self.actual_time = \
                time_method(self.determine_optimal_allocations)
            self.approx_success, self.approx_soln, self.approx_time = \
                time_method(self.determine_approx_allocations)

            objective = self.get_objective_fn(self.cost_fns)
            self.actual_cost = objective(self.actual_soln) if self.actual_success else None
            self.cost_w_approx_soln = objective(self.approx_soln) if self.approx_success else None

            self.completed = True

        return self

    def approx_cost_fns(self, cost_fns):
        return [self.approx_cost_fn(cost_fn) for cost_fn in cost_fns]

    def approx_cost_fn(self, cost_fn):
        if self.approx_method in ['least_squares', 'cap_least_squares']:
            cap = cost_fn.get_capacity()
            raw_x = np.linspace(0, cap, NUM_APPROX_VALS)
            y_at_cap = cost_fn.eval(cap)
            y = cost_fn.eval(raw_x)
            X = np.column_stack((np.ones(raw_x.shape[0]), raw_x))

            if self.approx_method is 'cap_least_squares':
                y -= y_at_cap
                X = (raw_x - cap)[:, None]

            coef = np.linalg.lstsq(X, y)[0]

            if self.approx_method is 'cap_least_squares':
                coef = np.array([y_at_cap - coef[0]*cap, coef[0]])

            return CostFn(coef, cost_fn.get_capacity())

    def determine_optimal_allocations(self):
        return self.determine_allocations_with(self.cost_fns)

    def determine_approx_allocations(self):
        return self.determine_allocations_with(self.approx_cost_fns)

    def determine_allocations_with(self, cost_fns):
        # setup model and variables
        num_bidders = len(cost_fns)
        model = Model('approx_allocations')
        alloc_vars = [model.addVar('x_{i}'.format(i=i), lb=0, ub=cost_fns[i].get_capacity()) \
                        for i in range(num_bidders)]
        entry_vars = [model.addVar('b_{i}'.format(i=i), vtype='B') for i in range(num_bidders)]

        # setup objective fn
        costs = [self.create_poly(alloc_vars[i], cost_fns[i].get_coef()[1:]) \
                    + entry_vars[i]*cost_fns[i].get_coef()[0] \
                        for i in range(num_bidders)]
        model.setObjective(quicksum(costs), sense='minimize')

        # setup constraints
        model.addCons(quicksum(alloc_vars) == self.get_quota(), name='quota') # quota constraint

        for i in range(num_bidders):
            model.addCons(alloc_vars[i] <= 9001*cost_fns[i].get_capacity()*entry_vars[i], name=str(i))

        model.hideOutput()
        model.optimize()
        
        alloc_var_vals = [model.getVal(var) for var in alloc_vars]

        model.free() # to prevent memory leaks

        # TODO: figure out how to detect solver failure
        return True, np.array(alloc_var_vals)

    def create_poly(self, var, coef):
        return quicksum([coef[i]*var**(i + 1) for i in range(len(coef))])

    def get_objective_fn(self, cost_fns):
        def objective(x):
            # TODO: find a cleaner, more numpy-friendly way of computing objective function
            costs = np.array([pair[0].eval(pair[1]) for pair in zip(cost_fns, x.T)])
            return np.sum(costs, 0)

        return objective