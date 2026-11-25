# README demo video

`layerwise-bokeh-demo.mp4` is the video the repository's README plays: 98.7 s, 1920 × 1080,
30 fps, with a voice-over, music and sound, encoded from a 3840 × 2160 master. `poster.png`
is its first frame, a finished title card, because GitHub shows a video's first frame until
it plays. The README links a copy uploaded to GitHub, so a new version needs a new upload
too.

The film opens on the title, which holds for two seconds. Its lines then rise out and one
slide builds with the voice from the film's own data: the night scene's All in focus, its
Disparity and its Occlusion tiles, looping, each with a short line for what a depth-aware
blur needs, and a headline for what real video lacks. The slide whips straight into the app,
where one sequence goes from an estimator and a seed to a strand of her hair, and a voice
reads 16 lines over it ([the transcript](#the-voice-and-the-sound) is below). The film ends
on the two addresses, which fade to the white ground. No subtitles are burned in, since
GitHub's player has no sidecar track; the opening's tiles and three lines are there for a
viewer who has the sound off.

It shows the paper's night scene at 1024 × 1024: a woman with white hair against
fireworks over a lake, and a lantern nearer the camera. This folder tracks the scripts and
the project, the voice's script and the sound the film plays. The library, the recording,
the loops, the voice clips, the music bed and the master are not tracked; the steps below
remake them.

| Path | What it is |
|---|---|
| `record.cjs` | Records the demo in Chromium through a CDP screencast, with a drawn cursor and pauses sized to the voice |
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
| 0 to 13.1 s | `compositions/intro.html` | The poster, finished at frame 0 and held to 2.0 s; its lines rise out, and one slide builds under V1 to V3 from the sequence's loops: All in focus at 2.7 s, Disparity with "Distance of every pixel" at 3.65 s, Occlusion with "What hides behind each edge" at 7.3 s, then the headline "Real video has neither" at 10.2 s; held, the loops still playing, until its sheet whips off at 12.6 s |
| 12.4 to 74.62 s | `compositions/demo.html` | The recording, with a camera and the speed label |
| 42.1 s, 55.43 s | `compositions/sheet-add.html`, `sheet-zoom.html` | Chapter sheets, "Every stream, in step" and "Down to a strand of hair", that whip across the recording |
| 74.12 to 84.62 s | `compositions/strengths.html` | "Any blur, layer by layer": the sequence at three bokeh strengths, looping beside All in focus |
| 84.0 to 94.1 s | `compositions/streams.html` | "Six streams, one set of layers": the six streams, looping, in the order the app left its panes: All in focus, Bokeh, Occlusion, Alpha, Disparity, Optical flow |
| 93.5 to 98.7 s | `compositions/end.html` | Logo, the GitHub and Hugging Face addresses; the content fades to the white ground from 97.67 to 98.47 s, so the last 0.2 s is bare ground |

The sheets sit over the recording while it waits, so the recording runs as one take under
them. The opening's lines are reduced echoes of V1 to V3, not a transcript. Its tiles are
three of the six stream loops, the ones the voice names: All in focus, the video a model
sees, rises in at 2.7 s, once the title's lines have gone; Disparity, how far every pixel is,
at 3.65 s, where V1's second clause starts, and its line lands at 4.3 s as V1 says how far;
Occlusion, what hides behind each edge, as V2 starts at 7.3 s; the headline 0.1 s after V3
does. The loops keep the slide moving from 2.7 s to the whip, so the only still stretch in
0 to 12.6 s is the poster's first 2.0 s. The tiles are 520 CSS px, larger than the 344 px
of the other scenes, since the slide has three and nothing else to show: the 688 px frames
are still sharper than the 1080p file needs. `project/assets/` also keeps the shared style
(`composition.css`), the logo, Inter Variable with its license, and GSAP, so the render
needs no network.

## The voice and the sound

The voice is `af_heart` of Kokoro, in American English, made by `tts.py`. Each line has a
window in `voice/lines.tsv`: the film second it starts and the latest second it may end,
set from the take's pauses and moves. `mix.py` takes, per line, the first of the speeds
0.97, 1.03 and 1.08 whose clip ends inside its window, so no line is reworded to fit; all
16 fit at 0.97. Every line starts at least 0.25 s after a click or a whoosh and every clip
ends at least 0.41 s before the next starts. The last ends 1.25 s before the film does.
The only clicks under a line are the second and third presses of Add pane under V8; no
line overlaps a whoosh. The two chapter sheets, the progress bar, the drags and the last
Play have no voice. The name is spelled "Layer Wise" in the text sent to the voice, so that
it reads as two words, and "LayerWise" everywhere else.

Under the voice runs a bed of ambient music: four copies of a 30 s MusicGen clip,
`project/assets/audio/bgm0.wav`, joined with 3 s crossfades and slowed to 95 % of its
speed. The voice goes onto its own bus at -18 LUFS, the bed is brought to -25 LUFS and
ducked by a side-chain compressor keyed by the voice, which then stands 10.5 dB over it on
average (8.1 to 13.3 dB from line to line), and the sum is set so that the whole file
measures -18 LUFS. `project/assets/audio/music.mp3` is that mix, with the bed's fades in
and out, so `index.html` plays it unfaded for the film's full length. The click and the
whooshes stay separate elements there, at volumes 0.9 and 0.25, under the voice.
`project/assets/audio/CREDITS.md` has every sound's source and license.

The transcript, as the voice reads it. Times are the seconds each line starts.

| Line | Start | Text |
|---|---|---|
| V1 | 2.00 | To learn to blur by depth, a model must know how far every pixel is. |
| V2 | 7.30 | And what hides behind each edge. |
| V3 | 10.10 | Real video records neither. |
| V4 | 13.50 | LayerWise builds its video from layers instead, so it knows both. |
| V5 | 18.30 | Pick a depth estimator, or bring your own. |
| V6 | 22.10 | A seed picks the sequence, and the same seed always gives it back. |
| V7 | 35.10 | One object holds the focus, and the rest blur by how far they are from it. |
| V8 | 45.40 | Add the streams you need. Every pane shows the same frame. |
| V9 | 59.15 | Hair is a hard edge, for depth and for blur. |
| V10 | 62.20 | Depth, flow and blur follow her matte, since all come from the same layers. |
| V11 | 67.60 | Step frame by frame: the occlusion mask marks what the next frame hides. |
| V12 | 75.12 | You set how strong the blur is, for any sequence. |
| V13 | 78.10 | Each layer is blurred on its own, so the lantern's soft edge shows what lies behind it. |
| V14 | 85.00 | Alpha keeps each object whole, even where another covers it. |
| V15 | 88.80 | One sequence holds the targets for depth, mattes, motion and blur. |
| V16 | 94.50 | Every seed makes another, even while your model trains. |

The finished file measures:

| | |
|---|---|
| Length | 98.71 s: 2961 frames at 30 fps (98.70 s), audio 98.71 s |
| Size | 47.9 MB (47,945,522 bytes), 3.9 Mbit/s |
| Video | H.264 High, level 4.1, yuv420p, bt709, 1920 × 1080 |
| Audio | AAC LC, 48 kHz, stereo, 192 kbit/s |
| Loudness | -18.0 LUFS integrated, loudness range 7.8 LU, true peak -2.1 dBTP |
| Voice over bed | 10.5 dB on average, 8.1 to 13.3 dB per line |
| End | the last 0.1 s is silent; the last line ends at 97.45 s; the card fades from 97.67 s to 98.47 s |
| Opening | the poster holds 2.0 s, the longest stretch of identical frames between 0 and 12.6 s; the loops move from 2.7 s on |
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

The demo must run on that library: `make api LIBRARY=backend/data/library_demo` and `make web`
from the repository root, which serve the API on `http://localhost:8000` and the page on
`http://localhost:3000`. When `:3000` is taken, serve the page elsewhere and let the API
name that origin:

```bash
CORS_ORIGINS=http://localhost:3100 make api LIBRARY=backend/data/library_demo
cd frontend && pnpm exec next dev -p 3100
```

The sequence the film generates must not be cached, or there is no progress bar to film:
find its folder with `grep -l '"seed": 245,' backend/data/sequences/*/sequence.json`, check
in `sequence.json` that its `bokeh_strength` is 16 (the others are the strength 8 and 32
sequences of step 4), and delete that folder. Frames take about 4 GB for one take, so write
them outside the repository.

1. Record. From this folder:

   ```bash
   DEMO_URL=http://localhost:3100 node record.cjs 245 frames
   ```

   `DEMO_URL` names the page when it is not on `http://localhost:3000`. `frames` is any
   folder; the take is about 4,500 JPEG frames of 3840 × 2160.

   The window is 1920 × 1080 CSS px on a 2× screen, so the frames are 3840 × 2160 and the
   app fills them. Off camera the script sets the size to 1024 × 1024 and the objects to 2
   to 2, and shows seed 6 from the first library, `da2-base`: a falcon and a taxi over the
   same lake, without the woman, playing. It closes that sequence's Alpha and Optical flow
   panes, so the new sequence opens in three panes. On camera the earlier sequence plays
   under the voice's first answer and stops, by the Pause button's own handler, as the
   camera moves in on the sidebar, so the sped-up wait does not turn a playing video into
   a flicker. The script then picks `da2-large`, types the seed and generates. It plays the
   new sequence for a lap and a bit more, and pauses on frame 71 (`PAUSE_AT`, give or take
   one), adds three panes there, drags Disparity in front of Optical flow and Occlusion in
   front of Alpha, so the top row holds All in focus, Bokeh and Occlusion and the bottom row
   Alpha, Disparity and Optical flow, zooms in on her hair, holds the zoomed view still
   while two lines of the voice play, drags the position slider four frames, zooms back out
   and plays. It marks every step and every press in `frames/frames.json`. While any pane
   has no frame to show yet, a red square sits in the page's top left corner, and the cursor
   holds still until every pane has shown a frame.

   Every pause is sized to the voice. Up to Generate the beats sit on the take's own clock,
   `BEAT` at the top of the script, in seconds after the screencast starts; the edit leaves
   that stretch at 1× and the film starts the take 12.4 s in, so a beat at 5.5 s is at
   17.9 s of the film. After Generate each pause is a length: the new panes rest for about
   a second before Play, the sequence runs `LAPS` laps before it is paused (so that the line
   over it ends before the press of Pause), and `HOLD.zoomStill` holds the zoomed view
   still from the double-click to the slider's press. A cursor glide takes exactly the time
   it is given, so the beats hold whatever the load. Another seed needs its own
   `PAUSE_AT`, zoom point (`HAIR`) and count of objects (`OBJECTS`): pick the frame where
   Optical flow and Occlusion show her hair and she is in focus in Bokeh. Its `SETUP_SEED`
   must name a sequence of the same size and objects that does not show her.

2. Edit. `python3 edit.py frames` leaves out every frame with the red square and holds the
   frame before it instead, so no empty pane reaches the film. Under the first chapter
   sheet the recording waits for the API to encode the streams still to be added; the edit
   cuts the part of that wait the sheet would not cover (0.30 s in this take). It prints the
   frames it left out (31 in this take), how many moves of the cursor fall inside them (it
   must be 0), the cut, the generation's speed-up factor (68.8 s at 12×, 5.73 s in the edit,
   from 15.32 s), every step mark and press in the edit's time and the film's, and an ffmpeg
   command that writes `project/assets/ui-edit.mp4`, 64.03 s. Run that command.

3. Time the composition from what `edit.py` printed. `index.html` takes film times, the
   last column, which `edit.py` counts from `DEMO_START`, 12.4 s, where the demo scene
   starts in the film: after the title. `compositions/demo.html` takes edit times, the
   column before it. The times of this take:

   | Where | Value |
   |---|---|
   | `#sheet-add` and `#sheet-zoom` in `index.html` | `data-start`: the film times of `chapter2` and `chapter3`, 42.10 s and 55.43 s |
   | `#strengths` | `data-start`: the film time of the last press, the last of the `presses, film` it prints (the press on Play), 74.12 s; `data-duration` 10.5, which its four loop videos and the closing no-op tween in `strengths.html` (10.4 s) follow, so that V12 and V13 fit and the scene holds 0.9 s after V13 |
   | `#streams` | `data-start`: `#strengths` plus 9.88, 84.0 s; `data-duration` 10.1, which its six loop videos and the closing tween (10.0 s) follow |
   | `#end` | `data-start`: `#streams` plus 9.5, 93.5 s; the root's `data-duration`: that plus 5.2, which is also the music's, since `music.mp3` carries its own fades; the card's content fades to the white ground over 0.8 s from 4.17 s in its own time (97.67 s), 0.2 s before the last frame, after V16 has ended (97.45 s) |
   | `#demo` and its video | `data-start` 12.4 (`DEMO_START`), `data-duration`: from 12.4 to 0.5 s after `#strengths` starts, 62.22 s |
   | `#intro` | `data-duration` 13.1; the poster holds to 2.0 s, its lines rise out from 2.0 s (the subtitle from 2.3 s), and the slide's tiles rise in at 2.7 s (All in focus), 3.65 s (Disparity, V1's second clause) and 7.3 s (Occlusion, V2), each line under a tile landing word by word, 0.16 s apart, at 3.1 s, 4.3 s and 7.7 s, and the headline at 10.2 s (V3); the three loops run on one clock from the scene's start, `data-media-start` 0.2 (see step 5); its sheet whips out at 12.6 s, 0.2 s after `#demo` starts |
   | `#dm-speed` in `demo.html` | the factor; shown at `generate` + 1.2 (16.1 s in the edit), once the camera has settled on the progress line, and faded out from 0.45 s before the sped-up span ends (20.55 s) |
   | the camera in `demo.html` | `push` 3.9 (the first beat of the take, `BEAT.push`), 11.5 (before the cursor drifts to Generate), `generate` + 0.2, `panes` + 0.05 (0.85 s long, so it ends before the press on Play), `add2` + 0.1 |
   | `#click-1` to `#click-17` | each press 0.04 s early, so the click peaks a frame after it (`#click-17`, the press on Play, at 74.08 s); the second of a double-click on track 13 |
   | `#whoosh-1` to `#whoosh-8` | each whip: the intro's exit at 12.6 s, each chapter sheet's start and its exit 2.15 s later, the starts of `#strengths`, `#streams` and `#end`; plus 0.096 s for `whoosh-a`, 0.065 s for `whoosh-b` |
   | `voice/lines.tsv` | each line's start and latest end, in film seconds, from the marks: a line starts in a pause or a move, 0.25 s or more after a click or a whoosh, and ends before the next click or whoosh, but for V8, which runs over two clicks |

   The recording keeps playing after the press on Play, and the app wraps from frame 80,
   which has no flow or occlusion, to frame 1, so its Optical flow pane goes white and its
   Occlusion pane shows the bare gray frame, with no mask. In this take the press is at
   61.72 s in the edit and the first white frame at 62.07 s, 0.35 s after it. The film must
   not show that. The strengths sheet starts with the press, so that its left edge is
   already past the Optical flow pane 0.15 s before the wrap, and the wrap lies under the
   sheet. If the wrap moves, find its first frame in `project/assets/ui-edit.mp4`, where the
   Optical flow pane goes white, and start the sheet 0.35 s before it.

