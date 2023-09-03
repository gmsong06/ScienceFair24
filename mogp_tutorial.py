import numpy as np
import joblib
import matplotlib
import matplotlib.pyplot as plt

import mogp

X, Y = mogp.utils.generate_toy_data(seed=0)

num_pat = X.shape[0]
onset_anchor = 48 # normal onset anchor for ALSFRS-R scores
X = np.hstack((np.zeros((num_pat,1)), X))
Y = np.hstack((onset_anchor * np.ones((num_pat,1)), Y))

for i in range(num_pat):
    print(X[i])
    print(Y[i])
    plt.plot(X[i], Y[i], 'o')
    plt.show()

# save_dir = './test'
#
# mix = mogp.MoGP_constrained(X=X, Y=Y, alpha=1., num_iter=10, savepath=save_dir, rand_seed=0, normalize=True)
# mix.sample()
#
# active_cluster_ids = np.where(mix.allocmodel.Nk>0)[0]
# print('Model has {} clusters'.format(len(active_cluster_ids)))
# print('Active Cluster IDs: {}'.format(active_cluster_ids))
#
# print(mix.z)
#
# fig, ax = plt.subplots(figsize=(8,5))
# ax = mogp.utils.plot_mogp(ax=ax, model=mix)