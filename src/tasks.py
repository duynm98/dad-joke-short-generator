import os
import shutil
from uuid import uuid4

from loguru import logger

from src import config
from src.jokes import get_random_joke
from src.images import get_images, image2video
from src.voice import create_voice_and_subtitle
from src.video import generate_video
from src.models.schema import VideoParams
from src import telebot


def init_task() -> str:
    task_id = str(uuid4())
    os.makedirs(os.path.join(config.output_folder, task_id), exist_ok=True)
    logger.info(f"Successfully init task: {task_id}")
    return task_id


def execute_task(task_id: str, delete_on_complete: bool = False):
    output_folder = os.path.join(config.output_folder, task_id)

    joke = get_random_joke()
    assert "setup" in joke and "punchline" in joke, f"Missing either setup or punchline: {joke}"

    images_folder = os.path.join(output_folder, "images")
    os.makedirs(images_folder, exist_ok=True)
    images = get_images(query=joke["setup"], output_folder=images_folder, amount=1)
    assert len(images) > 0, "No images found"
    image = images[0]

    audio_path = os.path.join(output_folder, "audio.mp3")
    subtitle_output_file, audio_duration = create_voice_and_subtitle(
        voice_name="en-US-AndrewNeural-Male",
        text="Joke of the Day: " + joke["setup"] + "\n... " * 4 + joke["punchline"],
        voice_output_file=audio_path,
        voice_rate=0.9,
    )

    video_path = os.path.join(output_folder, "video.mp4")
    image2video(image, video_path, audio_duration)

    final_video_path = os.path.join(output_folder, "video-final.mp4")
    generate_video(
        video_path=video_path, audio_path=audio_path, subtitle_path=subtitle_output_file, output_file=final_video_path, params=VideoParams()
    )

    logger.success(f"Task {task_id} completed!")

    telebot.send_message(f"Joke of the Day! #jokeoftheday #dadjoke #joke #comedy")
    telebot.send_message(f"Joke of the Day! {joke['setup']} #jokeoftheday #dadjoke #joke #comedy")
    telebot.send_video(final_video_path, caption=task_id)

    if delete_on_complete:
        shutil.rmtree(output_folder, ignore_errors=True)
        logger.info(f"All files in {output_folder} have been deleted")


if __name__ == "__main__":
    task_id = init_task()
    execute_task(task_id, delete_on_complete=True)
