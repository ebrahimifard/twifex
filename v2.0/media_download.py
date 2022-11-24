from tweet_exceptions import *
import requests
import re


class MediaDownload:

    @staticmethod
    def download_photo(photo_urls, saving_path):

        assert isinstance(photo_urls, list), "The photo_urls has to be a list"
        assert isinstance(saving_path, str), "The saving_path has to be a string"

        for photo_url in photo_urls:
            local_filename = photo_url.split('/')[-1]
            response = requests.get(photo_url, stream=True)
            if response.status_code == 200:
                with open(saving_path + local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            elif response.status_code == 404:
                raise PhotoNotFoundInSpecifiedUrl(photo_url)
            else:
                raise OtherPhotoError(f"The error code is {response.status_code}")

    @staticmethod
    def download_video(video_urls, saving_path):

        assert isinstance(video_urls, list), "The video_urls has to be a list"
        assert isinstance(saving_path, str), "The saving_path has to be a string"

        for video_url in video_urls:
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                local_filename = video_url.split('/')[-1]
                reg = re.search(r'^.*\?', local_filename)
                file_name = local_filename[reg.start():reg.end()].replace("?", "")
                with open(saving_path + file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            elif response.status_code == 404:
                raise VideoNotFoundInSpecifiedUrl(video_url)
            else:
                raise OtherVideoError(f"The error code is {response.status_code}")

    @staticmethod
    def download_gif(gif_urls, saving_path):

        assert isinstance(gif_urls, list), "The gif_urls has to be a list"
        assert isinstance(saving_path, str), "The saving_path has to be a string"

        for gif_url in gif_urls:
            response = requests.get(gif_url, stream=True)
            if response.status_code == 200:
                file_name = gif_url.split('/')[-1]
                with open(saving_path + file_name, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            elif response.status_code == 404:
                raise GifNotFoundInSpecifiedUrl(gif_url)
            else:
                raise OtherGifError(f"The error code is {response.status_code}")
