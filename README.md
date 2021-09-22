# PS Image Alignment Tool

#### requirement
- pygame
- opencv



#### how to use
- run: `python align.py`
- switch image
  - press `1`: show img1 only
  - press `2`: show img2 only
  - press `3`: show both img1 and img2
- shift image
  - press `W/A/S/D`: move img2 by 1 pixel
  - press `Ctrl` + `W/A/S/D`: move img2 by 50 pixel (you can reset this by changing variable `vel`)
- set reference points
  - left-click on empty space: set a reference point which won't move with the image
  - left-click on a reference point: cancel that point 
- affine image
  - right-click on empty space: set a control point(up to 3 in total)
  - right-click on a control point: select that point
  - when a control point is selected, you can press (`Ctrl`+) `W/A/S/D` to move that point, which will apply an affine transform to img2
- rotate image
  - middle-click on empty space: set a rotation center
  - middle-click on a rotation center: cancel that point
  - press `[/]`: rotate img2 around rotation center by 0.2 degree
  - press `Ctrl` + `[/]`: rotate img2 around rotation center by 1 degree

#### global setting
- `path1`, `path2`: image path
- `temperature1`, `temperature2`: image color temperature
- `x0`,`y0`: the position of the top-left corner of both image

#### warning
- Don't rotate and affine the same image! Some bugs need to be fixed. 
