import csv
import multiprocessing
import sys
import time
from functools import partial

import numpy as np

from .auction import CostFn, Auction
from .utils import create_cost_fn_coef, cartesian


def rand_cost_fn(deg_mean, deg_prob, cap_mean, cap_var):
    degree = np.random.binomial(deg_mean / deg_prob, deg_prob)
    capacity = np.random.normal(cap_mean, cap_var)
    return CostFn(create_cost_fn_coef(degree, capacity), capacity)


def rand_auction(deg_mean, \
                 deg_prob, \
                 cap_mean, \
                 cap_var, \
                 num_bidders, \
                 quota_factor):
    cost_fns = [rand_cost_fn(deg_mean, deg_prob, cap_mean, cap_var) \
                for i in range(int(num_bidders))]
    total_capacity = np.sum(np.array([fn.get_capacity() for fn in cost_fns]))
    return Auction(quota_factor * total_capacity, cost_fns)


def run_simulation_with_params(params, param_names, sims_per_test, auction_params):
    auction_params_ = auction_params.copy()
    id, param_vals = params[0], params[1:]
    param_updates = {param_names[i]: param_vals[i] for i in range(len(param_names))}
    auction_params_.update(param_updates)

    auction_results = [rand_auction(**auction_params_).run().get_results() for i in range(sims_per_test)]
    percent_err = np.array([(id,) +\
                            tuple(param_vals) +\
                            (abs((r['approx_cost'] - r['actual_cost']) / r['actual_cost']),)\
                            for r in auction_results \
                            if r['actual_success'] and r['approx_success']])
    running_time = np.sum(np.array([r['approx_time'] + r['actual_time'] for r in auction_results]))
    print('(id, {param_names}, time) = ({id}, {param_vals}, {time})' \
          .format(param_names=param_names, id=id, param_vals=param_vals, time=round(running_time, 3)))
    return percent_err


def generate_data_with_param_vals(param_names, param_vals, sims_per_test, auction_params):
    sim_ids = np.arange(param_vals.shape[0])
    vals_with_ids = np.column_stack((sim_ids, param_vals))
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start = time.time()
    run_simulation = partial(run_simulation_with_params, \
                             param_names=param_names, \
                             sims_per_test=sims_per_test, \
                             auction_params=auction_params)
    raw_results = pool.map(run_simulation, vals_with_ids)
    end = time.time()
    print('FINISHED in {time} seconds'.format(time=(end - start)))
    return [auction for sim in raw_results for auction in sim]


def generate_data_varied_by_quota(auction_params, min_quota, max_quota, num_tests, sims_per_test):
    quota_factors = np.linspace(min_quota, max_quota, num_tests)
    return generate_data_with_param_vals(('quota_factor',), quota_factors, sims_per_test, auction_params)


def generate_data_varied_by_cap_var(auction_params, min_cap_var, max_cap_var, num_tests, sims_per_test):
    cap_vars = np.linspace(min_cap_var, max_cap_var, num_tests)
    return generate_data_with_param_vals(('cap_var',), cap_vars, sims_per_test, auction_params)


def generate_data_varied_by_num_bidders(auction_params, min_num_bidders, max_num_bidders, num_repeats, sims_per_test):
    auction_sizes = np.arange(min_num_bidders, max_num_bidders + 1).repeat(num_repeats)
    return generate_data_with_param_vals(('num_bidders',), auction_sizes, sims_per_test, auction_params)


def generate_data(auction_params, \
                  min_num_bidders, \
                  max_num_bidders, \
                  min_quota, \
                  max_quota, \
                  min_cap_var, \
                  max_cap_var, \
                  num_quota_tests, \
                  num_cap_var_tests, \
                  sims_per_test):
    params = cartesian([np.linspace(min_quota, max_quota, num_quota_tests), \
                        np.arange(min_num_bidders, max_num_bidders + 1),
                        np.linspace(min_cap_var, max_cap_var, num_cap_var_tests)])

    return generate_data_with_param_vals(('quota_factor', 'num_bidders', 'cap_var'), params, sims_per_test,
                                         auction_params)


def write_data_to_csv(filename, data):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        for entry in data:
            writer.writerow(entry)


output_suffix = sys.argv[1]  # TODO: check if len(sys.argv) > 1

auction_params = {'deg_mean': 3, \
                  'deg_prob': 0.33, \
                  'cap_mean': 10, \
                  'cap_var': 3, \
                  'num_bidders': 10, \
                  'quota_factor': 0.5}

# generate slice data

quota_data = generate_data_varied_by_quota(auction_params, min_quota=0.1, max_quota=0.9, num_tests=50,
                                           sims_per_test=100)
write_data_to_csv('quota_data_{suffix}.csv'.format(suffix=output_suffix), quota_data)

cap_var_data = generate_data_varied_by_cap_var(auction_params, min_cap_var=0.5, max_cap_var=6, num_tests=50,
                                               sims_per_test=100)
write_data_to_csv('cap_var_data_{suffix}.csv'.format(suffix=output_suffix), cap_var_data)

bidder_count_data = generate_data_varied_by_num_bidders(auction_params, \
                                                        min_num_bidders=2, \
                                                        max_num_bidders=20, \
                                                        num_repeats=10, \
                                                        sims_per_test=100)
write_data_to_csv('bidder_count_data_{suffix}.csv'.format(suffix=output_suffix), bidder_count_data)

# generate multidimensional data

generated_data = generate_data(auction_params, \
                               min_num_bidders=2,
                               max_num_bidders=10,
                               min_quota=0.1, \
                               max_quota=0.9, \
                               min_cap_var=0.5, \
                               max_cap_var=5, \
                               num_quota_tests=50, \
                               num_cap_var_tests=20, \
                               sims_per_test=30)
write_data_to_csv('generated_data_{suffix}.csv'.format(suffix=output_suffix), generated_data)
