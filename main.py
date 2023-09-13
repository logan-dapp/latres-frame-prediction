from dataset import HatmanDownloader, VideoSeparator

downloader = HatmanDownloader()
file = next(downloader)
separator = VideoSeparator(file)
separator.get_next_frames()
