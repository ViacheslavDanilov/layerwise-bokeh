# LayerWise demo container

Generate a synthetic video from one of four depth estimators and compare its all-in-focus,
bokeh, disparity, alpha, optical flow, and occlusion streams. The demo runs on CPU with
one background and seven foregrounds per estimator.

See [Deploy the demo as a container](../../docs/how-to/deploy-the-demo.md) to build and run it.

## Sources and license

The demo data is for non-commercial research under CC BY-NC 4.0 (`cc-by-nc-4.0`).

- Foregrounds come from [MAGICK](https://ryanndagreat.github.io/MAGICK/) (Burgert et al.,
  CVPR 2024), licensed under CC BY-NC 4.0.
- The background comes from [BG-20k](https://github.com/JizhiziLi/GFM), released under MIT.
  Papers using it must cite Li et al., “Bridging Composite and Real: Towards End-to-end Deep
  Image Matting,” IJCV. Copyright for each image stays with its owner.
- The [Depth Anything V2 Large](https://github.com/DepthAnything/Depth-Anything-V2) weights
  used to prepare one library are licensed under CC BY-NC 4.0.

The application code is [MIT licensed](../../LICENSE).