4. Stream frames. The strengths scene needs the same sequence's bokeh at strengths 8 and
   32 as well, which the API renders as two more sequences of their own: same seed,
   objects, size and frames. They are made once and stay cached. With the API running, from
   anywhere:

   ```bash
   LIB=$(curl -s 127.0.0.1:8000/libraries | python3 -c "import json,sys; print(next(l['id'] for l in json.load(sys.stdin) if l['name'] == 'da2-large'))")
   for k in 8 32; do
     curl -s -X POST 127.0.0.1:8000/sequences -H 'content-type: application/json' -H 'accept: application/json' \
       -d "{\"library\": \"$LIB\", \"seed\": 245, \"frames\": 80, \"size\": 1024, \"n_objects_min\": 2, \"n_objects_max\": 2, \"bokeh_strength\": $k}" \
       | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])"
   done
   ```

   It prints each sequence's id (at once when it is cached, else after about a minute).
   Then from `backend/`, with the recorded sequence, which `frames/frames.json` names, and
   the two just made:

   ```bash
   uv run python ../.assets/demo/stream_frames.py data/sequences/<id> ../.assets/demo/streams
   uv run python ../.assets/demo/stream_frames.py data/sequences/<id of 8> ../.assets/demo/streams/strength-8 bokeh
   uv run python ../.assets/demo/stream_frames.py data/sequences/<id of 32> ../.assets/demo/streams/strength-32 bokeh
   ```

   Each frame is 688 px, a 344 CSS px tile at 2×.

