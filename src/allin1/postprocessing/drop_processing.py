import torch
from allin1.config import Config
from allin1.postprocessing.helpers import peak_picking
from allin1.typings import AllInOneOutput
from .helpers import local_maxima, peak_picking, event_frames_to_time
import numpy as np


def postprocess_drops(
  logits: AllInOneOutput,
  cfg: Config,
):
  raw_prob_drops = torch.sigmoid(logits.logits_drop[0])
  #raw_prob_functions = torch.softmax(logits.logits_function[0], dim=0)
  prob_drops, _ = local_maxima(raw_prob_drops, filter_size=4 * cfg.min_hops_per_beat + 1)
  prob_drops = prob_drops.cpu().numpy()
  #prob_functions = raw_prob_functions.cpu().numpy()

  drop_candidates = peak_picking(
    boundary_activation=prob_drops,
    window_past=12 * cfg.fps,
    window_future=12 * cfg.fps,
  )
  boundary = drop_candidates > 0.0

  duration = len(prob_drops) * cfg.hop_size / cfg.sample_rate
  pred_drop_times = event_frames_to_time(boundary, cfg)
  """ if pred_drop_times[0] != 0:
    pred_drop_times = np.insert(pred_drop_times, 0, 0)
  if pred_drop_times[-1] != duration:
    pred_boundary_times = np.append(pred_boundary_times, duration)
  pred_boundaries = np.stack([pred_boundary_times[:-1], pred_boundary_times[1:]]).T """

  return pred_drop_times