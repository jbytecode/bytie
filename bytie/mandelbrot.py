import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

max_iter = 200
divergence_radius = 4
canvas_shape = (600, 600)


def mandel_iter(canvas):

    real_c, cmplx_c = canvas
    real_z, cmplx_z = np.zeros(canvas_shape, dtype="float64"), np.zeros(
        canvas_shape, dtype="float64"
    )

    iter_array = np.zeros(canvas_shape, dtype="uint8")
    done_mask = np.zeros(canvas_shape, dtype="uint8")

    for idx in range(max_iter):

        # (a + bi) ** 2

        # a**2 - b**2
        # 2 * a * b

        real_z, cmplx_z = (
            real_z ** 2 - cmplx_z ** 2 + real_c,
            2 * real_z * cmplx_z + cmplx_c,
        )

        dists = real_z ** 2 + cmplx_z ** 2

        done_mask[dists >= divergence_radius] = 1
        # done_mask = done_mask | (dists >= divergence_radius)

        real_z[done_mask == 1] = 0
        cmplx_z[done_mask == 1] = 0

        iter_array[done_mask != 1] = idx

        if np.sum(done_mask == 0) == 0:
            break

    return iter_array


def mandelbrot(zoom=0.5, center=(0, 0), filename="deneme.png"):
    _extents = 2 / (2 ** zoom)

    x_lim = [center[0] - _extents, center[0] + _extents]
    y_lim = [center[1] - _extents, center[1] + _extents]

    x_range = np.linspace(x_lim[0], x_lim[1], canvas_shape[1], dtype="float64").reshape(
        1, canvas_shape[1]
    )
    canvas_real = np.repeat(x_range, canvas_shape[0], axis=0)
    y_range = np.linspace(y_lim[0], y_lim[1], canvas_shape[0], dtype="float64").reshape(
        canvas_shape[0], 1
    )
    canvas_cmplx = np.repeat(y_range[::-1, :], canvas_shape[1], axis=1)

    res = mandel_iter((canvas_real, canvas_cmplx))

    plt.imshow(res)
    plt.set_cmap("hot")
    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight")


"""
BYTIE REPO : https://github.com/jbytecode/bytie


1 - mandelbrot çizdir : mrgranddy

2 - parametre alıp zoomdur/scale 
    yaparak çizdir

2.5 - opsiyonel: 
      eğer ilginç bölgeleri bulmanın 
      bir yolu varsa onu bul

3 - bunun bi apisini yap

4 - bytie'ye bağla



"""
