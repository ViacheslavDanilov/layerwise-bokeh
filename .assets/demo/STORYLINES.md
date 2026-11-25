# README video: storylines

Subject: LayerWise's web demo, which generates a synthetic sequence and shows its streams
side by side. Viewer: someone who opened the repository and wants to know, in about a
minute and a half, what the dataset holds and what the demo does with it. One real sequence
travels through every option: the paper's night scene, seed 245 from the `da2-large` library
at 1024 x 1024 with two objects. A woman with long white hair stands against fireworks over
a lake, in focus; a glowing lantern nearer the camera is blurred. Her hair gives the zoom
its fine detail, and the lantern's soft edge gives the blur its proof. The sequence is
generated on camera, so the progress bar is real.

## A. "What hides behind an edge" (chosen)

- **Device and form:** one promise, made over the title and kept in the app. The voice
  names the problem in two parts over the opening: a model that blurs by depth must
  know how far every pixel is, and what hides behind each edge, and real video records
  neither. The title gives way to one slide that says it in three short lines, and the slide
  whips off onto a video already on screen, and the voice gives the
  answer: LayerWise builds its video from layers, so it knows both. The rest is one task
  told as one take inside the real app, with a full-frame white sheet between chapters
  carrying a headline of six words or fewer. Words about hiding recur on purpose ("hides",
  "behind", "covers") as one thread, from the problem to each payoff.
- **What the viewer sees and feels:** an estimator is picked from its list and the seed is
  typed, each with the line that says why it matters (the estimator is swappable, the seed
  brings the sequence back). The bar fills in silence, the panes swap to the new
  sequence, which plays and pauses where her hair moves. Three more panes are added and
  two are dragged into place, the image-like streams in the top row and the data maps
  below, and a double-click zooms all six panes in on the same strands of hair at once.
  The view is held still while the voice says what depth, flow and blur have in common.
  The slider then steps through the frames and the occlusion mask marks what the next frame
  hides. The same sequence loops at three bokeh strengths, where the lantern's soft edge
  shows what lies behind it, and then as its six streams. It feels calm and exact.
- **First two seconds:** the poster: the aperture logo, "LayerWise" and "Synthetic video
  with exact depth, rendered bokeh and optical flow", finished at frame 0, silent for 2 s
  so that it reads as a poster before the voice starts. Its lines then rise out.
- **Beats:** poster, held 2.0 s; one slide of three lines, built under the voice's first
  three lines until 12.6 s; the app, with the earlier sequence
  playing (a falcon and a taxi): estimator list, `da2-large`, seed typed, Generate, progress
  bar (sped up and labeled with its factor), three new panes, Play, a lap of the sequence,
  Pause on frame 71. "Every stream, in step": Add pane three times to a 3 x 2 grid,
  Disparity and Occlusion dragged into place: All in focus, Bokeh and Occlusion above, Alpha,
  Disparity and Optical flow below. "Down to a strand of hair": double-click on the hair, the
  view held, slider dragged four frames, double-click back, Play. "Any blur, layer by
  layer": All in focus beside bokeh strengths 8, 16 and 32, looping. "Six streams, one set
  of layers": the six streams looping, in that same order. End card: logo, the GitHub and
  Hugging Face addresses, held while the music fades under the last line, then faded to the
  white ground.
- **Look:** the app's own: Inter, near-black ink, no accent color. The film's ground is
  white, one step lighter than the app's #fafafa, and pulled back the app sits on it with
  a 1 px border and a soft shadow. Pushed in, the app fills the frame.
- **Sound:** a voice, Kokoro's `af_heart`, over a calm ambient bed, a soft click on every
  press of the mouse and a whoosh on every sheet, both quiet under the voice, the music
  fading out under the end card.

**Why this one:** it is one story. The earlier film opened with the title, a problem card
and a solution card, and then ran a demo whose voice described each step as it happened.
The owner found that it did not flow as one story, and the reasons show in how it was made:
the lines were fitted around holds the recording already had, the two cards said in text what the
voice said again, and the voice read what the screen already showed, such as a list of stream
names. This film is written first and recorded after. The problem is said once, over the
title, in the voice only; the answer lands on a moving picture; each later line says what a
thing is for, never what it is called; and the recording was made again so that its pauses,
the still cursor, the open list, the typed seed, the finished grid and the held zoom, are the
length each line needs.

