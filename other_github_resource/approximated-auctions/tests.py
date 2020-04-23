import numpy as np
import matplotlib.pyplot as plt
from auction import CostFn, Auction
from utils import create_cost_fn_coef

# single bidder
cost_fns = [CostFn(create_cost_fn_coef(2, 3), 3)]
auction = Auction(2, cost_fns).run()
assert (auction.actual_soln==np.array([2])).all()
assert (auction.approx_soln==np.array([2])).all()
assert auction.actual_cost==17

# two of same bidder
cost_fns = [CostFn(create_cost_fn_coef(2, 3), 3), CostFn(create_cost_fn_coef(2, 3), 3)]
auction = Auction(4, cost_fns).run()
assert (auction.actual_soln==np.array([3, 1])).all() or (auction.actual_soln==np.array([1, 3])).all()
assert (auction.approx_soln==np.array([3, 1])).all() or (auction.approx_soln==np.array([1, 3])).all()
assert auction.actual_cost==32

# one bidder with cheaper cost structure
cost_fns = [CostFn(create_cost_fn_coef(4, 4), 4), CostFn(create_cost_fn_coef(2, 3), 3)]
assert (auction.actual_soln==np.array([1, 3])).all()
assert (auction.approx_soln==np.array([1, 3])).all()
assert auction.actual_cost==449

# one bidder with cheaper cost structure and two with equally more expensive structures
cost_fns = [CostFn(create_cost_fn_coef(4, 4), 4), CostFn(create_cost_fn_coef(4, 4), 4), CostFn(create_cost_fn_coef(2, 3), 3)]
auction = Auction(4, cost_fns).run()
assert (auction.actual_soln==np.array([1, 0, 3])).all() or (auction.actual_soln==np.array([0, 1, 3])).all()
assert (auction.approx_soln==np.array([1, 0, 3])).all() or (auction.approx_soln==np.array([0, 1, 3])).all()
assert auction.actual_cost==449