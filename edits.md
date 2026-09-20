1. environment-new.yml
Had Codex rewrite environment.yml because `blas=1.0=mkl` doesn't work on my hardware (Apple Silicon)

2. mpc_metanet.py
```diff
-import scipy.sparse as sp
-import pandas as pd
-import pyomo.contrib.parmest.utils.ipopt_solver_wrapper as ipopt_solver_wrapper
```

```diff
mpc_opt():
- solver = pyo.SolverFactory('ipopt', executable='/usr/local/bin/ipopt')
+ solver = pyo.SolverFactory('ipopt')

-status, _, iters, _, _ = ipopt_solver_wrapper.ipopt_solve_with_stats(
-        model, solver,
-        max_iter=40000, max_cpu_time=180,
-        warmstart=(init_vsl is not None), tee=tee,
-    )
+    status = solver.solve(model, options={'max_iter': 40000, 'max_cpu_time': 180}, tee=tee)
+    iters = 0
```
ipopt_solver_wrapper.ipopt_solve_with_stats doesn't accept `warmstart` and `tee` arguments in my code.

3. run_controllable_congestion.ipynb
```diff
-plt.savefig("/Users/shreyaar/Desktop/PhD/research/MPC/figs/11_22_tsdiagram", dpi=150, bbox_inches='tight')
+plt.savefig("/Users/tristanchaang/MIT/UROP-Traffic/mpc-traffic-flow/figs/11_22_tsdiagram", dpi=150, bbox_inches='tight')
```

```diff
-optimal_vsl = np.load(f'{results_path}/optimal_vsl_54.npy')
+optimal_vsl = np.load(f'{results_path}/optimal_vsl.npy')
```
optimal_vsl_54.npy doesn't exist on the repo, so I changed it to optimal_vsl.npy

```diff
-delay_gt   = (0.4 / velocity_data[:, 1:-1].T - 0.4 / free_flow_speed_2d) * 60
+delay_gt   = (0.4 / velocity_data.T - 0.4 / free_flow_speed_2d) * 60

-im0 = axs[0].imshow(velocity_data[:, 1:-1].T, .........)
+im0 = axs[0].imshow(velocity_data.T, .........)
```
`velocity_data` with `[1:-1]` makes it have 12 segments instead of 14 (total including boundary should be 16)

5. metanet_calibration.ipynb

```diff
-plt.plot(r_inflow_array[:, 1])
+plt.plot(r_inflow_array)

-param_array = mpc_params[param][:, 6]
+param_array = params[param][:]
```

6. plotting.py

```diff
-p_nocontrol, v_nocontrol, tts_nocontrol, queue_nocontrol= run_metanet_sim(...): ...
+p_nocontrol, v_nocontrol, queue_nocontrol, tts_nocontrol= run_metanet_sim(...): ...
```

7. viz.py

Self class for plotting