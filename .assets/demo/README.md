# README demo video

`layerwise-bokeh-demo.mp4` is the video the repository's README plays: 99.1 s, 1920 × 1080,
30 fps, with a voice-over, music and sound, encoded from a 3840 × 2160 master. `poster.png`
is its first frame, a finished title card, because GitHub shows a video's first frame until
it plays. The README links a copy uploaded to GitHub, so a new version needs a new upload
too.

The film opens with the title, a problem card and a solution card, then runs the demo, and
a voice reads 23 lines over it ([the transcript](#the-voice-and-the-sound) is below). No
subtitles are burned in, since GitHub's player has no sidecar track.

It shows the paper's night scene at 1024 × 1024: a woman with white hair against
fireworks over a lake, and a lantern nearer the camera. This folder tracks the scripts and
the project, the voice's script and the sound the film plays. The library, the recording,
the loops, the voice clips, the music bed and the master are not tracked; the steps below
remake them.

| Path | What it is |
|---|---|
| `record.cjs` | Records the demo in Chromium through a CDP screencast, with a drawn cursor |
| `edit.py` | Speeds up the generation wait, leaves out frames with an empty pane, and prints the step marks the composition is timed by |
| `stream_frames.py` | Writes the streams' frames for the loop scenes, colored the way the demo colors them |
| `STORYLINES.md` | The storylines considered, the one chosen, and the choices made along the way |
| `project/` | The [HyperFrames](https://github.com/heygen-com/hyperframes) project: HTML scenes rendered to video |
| `project/SPEC.md` | The film's look, motion and shots, in numbers |
| `project/assets/audio/` | `music.mp3`, the mix of the voice and the music bed, the click and the whooshes, the MusicGen clip `bgm0.wav` the bed is made from, and `CREDITS.md` |
| `voice/` | `lines.tsv`, the voice's script and each line's window, `mix.json`, the mix's settings, and `requirements-kokoro.txt`, the voice model's pinned packages |
| `tts.py` | Synthesizes the lines with Kokoro, through the HyperFrames CLI, and checks the model's SHA-256 |
| `make_music.py` | Joins copies of `bgm0.wav` into a longer bed |
| `mix.py` | Places the clips, ducks the bed under them and writes the mix |

## Scenes

| Time | Scene | Content |
|---|---|---|
| 0 to 23.6 s | `compositions/intro.html` | The poster (to 4.5 s), the problem card (4.95 to 12.1 s), the solution card (12.55 to 20 s), then the first chapter's line, all on one white sheet |
| 22.9 to 80.55 s | `compositions/demo.html` | The recording, with a camera and the speed label |
| 44.5 s, 65.0 s | `compositions/sheet-add.html`, `sheet-zoom.html` | Chapter sheets that whip across the recording |
| 80.05 to 88.15 s | `compositions/strengths.html` | The sequence at three bokeh strengths, looping beside All in focus |
| 87.55 to 94.05 s | `compositions/streams.html` | The six streams, looping, in the order the app left its panes: All in focus, Bokeh, Occlusion, Alpha, Disparity, Optical flow |
| 93.45 to 99.05 s | `compositions/end.html` | Logo, the GitHub and Hugging Face addresses |

The sheets sit over the recording while it waits, so the recording runs as one take under
them. `project/assets/` also keeps the shared style (`composition.css`), the logo, Inter
Variable with its license, and GSAP, so the render needs no network.

## The voice and the sound

The voice is `af_heart` of Kokoro, in American English, made by `tts.py`. Each line has a
window in `voice/lines.tsv`: the film second it starts and the latest second it may end,
set from the take's pauses and moves. `mix.py` takes, per line, the first of the speeds
0.97, 1.03 and 1.08 whose clip ends inside its window, so no line is reworded to fit. Every
clip ends at least 0.3 s before the next starts, and the last ends 1.15 s before the film
does. The two
chapter sheets, "Every stream, side by side" and "Zoom in, frame by frame", have no voice.
The name is spelled "Layer Wise" in the text sent to the voice, so that it reads as two
words, and "LayerWise" everywhere else.

Under the voice runs a bed of ambient music: four copies of a 30 s MusicGen clip,
`project/assets/audio/bgm0.wav`, joined with 3 s crossfades and slowed to 95 % of its
speed. The voice goes onto its own bus at -18 LUFS, the bed is brought to -25 LUFS and
ducked by a side-chain compressor keyed by the voice, which then stands 10.6 dB over it on
average (8.3 to 13.2 dB from line to line), and the sum is set so that the whole file
measures -18 LUFS. `project/assets/audio/music.mp3` is that mix, with the bed's fades in
and out, so `index.html` plays it unfaded for the film's full length. The click and the
whooshes stay separate elements there, at volumes 0.9 and 0.25, under the voice.
`project/assets/audio/CREDITS.md` has every sound's source and license.

The transcript, as the voice reads it. Times are the seconds each line starts.

| Line | Start | Text |
|---|---|---|
| V1 | 0.60 | LayerWise generates synthetic video with exact depth. |
| V2 | 5.40 | A model that blurs by depth needs the distance of every pixel. |
| V3 | 9.80 | Real video does not come with it. |
| V4 | 12.90 | LayerWise composites objects onto backgrounds at depths we assign. |
| V5 | 17.60 | So every pixel's depth is known. |
| V6 | 20.55 | Pick a depth estimator and a seed. |
| V7 | 24.70 | Each library comes from one depth estimator. |
| V8 | 28.35 | The seed picks the sequence. |
| V9 | 34.40 | The wait is sped up twenty-one times. |
| V10 | 37.65 | The sequence opens in three panes. |
| V11 | 40.60 | Play it, and pause on a frame. |
| V12 | 47.65 | Add a pane for each stream. |
| V13 | 49.80 | Six streams: all in focus, alpha, disparity, optical flow, occlusion and bokeh. |
| V14 | 55.20 | Drag them into rows: image-like streams above, data maps below. |
| V15 | 61.00 | They play in step, so you can compare them. |
| V16 | 68.50 | A double-click zooms every pane to the same strand of hair. |
| V17 | 73.00 | The slider steps through the frames, and every pane follows. |
| V18 | 77.40 | Then zoom back out, and play. |
| V19 | 81.00 | Bokeh at three strengths, beside the all-in-focus frames. |
| V20 | 85.10 | Each layer is blurred on its own. |
| V21 | 88.47 | All six streams, in step. |
| V22 | 90.75 | They all come from the same layers. |
| V23 | 94.40 | LayerWise. Code on GitHub, dataset on Hugging Face. |

The finished file measures:

| | |
|---|---|
| Length | 99.07 s: 2972 frames at 30 fps, audio 99.07 s |
| Size | 34.5 MB (34,515,725 bytes), 2.8 Mbit/s |
| Video | H.264 High, level 4.1, yuv420p, bt709, 1920 × 1080 |
| Audio | AAC LC, 48 kHz, stereo, 192 kbit/s |
| Loudness | -18.0 LUFS integrated, loudness range 5.4 LU, true peak -2.6 dBTP |
| Voice over bed | 10.6 dB on average, 8.3 to 13.2 dB per line |
| End | the last 0.1 s is silent; the last line ends at 97.90 s |
| Decode | the whole file, `ffmpeg -hwaccel videotoolbox`, with no error |

## The demo's library

The demo serves a small library of one background and seven foregrounds, from the lab's
full library, under four depth estimators. Its folder, `backend/data/library_demo/`, is
ignored like every library.

| Asset | Lab id |
|---|---|
| Background, the night lake with fireworks | `train__h_6dbbc3f6` |
| The woman with white hair | `8V__8V95zPFQAb` |
| Six more foregrounds: a bauble, a falcon, a taxi, a lantern, a helicopter, a porcupinefish | `1Z__1ZwVfuotr0`, `4u__4utFk5cf41`, `6J__6JwGEDXl0A`, `7M__7M7iteGLJW`, `8H__8Hq8GqfviD`, `Xe__Xe17RZvrgx` |

The lab's library has these assets under `da2-large` only, so the other three estimators
are built here from the same source images. From `backend/`, with the lab reachable as
`upf` (read only):

1. Copy the `da2-large` assets:

   ```bash
   LAB=upf:/mnt/storage/projects/upf/layerwise-bokeh/backend/data
   mkdir -p data/library_demo/da2-large/foregrounds data/library_demo/da2-large/backgrounds
   for id in 1Z__1ZwVfuotr0 4u__4utFk5cf41 6J__6JwGEDXl0A 7M__7M7iteGLJW 8H__8Hq8GqfviD 8V__8V95zPFQAb Xe__Xe17RZvrgx; do
     scp -q -r $LAB/library/da2-large/foregrounds/$id data/library_demo/da2-large/foregrounds/
   done
   scp -q -r $LAB/library/da2-large/backgrounds/train__h_6dbbc3f6 data/library_demo/da2-large/backgrounds/
   ```

2. Copy their source images, the MAGICK cut-outs each foreground's `meta.json` names as
   `source_ref`, and the BG-20k photo:

   ```bash
   mkdir -p data/bg-20k_demo/images/train
   for ref in 1Z/1ZwVfuotr0 4u/4utFk5cf41 6J/6JwGEDXl0A 7M/7M7iteGLJW 8H/8Hq8GqfviD 8V/8V95zPFQAb Xe/Xe17RZvrgx; do
     mkdir -p data/magick_demo/images/$(dirname $ref)
     scp -q $LAB/magick/images/$ref.png data/magick_demo/images/$ref.png
   done
   scp -q $LAB/bg-20k/images/train/h_6dbbc3f6.jpg data/bg-20k_demo/images/train/
   ```

3. Build the other estimators, about a minute and a half in all on a Mac:

   ```bash
   for m in da2-base da2-small depth-pro; do
     LAYERWISE_BOKEH_RUNNER=local uv run --extra library python -m layerwise_bokeh.library.build \
       --fg-data-root data/magick_demo --bg-data-root data/bg-20k_demo \
       --output data/library_demo/.$m --model $m && mv data/library_demo/.$m data/library_demo/$m
   done
   ```

## Make the video

The demo must run at `http://localhost:3000` on that library: `make api
LIBRARY=backend/data/library_demo` and `make web` from the repository root. The sequence
it generates must not be cached, or there is no progress bar to film: find its folder with
`grep -l '"seed": 245,' backend/data/sequences/*/sequence.json` and delete it.

1. Record. From this folder:

   ```bash
   node record.cjs 245 frames
   ```

   `DEMO_URL` names the page when it is not on `http://localhost:3000`, say
   `DEMO_URL=http://localhost:3100 node record.cjs 245 frames`; the API's `CORS_ORIGINS`
   must then name that origin too.

   The window is 1920 × 1080 CSS px on a 2× screen, so the frames are 3840 × 2160 and the
   app fills them. Off camera the script sets the size to 1024 × 1024 and the objects to 2
   to 2, and shows seed 6 from the first library, `da2-base`: a falcon and a taxi over the
   same lake, without the woman. It closes that sequence's Alpha and Optical flow panes,
   so the new sequence opens in three panes. On camera it picks `da2-large`, types the
   seed and generates. It plays the new sequence and pauses on frame 71 (`PAUSE_AT`, give or take one), adds
   three panes there, drags Disparity in front of Optical flow and Occlusion in front of Alpha, so the top row holds All in focus, Bokeh and Occlusion and the bottom row Alpha, Disparity and Optical flow, zooms in on her hair, drags the
   position slider four frames, zooms back out and plays. It marks every step and every
   press in `frames/frames.json`. While any pane has no frame to show yet, a red square
   sits in the page's top left corner, and the cursor holds still until every pane has
   shown a frame. Another seed needs its own `PAUSE_AT`, zoom point (`HAIR`) and count of
   objects (`OBJECTS`): pick the frame where Optical flow and Occlusion show her hair and
   she is in focus in Bokeh. Its `SETUP_SEED` must name a sequence of the same size and
   objects that does not show her.

2. Edit. `python3 edit.py frames` leaves out every frame with the red square and holds the
   frame before it instead, so no empty pane reaches the film. Under the first chapter
   sheet the recording waits for the API to encode the streams still to be added, which at
   1024 px outlasts the sheet; the edit cuts that wait while the sheet covers the frame. It
   prints the frames it left out, how many moves of the cursor fall inside them (it must
   be 0), the cut, the generation's speed-up factor, every step mark and press in the
   edit's time and the film's, and an ffmpeg command that writes
   `project/assets/ui-edit.mp4`. Run that command.

3. Time the composition from what `edit.py` printed. `index.html` takes film times, the
   last column, which `edit.py` counts from `DEMO_START`, 22.9 s, where the demo scene
   starts in the film: after the title, the two cards and the first chapter's line.
   `compositions/demo.html` takes edit times, the column before it.

   | Where | Value |
   |---|---|
   | `#sheet-add` and `#sheet-zoom` in `index.html` | `data-start`: the film times of `chapter2` and `chapter3` |
   | `#strengths` | `data-start`: the film time of the last press, the last of the `presses, film` it prints (the press on Play); `data-duration` 8.1, which its four loop videos and the closing no-op tween in `strengths.html` (8.0 s) follow, so that V19 and V20 fit |
   | `#streams` | `data-start`: `#strengths` plus 7.5 |
   | `#end` | `data-start`: `#streams` plus 5.9; the root's `data-duration`: that plus 5.6, which is also the music's, since `music.mp3` carries its own fades |
   | `#demo` and its video | `data-start` 22.9 (`DEMO_START`), `data-duration`: from 22.9 to 0.5 s after `#strengths` starts |
   | `#intro` | `data-duration` 23.6; its sheet whips out at 23.1 s, 0.2 s after `#demo` starts, once the first chapter's line has had its voice line |
   | `#dm-speed` in `demo.html` | the factor; shown at `generate` + 1.2, once the camera has settled on the progress line, and faded out from 0.45 s before the sped-up span ends |
   | the camera in `demo.html` | `estimator` - 0.25, `toGenerate` - 0.18, `generate` + 0.2, `panes` + 0.13, `add2` + 0.1 |
   | `#click-1` to `#click-17` | each press 0.04 s early, so the click peaks a frame after it (`#click-17`, the press on Play, at 80.01 s); the second of a double-click on track 13 |
   | `#whoosh-1` to `#whoosh-8` | each whip: the intro's exit at 23.1 s, each chapter sheet's start and its exit 2.15 s later, the starts of `#strengths`, `#streams` and `#end`; plus 0.096 s for `whoosh-a`, 0.065 s for `whoosh-b` |

   The recording keeps playing after the press on Play, and the app wraps from frame 80,
   which has no flow or occlusion, to frame 1, so its Optical flow pane goes white and its
   Occlusion pane shows the bare gray frame, with no mask. In this take the press is at
   57.15 s in the edit and the first white frame at 57.53 s, 0.38 s after it. The film must
   not show that. The strengths sheet starts with the press, so that three frames before
   the wrap its left edge, 0.28 s in, is already past the Optical flow pane, and the wrap
   lies under the sheet. If the wrap moves, find its first frame in
   `project/assets/ui-edit.mp4`, where the Optical flow pane goes white, and start the sheet
   0.38 s before it.

4. Stream frames. The strengths scene needs the same sequence's bokeh at strengths 8 and
   32 as well, which the API renders as two more sequences of their own: same seed,
   objects, size and frames. With the API running, from anywhere:

   ```bash
   LIB=$(curl -s 127.0.0.1:8000/libraries | python3 -c "import json,sys; print(next(l['id'] for l in json.load(sys.stdin) if l['name'] == 'da2-large'))")
   for k in 8 32; do
     curl -s -X POST 127.0.0.1:8000/sequences -H 'content-type: application/json' -H 'accept: application/json' \
       -d "{\"library\": \"$LIB\", \"seed\": 245, \"frames\": 80, \"size\": 1024, \"n_objects_min\": 2, \"n_objects_max\": 2, \"bokeh_strength\": $k}" \
       | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])"
   done
   ```

   It prints each sequence's id; each takes about a minute. Then from `backend/`, with the
   recorded sequence, which `frames/frames.json` names, and the two just made:

   ```bash
   uv run python ../.assets/demo/stream_frames.py data/sequences/<id> ../.assets/demo/streams
   uv run python ../.assets/demo/stream_frames.py data/sequences/<id of 8> ../.assets/demo/streams/strength-8 bokeh
   uv run python ../.assets/demo/stream_frames.py data/sequences/<id of 32> ../.assets/demo/streams/strength-32 bokeh
   ```

   Each frame is 688 px, a 344 CSS px tile at 2×.

5. Stream loops. Optical flow and Occlusion are nearly blank at the start of the
   sequence and have no last frame, so the loops play frames 30 to 79, 50 frames, not all
   80: from frame 30 their tiles are plain to see. Each stream's 50 frames at 24 fps
   become one 1.875 s cycle at 30 fps, played five and a third times: 300 frames, 10 s.
   Both loop scenes start them 1.54 s in, on frame 71, where the recording paused. From
   this folder, for each `NAME` of `all_in_focus`, `alpha`, `disparity`, `bokeh`, `flow`
   and `occlusion`:

   ```bash
   mkdir -p project/assets/readme-loops
   ffmpeg -y -framerate 24 -start_number 30 -i streams/NAME/%03d.png \
     -vf 'trim=end_frame=50,settb=AVTB,setpts=N/(24*TB),loop=loop=5:size=50:start=0,setpts=0.9*N/(24*TB),fps=30,format=yuv420p' \
     -frames:v 300 -an -c:v libx264 -preset slow -crf 10 \
     -movflags +faststart project/assets/readme-loops/NAME.mp4
   ```

   and the same command with `-i streams/strength-K/bokeh/%03d.png` and
   `project/assets/readme-loops/bokeh-K.mp4` for each `K` of 8 and 32.

6. Voice and music. The voice needs a Python 3.12 environment of its own, outside the
   repository, with the pinned packages. It downloads Kokoro's model on the first run,
   about 350 MB into `~/.cache/hyperframes/tts/`, and `tts.py` stops if a model file's
   SHA-256 differs from the one it names. `tts.py` and `mix.py` themselves run on the
   system Python, which needs numpy, and `ffmpeg`. The voice and its transcript use
   `hyperframes@0.9.81`, the version the model hashes were taken with; the check and the
   render below stay on `hyperframes@0.8.206`, the one this project is pinned to. From
   this folder:

   ```bash
   uv venv --python 3.12 ~/.cache/layerwise-demo/kokoro-venv
   uv pip install --python ~/.cache/layerwise-demo/kokoro-venv/bin/python -r voice/requirements-kokoro.txt
   export HYPERFRAMES_PYTHON=~/.cache/layerwise-demo/kokoro-venv/bin/python
   python3 tts.py --speed 0.97
   python3 make_music.py --copies 4 --out voice/bed.wav
   python3 mix.py
   ```

   `tts.py` writes `voice/vo/<id>_0.97.wav`. `mix.py` stops at a line whose clip ends after
   its window and names it; synthesize that line again at the next speed, say
   `python3 tts.py --speed 1.03 V13`, then `--speed 1.08`, and run `mix.py` again. If a
   line fits at none, lengthen its window in `voice/lines.tsv`, and move the next line if
   the gap falls under 0.3 s; the wording stays. `mix.py` writes `voice/work/mix.wav` and
   `voice/work/mix-report.txt`, which lists each line's speed, end and slack, the mix's
   loudness and true peak, and the voice's margin over the bed. Encode the mix:

   ```bash
   ffmpeg -y -i voice/work/mix.wav -c:a libmp3lame -b:a 192k -ar 48000 project/assets/audio/music.mp3
   ```

   The click and the whooshes are added in the render, so the file's loudness is the
   mix's plus theirs: `voice/mix.json` sets `target_lufs` to -17.8 for the mix so that the
   rendered file measures -18.0. After a render, measure the master with
   `ffmpeg -i master.mp4 -vn -af ebur128=peak=true -f null -`; if it is more than 0.3 LU
   off -18, change `target_lufs` by the difference and run the three commands after the
   export again.

   To check what the voice says, `npx hyperframes@0.9.81 transcribe --json -d <dir>
   voice/vo/V1_0.97.wav` gives its words. Whisper hears "Layer-wise" for the name and, for
   "Bokeh" at the start of V19, "Bouquet", which sounds the same: the voice's phonemes for
   it are `bˈoʊkeɪ`.

7. Check and render a master. From `project/`:

   ```bash
   HYPERFRAMES_SKIP_SKILLS=1 DO_NOT_TRACK=1 npx hyperframes@0.8.206 check
   HYPERFRAMES_SKIP_SKILLS=1 DO_NOT_TRACK=1 npx hyperframes@0.8.206 render \
     --resolution 4k --crf 10 --video-frame-format jpg --frames-cache-dir off -o ../master.mp4
   ```

   `--frames-cache-dir off` keeps the 4K frames it extracts from piling up in the system's
   temporary folder.

8. Encode at 1920 × 1080. From this folder:

   ```bash
   ffmpeg -y -i master.mp4 -vf 'scale=1920:1080:flags=lanczos' -c:v libx264 -preset veryslow \
     -crf 13 -profile:v high -level:v 4.1 -pix_fmt yuv420p -force_key_frames 95.09 \
     -c:a aac -b:a 192k -movflags +faststart layerwise-bokeh-demo.mp4
   ```

   The 4K master, scaled down with Lanczos, keeps the UI text sharper than a render at
   1080p would. CRF 13 makes a file of about 35 MB. `-force_key_frames 95.09` puts a
   keyframe just after the end card has settled, 1.64 s after `#end` starts, so none falls
   inside its hold, where it would show as a jump in quality.

9. Poster. From `project/`:

   ```bash
   HYPERFRAMES_SKIP_SKILLS=1 DO_NOT_TRACK=1 npx hyperframes@0.8.206 snapshot \
     --at 0 --zoom 0,0,1920,1080 --zoom-scale 2 --no-end -o .hyperframes/poster
   cp .hyperframes/poster/frame-00-at-0s.png ../poster.png
   ```

10. Check the file decodes in full on the Mac's hardware decoder:

   ```bash
   ffmpeg -hwaccel videotoolbox -i layerwise-bokeh-demo.mp4 -f null -
   ```

11. Upload. Drag `layerwise-bokeh-demo.mp4` into a GitHub comment box, and put the link it gives
    in place of the `user-attachments` link in the root README.

`npx hyperframes@0.8.206 preview` from `project/` opens the composition in a browser for
checking timing before a render.
