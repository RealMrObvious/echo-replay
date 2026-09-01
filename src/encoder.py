import os
import subprocess
from pathlib import Path


class Encoder:
    def __init__(self, target_mb=19, audio_kbps=128):
        self.target_mb = target_mb
        self.audio_kbps = audio_kbps

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

    def compress_video(self, input_file, output_file=None):
        input_file = Path(input_file)

        if not output_file:
            output_file = (
                    input_file.parent
                    / f"{input_file.stem}_compressed{input_file.suffix}"
                )
        else:
            output_file = Path(output_file)

        duration = self._get_duration(input_file)

        # Calculate target video bitrate.
        total_kbps = self.target_mb * 8192 / duration
        video_kbps = int(total_kbps - self.audio_kbps)

        if video_kbps <= 0:
            raise ValueError("Target size is too small for this video.")

        # Keep FFmpeg's 2-pass files next to the output.
        passlog = Path.cwd() / "ffmpeg2pass"

        try:
            # Pass 1
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-loglevel", "error",
                    "-i", str(input_file),
                    "-c:v", "libx264",
                    "-b:v", f"{video_kbps}k",
                    "-pass", "1",
                    "-passlogfile", str(passlog),
                    "-an",
                    "-f", "null",
                    os.devnull,
                ],
                check=True,
            )

            # Pass 2
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-loglevel", "error",
                    "-i", str(input_file),
                    "-c:v", "libx264",
                    "-b:v", f"{video_kbps}k",
                    "-pass", "2",
                    "-passlogfile", str(passlog),
                    "-c:a", "aac",
                    "-b:a", f"{self.audio_kbps}k",
                    str(output_file),
                ],
                check=True,
            )

        finally:
            # FFmpeg can create multiple files using the pass-log prefix.
            for file in passlog.parent.glob(f"{passlog.name}*"):
                try:
                    file.unlink()
                except OSError:
                    pass

        return output_file


if __name__ == "__main__":
    encoder = Encoder(target_mb=19)

    input_file = Path(r"D:\Clips\Replay 2026-09-01 02-02-59.mp4")

    encoder.compress_video(input_file)
