# SPEC: README video

```text
GOAL:    a visitor to the repository finishes the film knowing what a depth-aware blur needs
         (how far every pixel is, and what hides behind each edge), that real video records
         neither, and that LayerWise's layers give both: one sequence generated in the demo,
         its six streams side by side in step, down to a single strand of hair.
OUTPUT:  HyperFrames, 1920 x 1080 at 30 fps, rendered at 2x (3840 x 2160) and delivered
         at 1920 x 1080; H.264 High, yuv420p, AAC.
TIME:    98.7 s at 30 fps, 2961 frames. A voice-over of 16 lines over an ambient bed, no beat lock.
SUBJECT: the paper's night scene: seed 245 from the demo's da2-large library, two objects,
         80 frames at 1024 x 1024. The woman with white hair, in focus; a lantern nearer the
         camera, blurred; a lake with fireworks behind them.
LOOK:    ground #ffffff; ink #171717; secondary #666666; lines #e5e5e5. No accent color.
         Inter (assets/fonts): titles 600 at 104-116 px, tracking -0.04 to -0.055 em;
         the strengths and streams headings 600 at 64 px; subtitle 400 at 46 px; the
         opening's two smaller lines 400 at 72 px, ink until its headline lands and
         #666666 after; tile labels 500 at 32 px; the speed label 600 at 32 px; end card
         links 42 px. No subtitles burned in.
         The app is the screen recording, 1920 x 1080 CSS px at 2x. Pulled back it sits at
         scale 0.94 on the white ground: 14 px radius, a 1 px #dedede ring, shadows
         0 4px 12px and 0 30px 80px of #171717 at 6% and 12%. Pushed in, scale 1.17 to 2.4,
         it fills the frame.
OBJECTS: the drawn cursor: a black arrow with a white 1.5 px edge, 36 CSS px, dipping to
         0.84 on each press. No ring on a click.
MOTION:  camera moves 1.0 s power2.inOut (0.9 s onto the progress line, 0.85 s onto the new
         panes), one at a time, never across a click; 2D transforms only.
         sheet: full-frame #ffffff, in from x 2050 and out to x -2050, 0.45 s power3.inOut,
         blur 10 px at its fastest. The opening slide leaves this way, chapters change this way, and
         the strengths scene, the streams scene and the end card enter this way.
         headline words: opacity 0 to 1 and blur 8 to 0 px, 0.16 s each, 0.08 s apart, no
         move; landed lines hold still. The opening's three lines land the same way, but
         0.16 s apart, and its two smaller lines turn from ink to #666666, 0.5 s
         power2.out, as its headline lands.
         the end card's lines rise 28 px into place, 0.55 s power3.out, title first, then
         each link. The poster's lines rise out the same way (28 px up, 0.6 s power2.inOut,
         opacity and blur to 0, the title at 2.0 s and the subtitle at 2.3 s); the poster
         holds still until 2.0 s, as the film's first frame. At the end the card's content
         fades to the bare white ground, opacity 1 to 0 with blur to 6 px, 0.8 s power1.inOut.
SHOTS (film seconds):
  0.00-2.00   poster, finished at frame 0: logo, "LayerWise", subtitle. Held still.
  2.00-2.90   the poster's lines rise out (title, then subtitle). V1 starts at 2.00.
  3.00-12.60  one slide, three lines at fixed positions so nothing reflows, centered on
              the frame (ink from y 382 to 698): "Distance of every pixel" (400, 72 px,
              #171717) lands at 3.00, a beat before V1's second clause (about 3.7);
              "What hides behind each edge" (same) at 7.30 with V2; "Real video has
              neither" (600, 116 px, #171717) at 10.20, 0.1 s after V3 starts, and the
              first two turn #666666 from 10.20 to 10.70. All three hold until the whip.
              No stretch of identical frames over 3.7 s.
  12.60-13.05 the opening slide's sheet whips off to the left, onto the app at 0.94 already on
              screen: a falcon and a taxi playing in three panes, two objects in the header
              and in the sidebar. The cursor holds still until 16.8 s.
  16.30-23.45 camera in on the sidebar at 2.0x as the falcon and the taxi stop: estimator
              list opened (17.90), da2-large picked (20.70), seed field pressed (21.70), 245
              typed (22.2 to 23.45).
  23.90-27.30 camera down to Generate at 2.0x; the cursor drifts there slowly and rests.
  27.30-33.45 Generate pressed; the camera onto the progress line at 2.4x; the wait at 12x
              with its label, "12× speed", from 28.5 s to 32.95 s.
  33.50-41.08 the woman and the lantern in one row of three panes at 1.17x: Play at 34.66,
              a lap of the sequence, Pause on frame 71 at 40.97, give or take one.
  42.10-44.70 sheet "Every stream, in step".
  45.08-55.43 Add pane three times (45.08, 46.51, 47.96; each new pane shows a frame before
              the next press), both rows and the transport at 1.175x from the second; two
              drags: Disparity in front of Optical flow (49.82 to 51.33), Occlusion in front
              of Alpha (52.47 to 53.99). The top row holds the image-like panes, All in
              focus, Bokeh and Occlusion; the bottom row the data maps, Alpha, Disparity
              and Optical flow. The finished grid is held.
  55.43-58.03 sheet "Down to a strand of hair".
  58.41-74.12 same framing: double-click on the tips of her hair (4x in all six panes),
              held still for 8.6 s until the slider's press (67.16), slider dragged four
              frames in 3.7 s, double-click back (72.65), Play (74.12); the next sheet whips
              in with that press, before the app wraps to frame 1, where Optical flow goes
              white and Occlusion loses its mask.
  74.12-84.62 sheet "Any blur, layer by layer": All in focus and bokeh strengths 8, 16 and
              32 in one row of four loops, labeled.
  84.00-94.10 sheet "Six streams, one set of layers": six loops in a 3 x 2 grid, labeled,
              in the order the app left its panes (All in focus, Bokeh, Occlusion; Alpha,
              Disparity, Optical flow). Both loop scenes play frames 30 to 79 and start on
              frame 71.
  93.50-98.70 end card: logo and title, "Code" and "Dataset" links; the music fades out
              from 96.0 s, silence from 98.6 s. The card's content fades to the white
              ground from 97.67 to 98.47 s, after V16 has ended (97.45 s), so the last
              0.2 s is bare ground.
SOUND:   the voice, Kokoro af_heart, 16 lines (voice/lines.tsv), each starting inside a
         pause or a move of the take, 0.25 s or more after any click or whoosh, and ending
         at least 0.4 s before the next line. No line overlaps a whoosh; the only clicks under a
         line are two of the three Add pane presses, under V8. The two chapter sheets, the
         progress bar, the drags and the last Play carry no voice. Under it an ambient bed,
         ducked so the voice stands about 10.5 dB over it on average, 8 to 13 dB line by
         line. A soft click one frame after each press, quiet under the voice; a whoosh
         peaking one frame after each sheet's fastest frame, two takes alternating. The file
         measures -18 LUFS integrated, true peak at most -1.5 dBTP, and the last 0.1 s is
         silent.
BANNED:  a caption strip over the UI; browser chrome; click rings; a gray or dark void
         around a small window; text under 28 px of our own; a spinner without progress
         held over 1 s; a sped-up wait whose bar fills without its factor on screen; the
         logo docked in a corner; panes added or zoomed on a frame where a stream shows
         nothing; a voice line that reads a label or an address on screen.
QA:      frames every 2 s (every 0.5 s over 0 to 14 s and the last 6 s) and around every
         seam; no stretch of identical frames over about 4 s between 0 and 12.6 s; text
         and links unclipped; the speed label matches edit.py's factor; audio -18 LUFS, true
         peak at most -1.5 dBTP, voice 8 to 13 dB over the bed, every clip ending inside its
         window with no overlap; the 1080p mp4 never over 50 MB and under 100 s, and decoded
         in full by VideoToolbox.
```
