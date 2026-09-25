import sys, os, pathlib

REPO_DIR = pathlib.Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(REPO_DIR / "src"))

from viz import colored
from sim_types import *
from paths import cut_repo

# Setup freeway info
from data_loader import Freeway

freeway = Freeway(freeway="i24", date="11_30", L=0.4, num_segments=14, time_step=10/3600, time_steps=360, start_time=0.0)
start_time_step = freeway.start_time_step

# Read in the data
CONSTRAINT = None # or "speed_lb", "hold_length", "safety_sweep"
SPEED_LBS = [0]
assert(CONSTRAINT == None or SPEED_LBS == [0])
calibration_id = "calibration_static/fixed_ramping" # default: "calibration_static/fixed_ramping"
calibration_interval = None # None if static, else interval in time steps

_, _, _, lane_cts, data_inflow, downstream_density, p_init, v_init \
             = freeway.load_real_data()
results_path = freeway.results_path(calibration_id, calibration_interval, CONSTRAINT)
model_params = freeway.get_params(calibration_id, calibration_interval)

lane_dict: lane_map = {i: lane_count for i, lane_count in enumerate(lane_cts)}

print(colored("VSL Optimization", "bold", "yellow"))

pred_horizon = 45  # in time steps
control_horizon = 5 # in time steps
hold_len = 1

pad_size = pred_horizon - control_horizon + 2
downstream_density_mpc: time_vec = np.pad(downstream_density, (0, pad_size), mode="edge")
inflow_mpc: time_vec = np.pad(data_inflow, (0, pad_size), mode="edge")

print(data_inflow.shape, '---padding-->', inflow_mpc.shape)

init_state = MetanetState(p_init, v_init, data_inflow[start_time_step], 0.0)

# Optimize I-24 Scenario
import json
from mpc_metanet import mpc_find_vsl

# init_path = f'{results_path}/optimal_vsl_92.npy'
# init_vsl = np.load(init_path)
for speed_lb in SPEED_LBS: #[24, 27, 30]:
    vsl_opt_config = {
        "hold_length": hold_len,
        "control_changepoints": None,
        "safety_temporal": None,
        "safety_spatial": None,
        "speed_lb": speed_lb,
        "warmup_time": 0, 
        "control_zone": [i for i in range(2, freeway.num_segments)], # (0 and 1 uncontrolled)
        "control_one_segment": None, # could get rid? 
        "initialize_vsl": None,
        "init_fixed": None, #[speed_lb, 100, 120, 140, 150], #speed if speed > 0 else None,
        "tee": False,
        "pred_horizon": pred_horizon,
        "control_horizon": control_horizon
    }

    opt_horizon = freeway.time_steps + vsl_opt_config["pred_horizon"] - vsl_opt_config["control_horizon"]  
    optimal_vsl = mpc_find_vsl(opt_horizon, inflow_mpc[start_time_step:], downstream_density_mpc[start_time_step:], lane_dict,
                            T=freeway.time_step,l=freeway.L, num_segments=freeway.num_segments, init_state=init_state, params=model_params, 
                            verbose=True, v_fd_penalty=1e14, **vsl_opt_config)

    path_id = f"optimal_vsl_{speed_lb}" if CONSTRAINT == "speed_lb" else f"optimal_vsl"

    if vsl_opt_config["initialize_vsl"] is not None:
        raise NotImplementedError("Loading from file is not implemented yet")

    np.save(results_path / f'{path_id}.npy', optimal_vsl)
    print(f"Optimal VSL saved to {colored(cut_repo((results_path / f'{path_id}.npy')), 'green')}")

    with open(results_path / f'{path_id}_config.json', "w") as file:
      json.dump(vsl_opt_config, file, indent=4)
    print(f"VSL config saved to {colored(cut_repo((results_path / f'{path_id}_config.json')), 'green')}")