**How the scenario was made:** three drafts of the scenario were written separately from
the same brief, each with its own voice lines and its own timing table. They were
compared beat by beat, and the draft whose story ran on one thread, what hides behind an
edge, became the base. The others added notes, not text: the six-stream scene is about what
the streams are for, the bar is better left silent, and a seed brings a sequence back from
one library.

## B. "The result first"

- **Device and form:** the payoff opens the film, then the camera pulls back to show where
  it came from.
- **What the viewer sees:** the six streams of one sequence fill the frame and play. The
  camera pulls back until they are panes in the app, and the film rewinds to show the seed
  being typed and the sequence being generated.
- **First two seconds:** the 3 x 2 grid of streams already playing.
- **Beats:** six streams, pull back into the app, rewind, estimator and seed, Generate,
  Add pane, zoom, end card.
- **Look and sound:** as A, with a rewind sound at the turn.
- **Not chosen because:** a poster with the name is the card a visitor expects first, and a
  result-first film shows the six streams twice. The rewind also has to fake the app
  running backwards, which the recording cannot do.

## C. "The hair, then everything"

- **Device and form:** an endless zoom in reverse. The film opens at 4x on one strand of
  hair in six panes and pulls out to the whole frame, then to the app, then to the poster.
- **What the viewer sees:** six views of the same few pixels, color, depth, mask, motion,
  blur and occlusion, before they know what any of them is.
- **First two seconds:** six square crops of the same hair, in six colorings.
- **Beats:** six crops, pull out to six panes, Play, out to the app, end card.
- **Look and sound:** as A, with the bed entering on the first pull-out.
- **Not chosen because:** it is the boldest picture, but a stranger cannot read the
  opening, and the generation, the Add pane clicks and the drag would have no place in it.

The chosen film borrows one thing from C: the zoom is the middle chapter's payoff, on all
six panes at once.

## Choices the brief left open

- **A small library.** The demo serves one background, the night lake, and seven
  foregrounds, the woman among them, copied from the lab's full library. The lab has them
  under `da2-large` only, so `da2-base`, `da2-small` and `depth-pro` are built from the
  same source images on a Mac; the estimator list then shows four entries, as the real app
  does with any directory of libraries. `README.md` says which ids come from where.
- **Size and objects.** 1024 x 1024 and two objects to two, set off camera before the film
  starts and left alone, so on camera only the estimator and the seed change. At 1024 px
  the 4x zoom shows the hair at better than one video pixel to a screen pixel.
- **Three panes to start, and a picture that moves.** The app opens a pane for every stream
  but Occlusion, so a first sequence shows five. Before the recording starts, off camera,
  the page is set to 1024 x 1024 and two objects to two, and generates an earlier sequence
  from the same library with those settings (seed 6, `da2-base`: a falcon and a taxi over
  the same lake, without the woman, so the opener does not give her away). Its Alpha and
  Optical flow panes are closed, and it plays. The app keeps a closed pane closed while the
  streams stay the same, so the new sequence opens in All in focus, Disparity and Bokeh, and
  "Add pane" brings back the other three in stream order. The film therefore opens on a
  sequence already on screen, moving under "builds its video from layers", with its header
  and the sidebar agreeing on two objects, and the progress bar runs in the line above its
  panes rather than on an empty page. The earlier sequence stops as the camera moves in on
  the sidebar: left playing, it would turn into a flicker when the wait is sped up.
- **No empty panes.** The API encodes a stream's video the first time a pane asks for it,
  and a pane reads "Preparing video" until its video has a first frame. Once the new
  sequence is on screen, the recording asks the API for the three videos still to come,
  again and again until each answers at once, so they are on disk before their panes ask.
  Even so a new pane takes a few frames to show its first frame, and the new sequence's
  panes take longer. `record.cjs` puts a red square in the page's corner in every frame
  painted while a pane is empty, and `edit.py` leaves those frames out and holds the frame
  before them. In the film each added pane appears with its first frame, and the earlier
  sequence's panes give way straight to the new ones. The cursor holds still until every
  pane has shown a frame, so no frame left out hides a move of it: it would seem to jump.
  `edit.py` counts the moves that fall inside a span left out, and the count is 0.
