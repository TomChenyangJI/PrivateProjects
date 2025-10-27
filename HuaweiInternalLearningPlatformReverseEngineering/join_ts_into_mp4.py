import ffmpeg
import numpy as np
import cv2  # Use OpenCV for testing
import io
import subprocess as sp
import threading
from functools import partial

out_filename = 'video.mp4'

# Build synthetic input, and read into BytesIO
###############################################
# Assume we know the width and height from advance
# (In case you don't know the resolution, I posted solution for getting it using FFprobe).
width = 192
height = 108
fps = 10
n_frames = 100

in_filename1 = 'test2/videos/444a010819af11efae05fa163e127b8c0.ts'
in_filename2 = 'test2/videos/444a010819af11efae05fa163e127b8c1.ts'

# Build synthetic video (in1.ts) for testing:
(
    ffmpeg
    .input(f'testsrc=size={width}x{height}:rate=1:duration={n_frames}', f='lavfi', r=fps)
    .filter('setpts', f'N/{fps}/TB')
    .output("./videos/temp1.mp4", vcodec='libx264', crf=17, pix_fmt='yuv420p', loglevel='error')
    .global_args('-hide_banner')
    .overwrite_output()
    .run(cmd="venv/lib/python3.11/site-packages/ffmpeg/_ffmpeg.py")
)

# Build synthetic video (in1.ts) for testing:
(
    ffmpeg
    .input(f'mandelbrot=size={width}x{height}:rate=1', f='lavfi', r=fps)
    .filter('setpts', f'N/{fps}/TB')
    .output("./videos/temp2.mp4", vcodec='libx264', crf=17, pix_fmt='yuv420p', loglevel='error', t=n_frames)
    .global_args('-hide_banner')
    .overwrite_output()
    .run()
)

# Read the file into in-memory binary streams
with open(in_filename1, 'rb') as f:
    in_bytes = f.read()
    stream1 = io.BytesIO(in_bytes)

# Read the file into in-memory binary streams
with open(in_filename2, 'rb') as f:
    in_bytes = f.read()
    stream2 = io.BytesIO(in_bytes)

# Use list instead of dictionary (just for the example).
in_memory_viddeos = [stream1, stream2]


###############################################


# Writer thread: Write to stdin in chunks of 1024 bytes
def writer(decoder_process, stream):
    for chunk in iter(partial(stream.read, 1024), b''):
        decoder_process.stdin.write(chunk)
    decoder_process.stdin.close()


def decode_in_memory_and_re_encode(vid_bytesio):
    """ Decode video in BytesIO, and write the decoded frame into the encoder sub-process """
    vid_bytesio.seek(0)

    # Execute video decoder sub-process
    decoder_process = (
        ffmpeg
        .input('pipe:')  # , f='mpegts', vcodec='h264')
        .video
        .output('pipe:', format='rawvideo', pix_fmt='bgr24')
        .run_async(pipe_stdin=True, pipe_stdout=True)
    )

    thread = threading.Thread(target=writer, args=(decoder_process, vid_bytesio))
    thread.start()

    # Read decoded video (frame by frame), and display each frame (using cv2.imshow for testing)
    while True:
        # Read raw video frame from stdout as bytes array.
        in_bytes = decoder_process.stdout.read(width * height * 3)

        if not in_bytes:
            break

        # Write the decoded frame to the encoder.
        encoder_process.stdin.write(in_bytes)

        # transform the byte read into a numpy array (for testing)
        in_frame = np.frombuffer(in_bytes, np.uint8).reshape([height, width, 3])

        # Display the frame (for testing)
        cv2.imshow('in_frame', in_frame)
        cv2.waitKey(10)

    thread.join()
    decoder_process.wait()


# Execute video encoder sub-process
encoder_process = (
    ffmpeg
    .input('pipe:', r=fps, f='rawvideo', s=f'{width}x{height}', pixel_format='bgr24')
    .video
    .output(out_filename, vcodec='libx264', crf=17, pix_fmt='yuv420p')
    .overwrite_output()
    .run_async(pipe_stdin=True)
)

# Re-encode the "in memory" videos in a loop
for memvid in in_memory_viddeos:
    decode_in_memory_and_re_encode(memvid)

encoder_process.stdin.close()
encoder_process.wait()

cv2.destroyAllWindows()