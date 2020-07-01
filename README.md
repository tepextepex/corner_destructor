# corner_destructor
A simple script for eliminating black corners from your imagery

**Have you ever encountered that annoying type of georeferenced images, where the black corners consist of ZERO value? Like this:**
<p align="center">
<img alt="Ugly black corners" src="https://drive.google.com/uc?export=view&id=1yM6r7VjRW1YBFwuRsTvD0wlxiXhFEGE3" width="300">
</p>

They overlap each other, and it becomes a real pain when you're trying to merge them or just display together.

- But dude, you can just make all the zero values transparent!

Yep, it's a possible, but not a perfect solution, because zero values present on the useful part of the image.

Making them transparent leads to TONS OF SMALL GAPS on the image.

- maan, you certainly need to create an alpha band!

Cool, but an image with two bands, in generally, uses more disk space.

- Ok, let we test your *corner_destructor*

This simple script turns the values into the image corners into NODATA, leaving all the needed data as they are.

No annoying corners, no gaps.