- **Where to pause.** On frame 1 her hair has not moved yet: Optical flow is white and
  Occlusion shows a bare gray frame, which reads as broken. So the film plays the new sequence and pauses
  on frame 71, adds the panes there and zooms in there. The frame was picked by measuring
  the sequence inside the zoom window: on frames 70 to 74 the flow there is 10.6 to 17.6 px
  a frame, against 0 on frame 1, Occlusion covers 7 to 9% of it, and she keeps 88 to 99% of
  her all-in-focus detail in Bokeh. Earlier frames have less motion, and on frames 50 to 67
  the renderer leaves her partly out of focus.
- **A lap before the pause.** The voice's line over the playing sequence is 4.3 s long and
  frame 71 is 3 s into it, so the sequence runs a lap and is paused on frame 71 the second
  time. The press of Pause then falls in the silence after the line, and the line, "One
  object holds the focus, and the rest blur by how far they are from it", plays over
  moving frames, including the ones where she is a little soft.
- **Bokeh strengths.** The strengths scene shows the renderer's own output: the API
  generated the same seed, objects, size and frames at bokeh strengths 8 and 32 beside the
  film's 16. Measured against All in focus over the sequence, the background keeps 7%, 3%
  and 1% of its detail at 8, 16 and 32, the lantern 3%, 1% and 0.3%, and the woman 86%, 76%
  and 57% on average: she stays the sharpest thing in every tile, softest on frames 50 to
  67, as at strength 16. The line over the scene, "Each layer is blurred on its own, so the
  lantern's soft edge shows what lies behind it", was checked in the tiles: at strength 32,
  and plainly at 16, the lantern's rim is soft and the lake and the smoke show through it;
  at 8 it is a thin soft line.
- **Where the loops run.** The two loop scenes play frames 30 to 79 of the sequence, not
  all 80. Optical flow and Occlusion are nearly blank at the start, where nothing has
  moved yet (on frames 1 to 25 the flow tile is almost white, and the occlusion mask holds
  hairlines), and the last frame has neither, as it moves nowhere. From frame 30 the
  lantern's and the woman's flow and the mask's edges are plain to see. All eight loops
  share the range, so the tiles of a scene wrap together, and both scenes start on frame
  71, where the recording paused, one wrap hidden under each scene's entering sheet. Each
  loop lasts 13.3 s, and the scenes use at most 12.04 s of it. In these frames the lantern
  touches the woman, in front of her, from frame 45 to frame 71, so the Alpha tile shows one
  object covering the other for about half of each cycle, which is the picture under "even
  where another covers it".
- **Where the take ends.** After the last Play the app runs to frame 80, which has no flow
  or occlusion, and wraps to frame 1, so its Optical flow pane goes white and its Occlusion
  pane shows a bare gray frame. In this take the press is at 61.72 s in the edit and the
  frame break at 62.07 s, 0.35 s after it, and the film does not show it: the strengths
  sheet starts with the press, and its left edge has passed the Optical flow pane 0.15 s
  before the wrap. The take's last beat is Play, without a pull back to the whole app.
- **The wait under the first sheet.** At 1024 px the API can take longer to encode those
  three videos than the first chapter sheet stays up. `edit.py` cuts the rest of that wait
  while the sheet covers the frame, so the cursor moves again as the sheet leaves (0.30 s in
  this take).
- **The sped-up wait.** The wait runs from the click on Generate to the first frame in the
  last pane. `edit.py` speeds it up by a whole number, which the label on screen states:
  68.8 s at 12x lasts 5.7 s in the film, long enough to watch the bar and read the label,
  and the voice stays silent over it. The label comes in once the camera has settled on the
  bar and leaves before the wait ends. For those seconds the app's small step spinner turns
  next to the bar as it fills.
- **Headlines.** "Every stream, in step", "Down to a strand of hair", "Any blur, layer by
  layer", "Six streams, one set of layers": six words or fewer, centered, word by word. The
  film has no sheet before the app and none for the estimator and the seed: the opening
  slide whips straight into the picture the first answer is about. Each headline names the
  chapter's subject, and the voice never repeats it.
- **No card text.** The earlier film's problem and solution cards are gone: a card of text
  and the voice reading it would say everything twice. The problem is said in the voice, and
  the opening slide shows only its nouns, "Distance of every pixel", "What hides behind each
  edge" and the verdict, "Real video has neither", so that a viewer without sound gets the
  problem and the voice adds the sentence.
