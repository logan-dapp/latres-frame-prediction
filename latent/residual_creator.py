import torch

def generate_dataset(latent_reps: torch.tensor):
    residuals = latent_reps[1:] - latent_reps[:-1]
    return latent_reps[:-1], residuals
