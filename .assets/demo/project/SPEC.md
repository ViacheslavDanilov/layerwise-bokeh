# SPEC: README video

```text
GOAL:    a visitor to the repository finishes the film knowing why the data has to be
         synthetic (real video has no exact depth), that the demo generates one sequence and
         shows its six streams side by side, frame-accurate, down to a single strand of hair.
OUTPUT:  HyperFrames, 1920 x 1080 at 30 fps, rendered at 2x (3840 x 2160) and delivered
         at 1920 x 1080; H.264 High, yuv420p, AAC.
TIME:    99.05 s at 30 fps, 2972 frames. A voice-over of 23 lines over an ambient bed, no beat lock.
SUBJECT: the paper's night scene: seed 245 from the demo's da2-large library, two objects,
         80 frames at 1024 x 1024. The woman with white hair, in focus; a lantern nearer the
         camera, blurred; a lake with fireworks behind them.
LOOK:    ground #ffffff; ink #171717; secondary #666666; lines #e5e5e5. No accent color.
         Inter (assets/fonts): titles 600 at 104-116 px, tracking -0.04 to -0.055 em;
         the strengths and streams headings 600 at 64 px; subtitle and the two lines of a
         problem or solution card 400 at 46 px; tile labels 500 at 32 px; the speed label
         600 at 32 px; end card links 42 px. No subtitles burned in.
         The app is the screen recording, 1920 x 1080 CSS px at 2x. Pulled back it sits at
         scale 0.94 on the white ground: 14 px radius, a 1 px #dedede ring, shadows
         0 4px 12px and 0 30px 80px of #171717 at 6% and 12%. Pushed in, scale 1.17 to 2.4,
         it fills the frame.
OBJECTS: the drawn cursor: a black arrow with a white 1.5 px edge, 36 CSS px, dipping to
         0.84 on each press. No ring on a click.
MOTION:  camera moves 1.0 s power2.inOut (0.9 s onto the progress line), one at a time,
         never across a click; 2D transforms only.
         sheet: full-frame #ffffff, in from x 2050 and out to x -2050, 0.45 s power3.inOut,
         blur 10 px at its fastest. Chapters change this way, and the strengths scene, the
         streams scene and the end card enter this way.
         headline words: opacity 0 to 1 and blur 8 to 0 px, 0.16 s each, 0.08 s apart, no
         move; landed lines hold still. The two lines under a card's headline blur in as
         blocks, 0.3 s, the second 0.15 s after the first.
         poster lines and each card's lines leave rising 28 px with blur 8 px, 0.3 s
         power2.in, 0.08 s apart; the end card's lines rise 28 px into place, 0.55 s
         power3.out, title first, then each link. No whoosh between the poster and the
         cards: they share one white sheet, which whips out only after the first chapter.
SHOTS (film seconds):
  0.00-4.50   poster, finished at frame 0: logo, "LayerWise", subtitle.
  4.50-4.95   poster lines rise out.
  4.95-12.10  problem card: "Real video has no exact depth", under it "To train a
              depth-aware blur model," and "you need the distance of every pixel."
  12.10-12.55 problem lines rise out.
  12.55-20.00 solution card: "Synthetic video, known depth", under it "Objects composited
              onto backgrounds" and "at disparities we assign."
  20.00-23.10 solution lines rise out; "Pick an estimator and a seed" lands; the sheet
              whips out at 23.10 onto the app at 0.94: a falcon and a taxi in three panes,
              two objects in the header and in the sidebar.
  23.55-44.52 sidebar at 2.0x: estimator list, da2-large, seed typed; down to Generate;
              onto the progress line at 2.4x, the speed label once the camera settles;
              the woman and the lantern in one row of three panes at 1.17x; Play, Pause on
              frame 71, give or take one.
  44.52-47.12 sheet "Every stream, side by side".
  47.12-65.03 the row at 1.17x: Add pane twice; then both rows and the transport at
              1.175x: the third Add pane, then two drags: Disparity in front of Optical flow,
              Occlusion in front of Alpha. The top row holds the image-like panes, All in focus,
              Bokeh and Occlusion; the bottom row the data maps, Alpha, Disparity and Optical flow.
  65.03-67.63 sheet "Zoom in, frame by frame".
  67.63-80.05 same framing: double-click on the tips of her hair (4x in all six panes),
              slider dragged four frames, double-click back, Play; the next sheet whips in within
              0.2 s of the press, before the app wraps to frame 1, where Optical flow goes white and Occlusion loses its mask.
  80.05-88.15 sheet "One sequence. Any blur.": All in focus and bokeh strengths 8, 16 and
              32 in one row of four loops, labeled.
  87.55-94.05 sheet "One sequence. Every stream.": six loops in a 3 x 2 grid, labeled, in the
              order the app left its panes (All in focus, Bokeh, Occlusion; Alpha, Disparity,
              Optical flow). Both loop scenes play frames 30 to 79 and start on frame 71.
  93.45-99.05 end card: logo and title, "Code" and "Dataset" links; the music fades out
              from 96.0 s, silence from 98.8 s.
SOUND:   the voice, Kokoro af_heart, 23 lines (voice/lines.tsv), each starting inside a
         pause or a move of the take and ending at least 0.3 s before the next; the chapter
         sheets "Every stream, side by side" and "Zoom in, frame by frame" carry none. Under
         it an ambient bed, ducked so the voice stands about 10 dB over it on average, 8 to 13 dB line by line. A soft click one
         frame after each press, quiet under the voice; a whoosh peaking one frame after each
         sheet's fastest frame, two takes alternating. The file measures -18 LUFS
         integrated, true peak at most -1.5 dBTP, and the last 0.1 s is silent.
BANNED:  a caption strip over the UI; browser chrome; click rings; a gray or dark void
         around a small window; text under 28 px of our own; a spinner without progress
         held over 1 s; a sped-up wait whose bar fills without its factor on screen; the
         logo docked in a corner; panes added or zoomed on a frame where a stream shows
         nothing.
QA:      frames every 2 s and around every seam; text and links unclipped; the speed label
         matches edit.py's factor; audio -18 LUFS, true peak at most -1.5 dBTP, voice 8 to
         12 dB over the bed, every clip ending inside its window with no overlap; the 1080p
         mp4 never over 50 MB and under 100 s, and decoded in full by VideoToolbox.
```