- **The voice.** 16 lines, each resting on the repository's own words, with numbers as
  words where a line has any. The estimator line describes the pipeline, which accepts a
  depth estimator of one's own, and not a button on screen. The seed line holds for one
  library and settings, which the picture keeps fixed. The line on hair says "a hard
  edge" and no more, which is as far as the repository goes: a depth estimator leaves holes
  around thin structures like hair (`docs/explanation/pipeline-explainer.md`), and a blur
  made from the finished frame gets the edges of objects wrong
  (`docs/explanation/layered-bokeh.md`). The last streams line says the sequence "holds
  the targets". That is the film's word, not the repository's, which calls the sequences
  training data and their alpha, disparity and optical flow exact; the line does not claim
  that any task trains on them. Each line has a
  window set from the take's pauses and moves, and `mix.py` fits the clip to it by speed
  (0.97, 1.03 or 1.08), never by new wording; all 16 fit at 0.97. The voice says "Layer
  Wise" as two words, since a speech model reads "LayerWise" as one.
- **A take sized to the voice.** The recording was made again after the lines were written
  and their clips measured: the cursor holds still for most of the first line over the app, the
  list stays open while the voice names the estimator, the seed is typed slowly under its
  line, the cursor drifts to Generate as that line ends, the finished grid and the hair are
  held for the time two lines need, and the slider moves a frame about every 0.85 s under
  the line about stepping. A hold costs nothing but a few seconds, and the film is 98.7 s.
- **The opening after the owner's first look.** In the merged film the finished title card
  held for 12.6 s while V1 to V3 played over it, and nothing on screen changed. The owner
  watches on GitHub with the sound off and saw a frozen card that made time pass for no
  reason; he asked for the start and the end to be finalized and said one slide in the
  opening is enough. The poster stays frame 0 (`poster.png` is unchanged, since GitHub shows
  it until the video plays) and holds to 2.0 s, where V1 starts. Its lines then rise out and
  one slide builds on the same white ground, in the film's own look, with the three lines at
  fixed positions so that nothing reflows, centered on the frame as the poster is: two
  lines of 72 px, then the headline, 116 px and 600, as the chapter headlines land. They are
  reduced echoes of V1 to V3, four or five words each.
  Timing: the second and the third land as V2 (7.30) and V3 (10.10; the headline at 10.20)
  start. The first lands at 3.0 s and not at V1's start, 2.0 s: from 2.3 s it would have stood
  alone for 4.7 s before the second, and the film's rule is no stretch of identical frames
  over about 4 s. V1's second clause, "a model must know how far every pixel is", starts at
  about 3.7 s, so at 3.0 s the line lands a beat ahead of its words, and the longest stretch
  is 3.7 s (3.6 to 7.3 s). The first line stands alone for 4.3 s, so it has to carry the
  frame: as a gray line of 56 px, about 24 px at the width GitHub plays the video at, it
  read as a caption that had lost its headline. The two smaller lines are therefore 72 px
  and land in ink. As the headline lands they step back to the secondary gray over 0.5 s,
  which leaves the headline as the only ink on the slide, 1.6 times their size, and gives
  the eye one more change at 10.2 s. They turn together, not one at each landing: they are
  two needs of equal rank, and "neither" answers both. Everything holds until
  the whip at 12.6 s, so the sound, the click and the whoosh and every later time stay as
  they were. One slide, not several: the voice says one thought in three breaths, and each
  new slide would be a cut the voice does not make.
- **The ending fades out.** The end card used to hold to the last frame. It now holds under
  V16 and the music's fade, and its content fades to the bare ground over 0.8 s, from 97.67
  s to 98.47 s, which is 0.22 s after V16's clip ends (97.45) and 0.2 s before the last
  frame, so the file ends on a still white frame and the music's last 0.1 s of silence
  still holds. The film is 98.7 s as before. The fade is to white, not to black, since the
  whole film is white from the poster on: a black frame would be the only one in it, and a
  fade to the ground makes the card go away.
- **Silence.** The poster is silent for its first 2 s; the progress bar, both chapter sheets,
  the two drags and the last Play carry no voice; the last 1.25 s are silent too.
- **Where the voice meets the clicks.** Every click stands clear of every line but two: the
  second and third presses of Add pane fall under the line that says to add the streams,
  since its 3.2 s cannot sit between presses 1.5 s apart. They are quiet and soft.
- **Resolution.** A 3840 x 2160 master, delivered at 1920 x 1080: scaled down with
  Lanczos, the master keeps the UI text sharper than a 1080p render, and CRF 13 gives a file
  of about 45 MB.
