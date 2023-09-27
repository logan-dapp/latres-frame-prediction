from dataset import HatmanDownloader, VideoSeparator, make_square
from latent import images_to_latents, latents_to_images, generate_dataset, check_initialize

check_initialize(torch_device='cuda')
downloader = HatmanDownloader()
file = next(downloader)

separator = VideoSeparator(file)
image_paths = separator.get_next_frames(frames=2)
for image_path in image_paths:
    make_square(image_path, outpath=image_path)
latents = images_to_latents(image_paths)
X_dat, Y_dat = generate_dataset(latents)
latents_to_images(X_dat+Y_dat, 'output_images')
