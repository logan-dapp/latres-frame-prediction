import torch
from PIL import Image
import numpy as np
from diffusers import AutoencoderKL
from typing import Union, Literal, List, Iterator
import os

INITIALIZED: bool = False
vae: AutoencoderKL = None  # None for non-initialized
device: torch.device = None  # None for non-initialized

def check_initialize(model: str = "SG161222/Realistic_Vision_V5.1_noVAE", subfolder: Union[str, bool] = "vae",
                     torch_device: Literal["auto", "cuda", "cpu"] = "auto") -> None:
    global INITIALIZED, vae, device
    if not INITIALIZED:
        if torch_device == "auto":
            torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        if subfolder:
            vae = AutoencoderKL.from_pretrained(model, subfolder=subfolder).to(torch_device)
        else:
            vae = AutoencoderKL.from_pretrained(model).to(torch_device)
        device = torch.device(torch_device)
        INITIALIZED = True

def images_to_latents(path_list: List[str]) -> torch.tensor:
    global vae, device
    check_initialize()

    np_images = [np.array(Image.open(path)) for path in path_list]
    assert all([image.shape == np_images[0].shape for image in np_images]), \
        f"All images must be the same size! (W, H, C) for all images submitted: {', '.join([str(image.shape) for image in np_images])}"

    tc_images = torch.from_numpy(np.array(np_images))
    tc_images = tc_images.type(torch.float) / 127.5 - 1.0
    tc_images = tc_images.permute(0, 3, 1, 2).to(device)

    with torch.no_grad():
        latents = vae.encode(tc_images)
        latents = latents.latent_dist.sample()
        latents = 0.18215 * latents

    return latents

def latents_to_images(latents: torch.tensor, outfolder: Union[None, str] = None,
                     name_generator: Union[Iterator[str], None] = None) -> Union[List[str], List[Image.Image]]:
    global vae, device
    check_initialize()

    latents = 1 / 0.18215 * latents
    with torch.no_grad():
        tc_images = vae.decode(latents).sample
    tc_images = (tc_images / 2 + 0.5).clamp(0, 1)
    np_images = tc_images.detach().cpu().permute(0, 2, 3, 1).numpy()
    np_images = (np_images * 255).round().astype("uint8")
    pil_images = [Image.fromarray(np_image) for np_image in np_images]

    if outfolder is None:
        return pil_images

    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    outpaths = []
    for i, pil_image in enumerate(pil_images):
        if name_generator is None:
            pil_image.save(f'{outfolder}/{i}.png')
            outpaths.append(f'{outfolder}/{i}.png')
            continue
        outfile = next(name_generator)
        pil_image.save(f'{outfolder}/{outfile}')
        outpaths.append(f'{outfolder}/{outfile}')
    return outpaths
