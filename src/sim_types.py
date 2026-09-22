import numpy as np
from typing import NamedTuple, TypedDict

hr = float
km = float
veh_hr = float
lane_map = dict[int, float]

time_space = np.ndarray[tuple[int, int], np.dtype[np.float64]]
time_vec = np.ndarray[tuple[int], np.dtype[np.float64]]
space_vec = np.ndarray[tuple[int], np.dtype[np.float64]]

class MetanetState(NamedTuple):
  density: space_vec
  velocity: space_vec
  demand: float
  queue: float

class MetanetParams(TypedDict):
  tau: space_vec | time_space
  K: space_vec | time_space
  eta_high: space_vec | time_space
  p_crit: space_vec | time_space
  v_free: space_vec | time_space
  a: space_vec | time_space
  q_capacity: space_vec | time_space
  r: space_vec | time_space
  beta: space_vec | time_space
  gamma: space_vec | time_space