5. Stream loops. Optical flow and Occlusion are nearly blank at the start of the
   sequence and have no last frame, so the loops play frames 30 to 79, 50 frames, not all
   80: from frame 30 their tiles are plain to see. Each stream's 50 frames at 24 fps
   become one 1.875 s cycle at 30 fps, played a little over seven times: 400 frames, 13.3 s.
   The strengths and streams scenes start them 1.54 s in, on frame 71, where the recording
   paused, and show them for 10.5 s and 10.1 s, so 12.04 s of loop is the most they use. The
   opening shows All in focus, Disparity and Occlusion for 13.1 s, from its start on one
   clock, so they stay in step whenever a tile rises in: `data-start` 0 and
   `data-media-start` 0.2, which plays to 13.3 s of the 13.33 s a loop lasts. No frame of the
   loop is empty (Occlusion's mask is plain to see from frame 30 on), so the start is chosen
   for the tiles, not the mask: it puts a wrap of the cycle, 1.875 s long, at 7.3 s, so that
   Occlusion rises in on the loop's first frame, where the woman's hair and the lantern's
   rim are outlined in cyan, and another at 12.93 s, under the whip. From this
   folder, for each `NAME` of `all_in_focus`, `alpha`, `disparity`, `bokeh`, `flow` and
   `occlusion`:

   ```bash
   mkdir -p project/assets/readme-loops
   ffmpeg -y -framerate 24 -start_number 30 -i streams/NAME/%03d.png \
     -vf 'trim=end_frame=50,settb=AVTB,setpts=N/(24*TB),loop=loop=7:size=50:start=0,setpts=0.9*N/(24*TB),fps=30,format=yuv420p' \
     -frames:v 400 -an -c:v libx264 -preset slow -crf 10 \
     -movflags +faststart project/assets/readme-loops/NAME.mp4
   ```

   and the same command with `-i streams/strength-K/bokeh/%03d.png` and
   `project/assets/readme-loops/bokeh-K.mp4` for each `K` of 8 and 32.

   Look at the tiles before the voice's wording is final. In this sequence the lantern
   touches the woman on frames 45 to 71 of the loops (in front of her, over her white
   dress), so the Alpha tile shows one object covering the other for about half of each
   cycle. At strength 32, and plainly at 16, the lantern's rim is soft and the lake and
   the smoke show through it; at 8 the rim is a thin soft line. V13 says so.

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
   line fits at none, lengthen its hold in the recording or its window in
   `voice/lines.tsv`, and move the next line if the gap falls under 0.3 s; the wording
   stays. `mix.py` writes `voice/work/mix.wav` and `voice/work/mix-report.txt`, which lists
   each line's speed, end and slack, the mix's loudness and true peak, and the voice's
   margin over the bed. Encode the mix:

   ```bash
   ffmpeg -y -i voice/work/mix.wav -c:a libmp3lame -b:a 192k -ar 48000 project/assets/audio/music.mp3
   ```

   The click and the whooshes are added in the render, so the file's loudness is the
   mix's plus theirs: `voice/mix.json` sets `target_lufs` to -17.8 for the mix so that the
   rendered file measures -18.0. After a render, measure the master with
   `ffmpeg -i master.mp4 -vn -af ebur128=peak=true -f null -`; if it is more than 0.3 LU
   off -18, change `target_lufs` by the difference and run the three commands after the
   export again. `voice/mix.json` also holds the film's duration and where the bed fades
   out, 96.0 s to 0.25 s before the end; change both with the film's length.

   To check what the voice says, `npx hyperframes@0.9.81 transcribe --json -d <dir>
   voice/vo/V1_0.97.wav` gives its words. Whisper hears "LayerWise" as one word, as the
   screen writes it, and spells "matte" as "mat", which sounds the same.

7. Check and render a master. From `project/`:

   ```bash
   HYPERFRAMES_SKIP_SKILLS=1 DO_NOT_TRACK=1 npx hyperframes@0.8.206 check
   HYPERFRAMES_SKIP_SKILLS=1 DO_NOT_TRACK=1 npx hyperframes@0.8.206 render \
     --resolution 4k --crf 10 --video-frame-format jpg --frames-cache-dir off -o ../master.mp4
   ```

   `--frames-cache-dir off` keeps the 4K frames it extracts from piling up in the system's
   temporary folder. The render takes about two and a half minutes and the master is about
   420 MB.

8. Encode at 1920 × 1080. From this folder:

   ```bash
   ffmpeg -y -i master.mp4 -vf 'scale=1920:1080:flags=lanczos' -c:v libx264 -preset veryslow \
     -crf 14 -profile:v high -level:v 4.1 -pix_fmt yuv420p -force_key_frames 95.14 \
     -c:a aac -b:a 192k -movflags +faststart layerwise-bokeh-demo.mp4
   ```

   The 4K master, scaled down with Lanczos, keeps the UI text sharper than a render at
   1080p would. CRF 14 makes a file of about 48 MB, under the 50 MB limit (CRF 13 made 54.6 MB,
   since the opening's three larger loops compress worse); raise the CRF if a longer film or
   loops that compress worse push it past. `-force_key_frames 95.14` puts a
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
