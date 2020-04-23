import csv
import numpy as np
import pandas as pd
#import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

SCATTER_PARAMS = {'alpha': 0.1}
PRINCIPAL_REG_FORMULA = 'err ~ quota_factor + I(quota_factor**2) + cap_var + I(cap_var**2) + num_bidders'

data = pd.read_csv('generated_data_full.csv',header=None, names=('sim_id', 'quota_factor', 'num_bidders', 'cap_var', 'err'))
data['num_bidders'] = data['num_bidders'].astype(int)
grouped_data = data.groupby(('quota_factor', 'num_bidders', 'cap_var'), as_index=False)

mean_err = grouped_data.agg({'err': 'mean'})
mean_err = mean_err[mean_err['err'] <= 1] # removes a single outlier
print mean_err.describe()

mean_err_reg_line = smf.ols(formula=PRINCIPAL_REG_FORMULA, data=mean_err).fit()
print mean_err_reg_line.summary()

standardized_vars = (mean_err - mean_err.mean()) / mean_err.std()
print standardized_vars.describe()
standardized_reg_line = smf.ols(formula=PRINCIPAL_REG_FORMULA, data=standardized_vars).fit()
print standardized_reg_line.summary()

mean_err['residuals'] = mean_err_reg_line.resid

fig = plt.figure()

# partial residual plot for num_bidders
MIN_NUM_BIDDERS_REG_LINE = 1.5
MAX_NUM_BIDDERS_REG_LINE = 10.5

partial_reg_num_bidders_data = pd.DataFrame({'num_bidders': mean_err['num_bidders'], \
                                'part_reg': mean_err['residuals'] + mean_err_reg_line.params['num_bidders'] * mean_err['num_bidders']})

num_bidders_plt = fig.add_subplot(221)
num_bidders_plt.set_title('Partial Residual Plot for # of Bidders')
num_bidders_plt.set_xlim([MIN_NUM_BIDDERS_REG_LINE, MAX_NUM_BIDDERS_REG_LINE])
sns.regplot(x='num_bidders', y='part_reg', order=1, data=partial_reg_num_bidders_data, ax=num_bidders_plt, scatter_kws=SCATTER_PARAMS)
num_bidders_plt.set_xlabel('# of bidders')
num_bidders_plt.set_ylabel('partial residual for # of bidders')

num_bidders_reg_line = smf.ols(formula='part_reg ~ num_bidders', data=partial_reg_num_bidders_data).fit()
print num_bidders_reg_line.summary()

# partial residual plot for quota_factor
MIN_QUOTA_FACTOR_REG_LINE = 0.05
MAX_QUOTA_FACTOR_REG_LINE = 0.95

partial_reg_quota_factor_data = pd.DataFrame({'quota_factor': mean_err['quota_factor'], \
                                'part_reg': mean_err['residuals'] + mean_err_reg_line.params['quota_factor'] * mean_err['quota_factor'] \
                                            + mean_err_reg_line.params['I(quota_factor ** 2)'] * mean_err['quota_factor']**2})

quota_factor_plt = fig.add_subplot(222)
quota_factor_plt.set_title('Partial Residual Plot for Quota Factor')
quota_factor_plt.set_xlim([MIN_QUOTA_FACTOR_REG_LINE, MAX_QUOTA_FACTOR_REG_LINE])
sns.regplot(x='quota_factor', y='part_reg', order=2, data=partial_reg_quota_factor_data, ax=quota_factor_plt, scatter_kws=SCATTER_PARAMS)
quota_factor_plt.set_xlabel('quota factor')
quota_factor_plt.set_ylabel('partial residual for quota factor')

quota_factor_reg_line = smf.ols(formula='part_reg ~ quota_factor + I(quota_factor**2)', data=partial_reg_quota_factor_data).fit()
print quota_factor_reg_line.summary()

# partial residual plot for cap_var
MIN_CAP_VAR_REG_LINE = 0
MAX_CAP_VAR_REG_LINE = 5.5

partial_reg_cap_var_data = pd.DataFrame({'cap_var': mean_err['cap_var'], \
                                'part_reg': mean_err['residuals'] + mean_err_reg_line.params['cap_var'] * mean_err['cap_var'] \
                                            + mean_err_reg_line.params['I(cap_var ** 2)'] * mean_err['cap_var']**2})

cap_var_plt = fig.add_subplot(223)
cap_var_plt.set_title('Partial Residual Plot for Capacity Std Dev')
cap_var_plt.set_xlim([MIN_CAP_VAR_REG_LINE, MAX_CAP_VAR_REG_LINE])
sns.regplot(x='cap_var', y='part_reg', order=2, data=partial_reg_cap_var_data, ax=cap_var_plt, scatter_kws=SCATTER_PARAMS)
cap_var_plt.set_xlabel('capacity std dev')
cap_var_plt.set_ylabel('partial residual for capacity std dev')

cap_var_reg_line = smf.ols(formula='part_reg ~ cap_var + I(cap_var**2)', data=partial_reg_cap_var_data).fit()
print cap_var_reg_line.summary()

plt.tight_layout()
plt.show()

# slice of data with capacity variance between 0.5 and 6 with num_bidders fixed at 10 and quota_factor fixed at 0.5
cap_var_data = pd.read_csv('cap_var_data_test_5.csv',header=None, names=('sim_id', 'cap_var', 'err'))
mean_cap_var_data = cap_var_data.groupby('cap_var', as_index=False).agg({'err': 'mean'})

sns.regplot(x='cap_var', y='err', order=2, data=mean_cap_var_data)
plt.title('Slice Varying Capacity Std Dev, quota factor = 0.5 and # bidders = 10')
plt.xlabel('capacity std dev')
plt.ylabel('average error')
plt.show()

# slice of data with quota factor between 0.1 and 0.9 with num_bidders fixed at 10 and cap_var fixed at 3
quota_factor_data = pd.read_csv('quota_data_test_5.csv',header=None, names=('sim_id', 'quota_factor', 'err'))
mean_quota_factor_data = quota_factor_data.groupby('quota_factor', as_index=False).agg({'err': 'mean'})

sns.regplot(x='quota_factor', y='err', order=2, data=mean_quota_factor_data)
plt.title('Slice Varying Quota Factor, capacity std dev = 3 and # bidders = 10')
plt.xlabel('quota factor')
plt.ylabel('average error')
plt.show()

# slice of data with num_bidders varied between 2 and 20 with quota_factor fixed at 0.5 and cap_var_fixed at 3
num_bidders_data = pd.read_csv('bidder_count_data_test_5.csv',header=None, names=('sim_id', 'num_bidders', 'err'))
num_bidders_data['num_bidders'] = num_bidders_data['num_bidders'].astype(int)
mean_num_bidders_data = num_bidders_data.groupby('num_bidders', as_index=False).agg({'err': 'mean'})

sns.regplot(x='num_bidders', y='err', order=1, data=mean_num_bidders_data)
plt.title('Slice Varying # Bidders, quota factor = 0.5 and capacity std dev = 3')
plt.xlabel('# bidders')
plt.ylabel('average error')
plt.show()