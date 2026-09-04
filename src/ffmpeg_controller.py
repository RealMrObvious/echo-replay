import os
import subprocess
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

# common video encoders prolly
VIDEO_ENCODERS = {
        "H.264 (CPU)": "libx264",
        "H.265 / HEVC (CPU)": "libx265",
        "VP9 (CPU)": "libvpx-vp9",
        "AV1 (CPU)": "libaom-av1",

        "H.264 (NVIDIA)": "h264_nvenc",
        "H.265 / HEVC (NVIDIA)": "hevc_nvenc",
        "AV1 (NVIDIA)": "av1_nvenc",

        "H.264 (AMD)": "h264_amf",
        "H.265 / HEVC (AMD)": "hevc_amf",
        "AV1 (AMD)": "av1_amf",

        "H.264 (Intel)": "h264_qsv",
        "H.265 / HEVC (Intel)": "hevc_qsv",
        "AV1 (Intel)": "av1_qsv",
    }

class FFmpegController(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    error = pyqtSignal(bool, str)
    thumbnail_ready = pyqtSignal(str)

    def __init__(self, target_mb, selected_codec, target_v_res, target_h_res, audio_kbps=128):
        super().__init__()
        self.target_mb = target_mb
        self.audio_kbps = audio_kbps
        self.target_h_res = target_h_res
        self.target_v_res = target_v_res
        self.available_video_encoders = {}
        self.recent_output = None

        self.find_video_encoders()

        for i in self.available_video_encoders.items():
            print(f"Encoders Available: {i}")

        if(selected_codec not in self.available_video_encoders.values()):
            raise ValueError(f"{selected_codec} is not available as an encoder")

        self.selected_codec = selected_codec

    def find_video_encoders(self):
        self.available_video_encoders.clear()

        for codec_full_name, codec_short_name in VIDEO_ENCODERS.items():
            try:
                result = subprocess.run(
                    [
                        "ffmpeg",
                        "-hide_banner",
                        "-loglevel", "error",
                        "-f", "lavfi",
                        "-i", "color=c=black:s=1280x720:d=1",
                        "-c:v", codec_short_name,
                        "-frames:v", "1",
                        "-f", "null",
                        os.devnull,
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10,
                )

                if result.returncode == 0:
                    # print(f"{codec_full_name} ({codec_short_name}): available")
                    self.available_video_encoders[codec_full_name] = codec_short_name

                else:
                    # print(f"{codec_full_name} ({codec_short_name}): unavailable")

                    if result.stderr:
                        print(result.stderr.strip())

            except subprocess.TimeoutExpired:
                print(f"{codec_full_name} ({codec_short_name}): timed out")

            except FileNotFoundError:
                print("FFmpeg was not found.")
                break

            except subprocess.SubprocessError as e:
                print(
                    f"Failed to test {codec_full_name} "
                    f"({codec_short_name}): {e}"
                )

    def _get_duration(self, input_file):
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                str(input_file),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"ffprobe failed:\n{result.stderr.strip()}"
            )

        return float(result.stdout.strip())

    def generate_thumbnail(self, video_path):
            duration = self._get_duration(video_path)
    
            middle = duration / 2
    
            thumbnail_path = "thumbnail.jpg"
    
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-loglevel", "error",
                    "-ss", str(middle),
                    "-i", str(video_path),
                    "-frames:v", "1",
                    "-vf", "scale=320:-1",
                    thumbnail_path,
                ],
                check=True,
            )

            print(f"Thumbnail Ready: {thumbnail_path}")

            self.thumbnail_ready.emit(thumbnail_path)

    def compress_video(self, input_file, output_file=None):
        input_file = Path(input_file)

        if output_file:
            output_file = Path(output_file)
        else:
            output_file = (
                input_file.parent
                / f"{input_file.stem}_compressed{input_file.suffix}"
            )

        actual_bytes = input_file.stat().st_size
        actual_mb = actual_bytes / (1024 * 1024)

        if actual_mb <= self.target_mb:
            print(f"File already fits the size ({actual_mb} <= {self.target_mb})")
            self.progress.emit(100)
            self.recent_output = input_file
            return input_file

        duration = self._get_duration(input_file)

        self.progress.emit(10)
        # Reserve some space for the container.
        target_bytes = self.target_mb * 1024 * 1024 * 0.97

        # Calculate initial video bitrate.
        target_bits = target_bytes * 8
        audio_bits = self.audio_kbps * 1000 * duration

        video_bits = target_bits - audio_bits
        video_kbps = int(video_bits / duration / 1000)

        if video_kbps <= 0:
            raise ValueError("Target size is too small for this video.")

        print(f"Initial video bitrate: {video_kbps} kbps")

        # Try several encodes.
        for attempt in range(5):
            print(
                f"Encoding attempt {attempt + 1}: "
                f"{video_kbps} kbps"
            )

            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-loglevel", "error",
                        "-i", str(input_file),
                        "-vf", f"scale={self.target_h_res}:{self.target_v_res}",
                        "-c:v", self.selected_codec,
                        "-b:v", f"{video_kbps}k",
                        "-c:a", "aac",
                        "-b:a", f"{self.audio_kbps}k",
                        str(output_file),
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(e.stderr)

            actual_bytes = output_file.stat().st_size
            actual_mb = actual_bytes / (1024 * 1024)

            print(f"Result: {actual_mb:.2f} MB")

            # Good enough.
            if actual_mb <= self.target_mb:
                print("Target reached.")
                self.progress.emit(100)
                self.recent_output = output_file
                return output_file

            # Calculate new bitrate based on actual size.
            ratio = self.target_mb / actual_mb
            
            progress_percentage = int(ratio * 100)
            print(ratio, progress_percentage)

            self.progress.emit((progress_percentage))

            # Slight safety margin.
            video_kbps = int(video_kbps * ratio * 0.98)            

        raise RuntimeError(
            f"Could not compress below {self.target_mb} MB "
            f"after {attempt + 1} attempts."
            f"\nConsider lowering the output resolution."
        )


    @pyqtSlot(str)
    def files_received(self, path):
        print(f"Recieved File: {path}, starting encoding")

        if(not path):
            print(f"Path '{path}' doesn't exist")
            self.error.emit(True)
            return False

        try:
            self.generate_thumbnail(path)
            self.compress_video(path)
            self.finished.emit(True, str(self.recent_output))
        except BaseException as e:
            print(f"Error compressing video: {path}")
            self.error.emit(True, str(e))
    


# Testing compressing manually
# if __name__ == "__main__":
#     encoder = FFmpegController(target_mb=19, selected_codec="av1_amf", target_h_res=1920, target_v_res=1080)

#     input_file = Path(r"D:\Clips\Replay 2026-09-01 02-02-59.mp4")

#     encoder.compress_video(input_file)