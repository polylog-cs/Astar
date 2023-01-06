import copy
import itertools
import random
import math
from utils.util_graph import *
from manim import *
from typing import Set
from utils.solarized import *
from manim.utils.unit import Percent

############### DEFAULT OPTIONS

def default():
    VMobject.set_default(color = GRAY)
    Polygon.set_default(color = RED)
    # SurroundingRectangle.set_default(color = RED)
    # SurroundingRectangle.set_default(fill_color = config.background_color)
    # SurroundingRectangle.set_default(fill_opacity = 1)

############### GENERATING SOUNDS

def random_click_file():
    return f"audio/click/click_{random.randint(0, 3)}.wav"


def random_pop_file():
    return f"audio/pop/pop_{random.randint(0, 6)}.wav"


def random_whoosh_file():
    return f"audio/whoosh/whoosh_{random.randint(0, 3)}.wav"


whoosh_gain = -8


def random_whoops_file():
    return f"audio/whoops/whoops{random.randint(1, 1)}.mp3"


def random_rubik_file():
    return f"audio/cube/r{random.randint(1, 20)}.wav"


# use as: 
# self.add_sound(random_whoosh_file(), time_offset = 0.15, gain = whoosh_gain)


############### GENERATING CLIPARTS

PRAGUE = 0
ROME = 1
N_CITIES = 32
SCALE_EUROPE = 1.25

def clipart_arrow():
    return ImageMobject("img/arrow.png").scale_to_fit_height(0.7)

def clipart_yes_no_maybe(which, height):
    pnts_yes = [
        np.array([174.042, 364.002, 0]),
        np.array([169.653, 359.498, 0]),
        np.array([181.318, 347.66, 0]),
        np.array([200.663, 367.236, 0]),
        np.array([195.928, 371.625, 0]),
        np.array([181.376, 356.553, 0])
    ]
    pnts_no = [
        np.array([397.791, 350.711, 0]),
        np.array([402.185, 346.322, 0]),
        np.array([410.393, 354.779, 0]),
        np.array([417.863, 347.317, 0]),
        np.array([421.913, 351.489, 0]),
        np.array([414.443, 358.95, 0]),
        np.array([421.999, 366.735, 0]),
        np.array([417.606, 371.123, 0]),
        np.array([410.049, 363.339, 0]),
        np.array([401.857, 371.522, 0]),
        np.array([397.807, 367.35, 0]),
        np.array([406.359, 359.167, 0])
    ]
    pnts_maybe = [
        #np.array([300.242, 355.568, 0]),
        np.array([300.329, 356.423, 0]),
        np.array([300.478, 357.373, 0]),
        np.array([300.915, 358.039, 0]),
        np.array([301.621, 358.773, 0]),
        np.array([302.28, 359.361, 0]),
        np.array([302.983, 359.868, 0]),
        np.array([303.927, 360.481, 0]),
        np.array([304.549, 360.903, 0]),
        np.array([305.347, 361.538, 0]),
        np.array([305.847, 362.036, 0]),
        np.array([306.411, 362.764, 0]),
        np.array([306.822, 363.514, 0]),
        np.array([307.069, 364.183, 0]),
        np.array([307.247, 364.906, 0]),
        np.array([307.382, 365.766, 0]),
        np.array([307.454, 366.456, 0]),
        np.array([307.5, 367.296, 0]),
        np.array([307.483, 368.449, 0]),
        np.array([307.368, 369.476, 0]),
        np.array([307.122, 370.533, 0]),
        np.array([306.738, 371.538, 0]),
        np.array([306.243, 372.415, 0]),
        np.array([305.63, 373.196, 0]),
        np.array([305.216, 373.623, 0]),
        np.array([304.639, 374.132, 0]),
        np.array([304.202, 374.464, 0]),
        np.array([303.471, 374.93, 0]),
        np.array([302.656, 375.315, 0]),
        np.array([301.972, 375.546, 0]),
        np.array([301.166, 375.736, 0]),
        np.array([300.224, 375.859, 0]),
        np.array([298.285, 375.953, 0]),
        np.array([296.657, 375.957, 0]),
        np.array([294.859, 375.787, 0]),
        np.array([294.403, 375.672, 0]),
        np.array([293.672, 375.397, 0]),
        np.array([292.749, 374.913, 0]),
        np.array([291.972, 374.442, 0]),
        np.array([290.817, 373.659, 0]),
        np.array([289.949, 372.98, 0]),
        np.array([289.316, 372.386, 0]),
        np.array([288.951, 371.975, 0]),
        np.array([288.621, 371.532, 0]),
        np.array([288.237, 370.902, 0]),
        np.array([287.855, 370.102, 0]),
        np.array([287.6, 369.378, 0]),
        np.array([287.436, 368.697, 0]),
        np.array([287.307, 367.822, 0]),
        np.array([287.235, 366.977, 0]),
        np.array([287.282, 366.009, 0]),
        np.array([292.414, 366.022, 0]),
        np.array([293.403, 366.042, 0]),
        np.array([294.352, 366.039, 0]),
        np.array([294.433, 366.942, 0]),
        np.array([294.533, 367.926, 0]),
        np.array([294.593, 368.426, 0]),
        np.array([294.835, 368.99, 0]),
        np.array([295.18, 369.352, 0]),
        np.array([295.838, 369.706, 0]),
        np.array([296.789, 369.93, 0]),
        np.array([297.278, 369.977, 0]),
        np.array([298.182, 369.937, 0]),
        np.array([298.87, 369.745, 0]),
        np.array([299.466, 369.41, 0]),
        np.array([299.913, 369.01, 0]),
        np.array([300.142, 368.711, 0]),
        np.array([300.326, 368.337, 0]),
        np.array([300.399, 368.005, 0]),
        np.array([300.392, 367.466, 0]),
        np.array([300.315, 366.959, 0]),
        np.array([300.217, 366.476, 0]),
        np.array([300.052, 365.885, 0]),
        np.array([299.736, 365.153, 0]),
        np.array([299.328, 364.545, 0]),
        np.array([298.823, 363.99, 0]),
        np.array([298.173, 363.384, 0]),
        np.array([297.472, 362.763, 0]),
        np.array([296.921, 362.255, 0]),
        np.array([296.5, 361.84, 0]),
        np.array([295.955, 361.235, 0]),
        np.array([295.516, 360.609, 0]),
        np.array([295.169, 359.915, 0]),
        np.array([294.877, 358.949, 0]),
        np.array([294.851, 358.451, 0]),
        np.array([294.803, 357.471, 0]),
        np.array([294.769, 356.475, 0]),
        np.array([294.771, 355.811, 0]),
        np.array([300.261, 355.911, 0]),
    ]

    color = ""
    
    if which == "yes":
        color = GREEN
        clipart = Polygon(
            *pnts_yes,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).move_to(
            ORIGIN
        ).scale_to_fit_height(
            height/2
        )

    if which == "no":
        color = RED
        clipart = Polygon(
            *pnts_no,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).move_to(
            ORIGIN
        ).scale_to_fit_height(
            height/2
        )
    
    if which == "maybe":
        color = ORANGE
        clipart = Polygon(
            *pnts_maybe,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).move_to(
            ORIGIN
        ).scale_to_fit_height(
            height/2.5
        )
        small_circle = Circle(
            radius = height/12.5,
            color = color,
            fill_color = WHITE,
            fill_opacity = 1,
        ).next_to(clipart, DOWN, buff = height/20)
        Group(clipart, small_circle).move_to(ORIGIN)
    

    circle = Circle(
        radius = height/2,
        color = color,
        fill_color = color,
        fill_opacity = 1,
    ).move_to(ORIGIN)

    if which != "maybe":
        return Group(circle, clipart)
    else:
        return Group(circle, clipart, small_circle)

def clipart_map_europe(scale = 1, undirected = True, rate = 0.5, setup_potentials = True, weird_bug = False):
    pnts_europe = [
        np.array([404.246, 552.657, 0]),
        np.array([404.373, 545.566, 0]),
        np.array([399.055, 540.882, 0]),
        np.array([392.471, 546.2, 0]),
        np.array([387.659, 553.923, 0]),
        np.array([377.15, 552.277, 0]),
        np.array([373.858, 540.122, 0]),
        np.array([370.946, 536.956, 0]),
        np.array([372.592, 515.938, 0]),
        np.array([372.845, 505.429, 0]),
        np.array([361.196, 505.935, 0]),
        np.array([358.537, 495.173, 0]),
        np.array([351.314, 495.315, 0]),
        np.array([347.156, 502.995, 0]),
        np.array([307.369, 488.558, 0]),
        np.array([297.998, 494.911, 0]),
        np.array([276.094, 491.999, 0]),
        np.array([264.951, 503.901, 0]),
        np.array([261.279, 517.449, 0]),
        np.array([272.422, 533.15, 0]),
        np.array([267.864, 553.535, 0]),
        np.array([243.426, 539.354, 0]),
        np.array([243.047, 517.702, 0]),
        np.array([250.644, 488.074, 0]),
        np.array([235.703, 481.616, 0]),
        np.array([211.772, 477.438, 0]),
        np.array([209.113, 460.598, 0]),
        np.array([200.25, 450.848, 0]),
        np.array([183.536, 441.732, 0]),
        np.array([178.472, 429.83, 0]),
        np.array([177.459, 426.158, 0]),
        np.array([161.632, 415.396, 0]),
        np.array([142.639, 406.153, 0]),
        np.array([116.809, 406.406, 0]),
        np.array([119.468, 394.63, 0]),
        np.array([139.853, 389.059, 0]),
        np.array([153.022, 369.054, 0]),
        np.array([152.277, 334.573, 0]),
        np.array([135.342, 330.408, 0]),
        np.array([101.749, 334.851, 0]),
        np.array([78.1504, 334.295, 0]),
        np.array([73.4307, 321.524, 0]),
        np.array([78.428, 300.425, 0]),
        np.array([70.6545, 272.107, 0]),
        np.array([77.5952, 262.945, 0]),
        np.array([75.0965, 247.12, 0]),
        np.array([102.859, 247.953, 0]),
        np.array([111.466, 236.293, 0]),
        np.array([158.94, 252.95, 0]),
        np.array([167.546, 272.94, 0]),
        np.array([164.77, 284.322, 0]),
        np.array([179.295, 303.597, 0]),
        np.array([197.53, 309.031, 0]),
        np.array([197.073, 326.645, 0]),
        np.array([208.341, 330.95, 0]),
        np.array([223.029, 326.138, 0]),
        np.array([232.399, 330.064, 0]),
        np.array([247.34, 339.813, 0]),
        np.array([252.024, 343.358, 0]),
        np.array([256.456, 343.738, 0]),
        np.array([265.066, 338.927, 0]),
        np.array([269.751, 324.619, 0]),
        np.array([282.159, 313.857, 0]),
        np.array([288.743, 305.753, 0]),
        np.array([302.291, 301.321, 0]),
        np.array([303.684, 295.624, 0]),
        np.array([318.878, 284.861, 0]),
        np.array([323.31, 272.073, 0]),
        np.array([319.765, 260.931, 0]),
        np.array([326.475, 260.044, 0]),
        np.array([334.199, 276.251, 0]),
        np.array([329.894, 284.735, 0]),
        np.array([332.806, 291.319, 0]),
        np.array([344.582, 287.647, 0]),
        np.array([344.582, 294.611, 0]),
        np.array([322.424, 306.766, 0]),
        np.array([304.191, 320.694, 0]),
        np.array([297.227, 338.674, 0]),
        np.array([284.692, 346.524, 0]),
        np.array([286.971, 358.552, 0]),
        np.array([297.86, 362.351, 0]),
        np.array([304.697, 351.209, 0]),
        np.array([314.447, 347.663, 0]),
        np.array([325.589, 333.229, 0]),
        np.array([342.429, 322.72, 0]),
        np.array([355.724, 310.311, 0]),
        np.array([354.964, 295.497, 0]),
        np.array([363.954, 278.277, 0]),
        np.array([371.678, 271.82, 0]),
        np.array([373.704, 265.362, 0]),
        np.array([390.924, 263.21, 0]),
        np.array([369.905, 261.944, 0]),
        np.array([379.275, 247.383, 0]),
        np.array([390.417, 243.078, 0]),
        np.array([391.81, 255.106, 0]),
        np.array([394.216, 259.411, 0]),
        np.array([404.725, 259.158, 0]),
        np.array([404.598, 268.907, 0]),
        np.array([396.241, 274.352, 0]),
        np.array([389.024, 289.926, 0]),
        np.array([399.407, 290.179, 0]),
        np.array([402.319, 296.89, 0]),
        np.array([413.588, 299.549, 0]),
        np.array([426.503, 293.345, 0]),
        np.array([436.759, 300.055, 0]),
        np.array([449.167, 297.65, 0]),
        np.array([451.193, 303.474, 0]),
        np.array([443.723, 306.893, 0]),
        np.array([436.632, 318.162, 0]),
        np.array([440.051, 330.697, 0]),
        np.array([447.648, 334.242, 0]),
        np.array([448.788, 345.638, 0]),
        np.array([455.118, 351.968, 0]),
        np.array([458.537, 363.87, 0]),
        np.array([469.3, 374.253, 0]),
        np.array([479.302, 375.519, 0]),
        np.array([479.935, 368.808, 0]),
        np.array([492.217, 367.922, 0]),
        np.array([493.539, 364.586, 0]),
        np.array([481.011, 358.284, 0]),
        np.array([493.614, 354.683, 0]),
        np.array([492.039, 347.706, 0]),
        np.array([499.466, 343.355, 0]),
        np.array([509.894, 350.857, 0]),
        np.array([523.997, 357.759, 0]),
        np.array([511.169, 361.36, 0]),
        np.array([503.517, 369.012, 0]),
        np.array([548.754, 384.991, 0]),
    ]

    pnts_cities = [
        np.array([1, 307.112, 427.572]) + np.array([0, 0, 0]),
        np.array([2, 287.537, 312.262]),
        np.array([1, 304.973, 297.951]),
        np.array([1, 261.301, 524.645]),
        np.array([1, 335.569, 296.47]),
        np.array([1, 288.359, 338.581]),
        np.array([1, 270.594, 359.471]),
        np.array([1, 298.229, 390.725]) + np.array([0, 3, -7]),
        np.array([2, 278.983, 398.292]) + np.array([0, -10, 0]),
        np.array([1, 250.361, 427.572]),

        np.array([2, 188.183, 408.82]),
        np.array([2, 297.571, 464.583]) + np.array([0, 0, 7]),
        np.array([2, 371.429, 460.8]),
        np.array([1, 401.366, 423.459]),
        np.array([2, 464.697, 433.0]),
        np.array([2, 326.193, 399.279]) + np.array([0, 10, -5]),
        np.array([1, 323.067, 365.064]),
        np.array([1, 346.261, 337.265]),
        np.array([2, 422.257, 345.818]),
        np.array([1, 447.754, 381.843]),
        
        np.array([1, 393.471, 321.802]),
        np.array([2, 398.077, 261.433]),
        np.array([1, 219.107, 330.52]),
        np.array([1, 185.386, 304.859]),
        np.array([2, 129.623, 291.535]),
        np.array([1, 161.041, 350.589]),
        np.array([2, 207.922, 438.264]),
        np.array([1, 213.021, 364.242]),
        np.array([1, 413.704, 500.936]),
        np.array([1, 347.742, 497.153]),

        np.array([1, 263.685, 481.361]),
        np.array([1, 397.944, 379.455]),
        
    ]
    
    pnts_paths = [
    [
        np.array([368.422, 460.77, 0]),
        np.array([354.492, 459.97, 0]),
        np.array([339.122, 450.684, 0]),
        np.array([320.39, 441.558, 0]),
        np.array([308.382, 428.589, 0]),
    ],
    # [
    #     np.array([322.82, 282.496, 0]),
    #     np.array([321.399, 286.139, 0]),
    #     np.array([318.339, 288.391, 0]),
    #     np.array([315.336, 292.837, 0]),
    #     np.array([311.467, 296.706, 0]),
    #     np.array([306.268, 297.663, 0]),
    # ],
    [
        np.array([304.486, 299.184, 0]),
        np.array([303.69, 305.727, 0]),
        np.array([295.581, 307.985, 0]),
        np.array([292.159, 311.714, 0]),
        np.array([290.325, 311.725, 0]),
    ],
    [
        np.array([288.508, 336.479, 0]),
        np.array([289.658, 333.929, 0]),
        np.array([287.391, 328.684, 0]),
        np.array([288.457, 323.795, 0]),
        np.array([285.746, 320.239, 0]),
        np.array([286.62, 314.949, 0]),
    ],
    [
        np.array([324.291, 363.662, 0]),
        np.array([333.061, 357.936, 0]),
        np.array([336.352, 344.597, 0]),
        np.array([345.175, 338.373, 0]),
    ],
    [
        np.array([347.409, 336.22, 0]),
        np.array([361.645, 326.58, 0]),
        np.array([376.774, 327.157, 0]),
        np.array([383.415, 321.845, 0]),
        np.array([391.39, 321.788, 0]),
    ],
    [
        np.array([393.653, 319.73, 0]),
        np.array([393.517, 296.357, 0]),
        np.array([385.623, 293.628, 0]),
        np.array([384.356, 273.064, 0]),
        np.array([396.59, 263.802, 0]),
    ],
    [
        np.array([394.921, 323.295, 0]),
        np.array([403.945, 338.656, 0]),
        np.array([420.4, 345.13, 0]),
    ],
    [
        np.array([423.901, 346.924, 0]),
        np.array([438.057, 360.293, 0]),
        np.array([437.862, 378.908, 0]),
        np.array([446.25, 382.036, 0]),
    ],
    [
        np.array([448.589, 383.108, 0]),
        np.array([457.842, 393.625, 0]),
        np.array([454.626, 417.503, 0]),
        np.array([461.986, 430.552, 0]),
    ],
    [
        np.array([461.046, 432.896, 0]),
        np.array([439.714, 421.986, 0]),
        np.array([421.391, 428.126, 0]),
        np.array([408.234, 426.275, 0]),
        np.array([403.228, 424.193, 0]),
    ],
    [
        np.array([399.459, 422.853, 0]),
        np.array([385.72, 426.859, 0]),
        np.array([381.627, 444.403, 0]),
        np.array([371.101, 450.835, 0]),
        np.array([371.048, 457.947, 0]),
    ],
    [
        np.array([322.873, 366.915, 0]),
        np.array([324.611, 375.692, 0]),
        np.array([321.2, 382.806, 0]),
        np.array([324.901, 396.933, 0]),
    ],
    [
        np.array([328.854, 398.979, 0]),
        np.array([334.845, 397.913, 0]),
        np.array([340.985, 406.587, 0]),
        np.array([357.748, 413.117, 0]),
        np.array([360.867, 426.372, 0]),
        np.array([358.723, 446.254, 0]),
        np.array([370.019, 458.291, 0]),
    ],
    [
        np.array([326.868, 401.87, 0]),
        np.array([332.018, 411.46, 0]),
        np.array([323.539, 420.134, 0]),
        np.array([313.793, 424.423, 0]),
        np.array([308.175, 426.78, 0]),
    ],
    [
        np.array([306.567, 426.363, 0]),
        np.array([292.644, 416.723, 0]),
        np.array([285.431, 406.587, 0]),
        np.array([280.302, 399.761, 0]),
    ],
    [
        np.array([277.95, 396.61, 0]),
        np.array([275.49, 388.167, 0]),
        np.array([276.27, 373.06, 0]),
        np.array([271.47, 360.367, 0]),
    ],

    [
        np.array([219.105, 332.508, 0]),
        np.array([211.528, 345.265, 0]),
        np.array([212.813, 362.272, 0]),
    ],
    [
        np.array([212.475, 366.146, 0]),
        np.array([213.478, 378.649, 0]),
        np.array([201.7, 379.175, 0]),
        np.array([198.999, 397.555, 0]),
        np.array([190.106, 406.686, 0]),
    ],
    [
        np.array([161.975, 352.067, 0]),
        np.array([172.067, 358.844, 0]),
        np.array([168.091, 371.222, 0]),
        np.array([175.593, 381.95, 0]),
        np.array([174.243, 394.404, 0]),
        np.array([186.696, 401.381, 0]),
        np.array([187.248, 406.103, 0]),
    ],
    [
        np.array([209.231, 436.768, 0]),
        np.array([219.18, 431.314, 0]),
        np.array([228.783, 435.44, 0]),
        np.array([238.01, 431.089, 0]),
        np.array([249.245, 427.899, 0]),
    ],
    
    [
        np.array([214.707, 365.281, 0]),
        np.array([227.305, 373.312, 0]),
        np.array([233.835, 381.888, 0]),
        np.array([247.644, 385.045, 0]),
        np.array([260.091, 396.451, 0]),
        np.array([277.022, 398.512, 0]),
    ],
    
    [
        np.array([278.041, 400.027, 0]),
        np.array([265.023, 406.839, 0]),
        np.array([262.197, 422.043, 0]),
        np.array([251.123, 426.693, 0]),
    ],
    [
        np.array([306.707, 428.835, 0]),
        np.array([298.55, 442.997, 0]),
        np.array([302.741, 456.252, 0]),
        np.array([298.984, 462.437, 0]),
    ],
    [
        np.array([295.607, 466.24, 0]),
        np.array([286.757, 473.6, 0]),
        np.array([273.405, 471.846, 0]),
        np.array([264.917, 480.418, 0]),
    ],
    [
        np.array([370.017, 463.307, 0]),
        np.array([360.244, 478.376, 0]),
        np.array([347.671, 480.13, 0]),
        np.array([348.094, 495.203, 0]),
    ],
    [
        np.array([345.914, 496.389, 0]),
        np.array([330.713, 493.385, 0]),
        np.array([316.678, 485.101, 0]),
        np.array([304.3, 481.007, 0]),
        np.array([304.983, 473.6, 0]),
        np.array([299.368, 466.419, 0]),
    ],
    [
        np.array([373.946, 462.193, 0]),
        np.array([385.756, 470.622, 0]),
        np.array([388.795, 485.817, 0]),
        np.array([400.824, 496.832, 0]),
        np.array([412.26, 500.147, 0]),
    ],
    [
        np.array([307.312, 426.261, 0]),
        np.array([308.978, 415.467, 0]),
        np.array([306.104, 407.598, 0]),
        np.array([305.522, 399.694, 0]),
        np.array([298.85, 396.239, 0]),
        np.array([298.354, 391.602, 0]),
    ],
    [
        np.array([297.647, 390.058, 0]),
        np.array([288.089, 380.56, 0]),
        np.array([285.389, 369.007, 0]),
        np.array([271.846, 359.52, 0]),
    ],
    [
        np.array([132.871, 292.614, 0]),
        np.array([148.738, 296.479, 0]),
        np.array([157.169, 309.125, 0]),
        np.array([171.895, 310.454, 0]),
        np.array([182.349, 308.614, 0]),
    ],
    [
        np.array([189.705, 411.256, 0]),
        np.array([190.976, 418.322, 0]),
        np.array([202.622, 425.345, 0]),
        np.array([207.051, 436.477, 0]),
    ],
    [
        np.array([263.835, 482.906, 0]),
        np.array([264.375, 496.097, 0]),
        np.array([255.616, 507.799, 0]),
        np.array([255.718, 518.747, 0]),
        np.array([260.119, 523.271, 0]),
    ],
    [
        np.array([420.976, 347.329, 0]),
        np.array([414.252, 354.212, 0]),
        np.array([415.677, 366.215, 0]),
        np.array([401.499, 371.392, 0]),
        np.array([398.28, 378.751, 0]),
    ],
    [
        np.array([397.798, 380.221, 0]),
        np.array([396.547, 391.197, 0]),
        np.array([389.045, 399.599, 0]),
        np.array([390.32, 409.802, 0]),
        np.array([400.096, 421.914, 0]),
    ],
    [
        np.array([397.221, 379.165, 0]),
        np.array([375.691, 373.042, 0]),
        np.array([369.09, 365.165, 0]),
        np.array([355.736, 361.039, 0]),
        np.array([347.634, 349.486, 0]),
        np.array([346.536, 338.792, 0]),
    ],
    [
        np.array([221.086, 330.708, 0]),
        np.array([231.385, 332.241, 0]),
        np.array([248.883, 344.888, 0]),
        np.array([255.35, 357.881, 0]),
        np.array([269.348, 359.598, 0]),
    ],
    [
        np.array([251.024, 428.528, 0]),
        np.array([257.563, 438.322, 0]),
        np.array([249.82, 452.114, 0]),
        np.array([250.546, 470.504, 0]),
        np.array([262.621, 480.232, 0]),
    ],
    # [
    #     np.array([217.509, 331.702, 0]),
    #     np.array([211.14, 336.112, 0]),
    #     np.array([202.078, 336.653, 0]),
    # ],
    [
        np.array([200.395, 336.367, 0]),
        np.array([191.717, 327.773, 0]),
        np.array([191.618, 315.119, 0]),
        np.array([186.462, 309.642, 0]),
    ],
    [
        np.array([200.115, 337.901, 0]),
        np.array([194.954, 343.959, 0]),
        np.array([182.201, 342.39, 0]),
        np.array([168.468, 343.469, 0]),
        np.array([162.243, 349.32, 0]),
    ],
    [
        np.array([306.274, 298.209, 0]),
        np.array([312.492, 299.59, 0]),
        np.array([319.264, 295.688, 0]),
        np.array([329.593, 293.392, 0]),
        np.array([334.486, 295.56, 0]),
    ],
    [
        np.array([286.316, 339.094, 0]),
        np.array([277.793, 341.009, 0]),
        np.array([269.802, 348.784, 0]),
        np.array([270.566, 358.219, 0]),
    ],
    [
        np.array([287.051, 340.232, 0]),
        np.array([281.14, 348.028, 0]),
        np.array([283.515, 359.041, 0]),
        np.array([297.66, 367.14, 0]),
        np.array([312.237, 360.337, 0]),
        np.array([321.349, 364.35, 0]),
    ],

    ]

    def normalize(pnt):
        return pnt/50.0 * scale

    #### boundary
    background = Rectangle(color = BASE02, fill_color = BASE02, fill_opacity = 1, height = 9 + (100 if weird_bug else 0), width =15 + (100 if weird_bug else 0), z_index = -100)
    europe_boundary = Polygon(
        *[normalize(pnt) for pnt in pnts_europe],
        color = BASE02,
        fill_color = config.background_color,
        fill_opacity = 1,
        z_index = -90,
    )
    europe_boundary.generate_target()
    europe_boundary.target.move_to(
        ORIGIN
    )
    shft = europe_boundary.target.get_center() - europe_boundary.get_center()
    europe_boundary.shift(shft)

    #### cities
    G = CustomGraph([], [])
    
    # for v in G.vertices.keys():
    #     G.vertices[v] = Cylinder(radius = G.vertices[v].radius, color = G.vertices[v].color, height = 0.01).move_to(G.vertices[v].get_center())

    cities = []
    for i, pnts in enumerate(pnts_cities):
        G.add_vertices(i, positions = {i: normalize(pnts[1])*RIGHT + normalize(pnts[2])*UP})#, vertex_type = Cylinder)
        G.vertices[i].scale(1).shift(shft).set_color(GRAY)

    MADRID = 25
    KYEV = 15
    E_MADRID = -3.7
    N_MADRID = 40.4 
    E_KYEV = 30.6
    N_KYEV = 50.45
    alphaE = (E_KYEV - E_MADRID) / (G.vertices[KYEV].get_center()[0] - G.vertices[MADRID].get_center()[0])
    betaE = E_MADRID - alphaE * G.vertices[MADRID].get_center()[0]
    alphaN = (N_KYEV - N_MADRID) / (G.vertices[KYEV].get_center()[1] - G.vertices[MADRID].get_center()[1])
    betaN = N_MADRID - alphaN * G.vertices[MADRID].get_center()[1]
    

    DOWNISH = 0.3*DOWN
    pos = [
        RIGHT, RIGHT, LEFT, RIGHT, RIGHT,
        RIGHT, RIGHT + DOWNISH, RIGHT, LEFT, LEFT + DOWNISH,
        LEFT, RIGHT, RIGHT, RIGHT + DOWNISH, RIGHT,
        RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT,
        RIGHT, RIGHT + DOWNISH, RIGHT, RIGHT + DOWNISH, LEFT,
        LEFT, LEFT, RIGHT, UP*0.4, LEFT, 
        RIGHT, RIGHT
    ]
    for i in range(len(pnts_cities)):
        E_city = alphaE * G.vertices[i].get_center()[0] + betaE
        N_city = alphaN * G.vertices[i].get_center()[1] + betaN
        name = "[{:d}E, {:d}N]".format(round(E_city), round(N_city))
        if E_city < 0:
            name = "[{:d}W, {:d}N]".format(-round(E_city), round(N_city))
            
        G.create_name(i, name, 0.66 * pos[i])

    #### paths

    for path in pnts_paths:
        for i in range(len(path)):
            path[i] = np.add(normalize(path[i]), shft)
        u = 0
        for i in range(len(pnts_cities)):
            if np.linalg.norm(G.vertices[i].get_center() - path[0]) < np.linalg.norm(G.vertices[u].get_center() - path[0]):
                u = i
        v = 0
        for i in range(len(pnts_cities)):
            if np.linalg.norm(G.vertices[i].get_center() - path[-1]) < np.linalg.norm(G.vertices[v].get_center() - path[-1]):
                v = i

        if undirected:
            alpha = 1.2
            def add_edge(u, v):
                G.add_edges((u, v))
                G.edges[(u, v)].set_color(GRAY)
                G.create_edge_length((u,v), alpha * np.linalg.norm(G.vertices[u].get_center()-G.vertices[v].get_center()))
                G.add_edges((v, u))
                G.edges[(v, u)].set_color(GRAY)
                G.create_edge_length((v,u), alpha * np.linalg.norm(G.vertices[u].get_center()-G.vertices[v].get_center()))
                
            for i in range(1, len(path)-1, 1):
                new_ind = len(G.vertices.items())
                G.add_vertices(new_ind, positions = {new_ind: path[i]})
                G.vertices[new_ind].scale(0.005).set_color(GRAY)
                add_edge(u, new_ind)
                u = new_ind

            add_edge(u, v)
        else:
            alpha = 1.8
            weight = alpha * np.linalg.norm(G.vertices[u].get_center()-G.vertices[v].get_center())
            if u == 7 and v == 6:
                weight = 2.0
            
            offset = np.array([-(G.vertices[v].get_center()-G.vertices[u].get_center())[1], (G.vertices[v].get_center()-G.vertices[u].get_center())[0], 0])
            offset /= np.linalg.norm(offset)
            offset *= -0.04

            G.add_directed_edge(
                u, 
                v, 
                offset = offset, 
                weight = weight,
                offset_weight = 2*offset,
            )
            G.add_directed_edge(
                v, 
                u, 
                offset = -offset, 
                weight = weight,
                offset_weight = -2*offset,
            )

    if setup_potentials:
        G.setup_potentials(rate = rate)
    return (background, europe_boundary, G)


list_properties_str = [
    [
        r"1. potential(Prague) as high as possible ",
        r"1. potential(start) as high as possible ",
        r"1. heuristic(start) as high as possible",
    ],
    [
        r"{{2. For every edge $(u,v):$ \\}}{{potential$(u)$ $\le $ potential$(v)$ + length$(u,v)$ }}",
        r"{{2. For every edge $(u,v):$ \\}}{{potential$(u)$ $\le $ potential$(v)$ + length$(u,v)$ }}",
        r"{{2. For every edge $(u,v):$ \\}}{{heuristic$(u)$ $\le $ heuristic$(v)$ + length$(u,v)$ }}",
    ],
    [
        r"{{Implies that for every node $u$: \\}}{{potential$(u)$ $\le $ distance($u$, Rome)}}",
        r"{{Implies that for every node $u$: \\}}{{potential$(u)$ $\le $ distance($u$, end)}}",
        r"{{Implies that for every node $u$: \\}}{{heuristic$(u)$ $\le $ distance($u$, end)}}",
    ],
    [
        r"3. We can compute it fast.  ",
        r"3. We can compute it fast.  ",
        r"3. We can compute it fast.  ",
    ],
]

def create_potential_list(options, heuristic = False):
    list_header_scale = 1.1
    list_properties_scale = 1
    list_header = Tex("Good potential satisfies: ", z_index = 100, font_size = 35).scale(list_header_scale)
    if heuristic == True:
        list_header = Tex("Good heuristic satisfies: ", z_index = 100, font_size = 35).scale(list_header_scale)
        
    list_properties = []
    for i in range(4):
        txt = Tex(list_properties_str[i][options[i]], font_size = 30, z_index = 100).scale(list_properties_scale)
        list_properties.append(txt)


    Group(*list_properties).arrange_in_grid(cols = 1, col_alignments="l").next_to(
        list_header, DOWN
    ).align_to(list_header, LEFT)

    list_properties[1][0].align_to(list_properties[0], LEFT)
    list_properties[2].scale(0.8)
    list_properties[2][0].align_to(list_properties[0], LEFT)
    list_properties[2][1].move_to(np.array([list_properties[1][1].get_center()[0], list_properties[2][1].get_center()[1], 0]))

    border = SurroundingRectangle(
        Group(list_header, *list_properties), 
        #corner_radius = 0.3, 
        fill_opacity = 1, 
        fill_color = config.background_color, 
        color = RED)

    return Group(border, list_header, *list_properties).set_z_index(100).move_to(ORIGIN)

def create_strategy(old=True, scale = 1):

    scale_small = 0.6
    if old:
        strategy = Group(*[
            Tex("A* strategy: ").scale(scale),
            Tex("1. Change the weights!").scale(scale_small * scale),
            Tex("2. Run Dijkstra on the new graph. ").scale(scale_small * scale)
        ]).arrange_in_grid(cols = 1, cell_alignment = LEFT)
    else:
        scale_new = 0.9
        strategy = Group(*[
            Tex("A* algorithm: ").scale(scale * scale_new),
            Tex("1. Compute clever potentials. ").scale(scale_small * scale * scale_new),
            Tex("2. Apply potential reweighting. ").scale(scale_small * scale * scale_new),
            Tex("3. Run Dijkstra on the new graph. ").scale(scale_small * scale * scale_new)
        ]).arrange_in_grid(cols = 1, cell_alignment = LEFT)

    scroll = ImageMobject("img/scroll_transparent.png").scale_to_fit_height(3.5).scale(scale)
    strategy.move_to(scroll.get_center())

    return Group(scroll, strategy)



def basicDijkstraRun(scene, G, variant = None):
    anims, lines, path_nodes, path_edges, _, red_nodes = G.run_dijkstra(PRAGUE, ROME, 3)
    for v in G.vertices.values():
        v.save_state()

    scene.play(Flash(G.vertices[PRAGUE], color = RED))
    scene.play(
        anims
    )
    scene.play(Flash(G.vertices[ROME], color = RED))
    scene.wait()

    scene.play(
        *[FadeOut(line) for (edge, line) in lines.items() if edge not in path_edges],
        *[G.vertices[node].animate.restore() for node in G.vertices.keys() if node not in path_nodes],
    )
    scene.wait()        
    scene.play(
        *[FadeOut(line) for (edge, line) in lines.items() if edge in path_edges],
        *[G.vertices[node].animate.restore() for node in red_nodes],
    )
    scene.wait()

def changeWeights(scene, G, new_weights, color = RED):
    scene.play(
        *[G.edges[e].animate.set_color(color) for e in new_weights.keys()],
        *[G.edge_weights_objs[e].animate.set_color(color) for e in new_weights.keys()],
        run_time = 0.3
    )
    scene.play(
        *[G.edge_weights_vals[(u,v)].animate.set_value(val) for ((u,v), val) in new_weights.items()]
    )
    scene.wait()
    scene.play(
        *[G.edges[e].animate.set_color(GRAY) for e in new_weights.keys()],
        *[G.edge_weights_objs[e].animate.set_color(GRAY) for e in new_weights.keys()],
        run_time = 0.3
    )
    
    scene.wait()

# TODO update edge colors
def simple_reweighting(scene, G, edges_plus, edges_minus, change, weight, diff):

    #TODO fix at je to smooth
    scene.play(
        *[G.edge_weights_objs[e].animate.increment_value(change).set_color(color_from_potential(weight, diff)) for e in edges_plus],
        *[G.edge_weights_objs[e].animate.increment_value(-change).set_color(color_from_potential(weight, -diff)) for e in edges_minus],
        *[G.edges[e].animate.set_color(color_from_potential(weight, diff)) for e in edges_plus],
        *[G.edges[e].animate.set_color(color_from_potential(weight, -diff)) for e in edges_minus],    
    )
    scene.wait()

def go_along_path(scene, G, path):
    
    cleaning_anims = []
    for i in range(len(path)):
        line = Line(
            start = G.vertices[path[i][0]].get_center(), 
            end = G.vertices[path[i][1]].get_center(),
            color = RED,
        )
        scene.play(
            Create(line)
        )
        cleaning_anims.append(FadeOut(line))

    scene.play(AnimationGroup(*cleaning_anims))
    scene.wait()

def rome_tex_name(G, scale = 1):
    return Tex(r"Rome", color = RED).scale(scale).move_to(G.vertices[ROME].get_center() + 0.8*LEFT).set_z_index(100000)

def prague_tex_name(G, scale = 1):
    tex = Tex(r"Prague", color = RED).scale(scale).move_to(G.vertices[PRAGUE].get_center() + 0.5*LEFT + 0.45 *UP)
    back = SurroundingRectangle(tex, color = config.background_color, fill_opacity = 1, fill_color = config.background_color).shift(10000*DOWN)
    return Group(back, tex).set_z_index(100000)

def tex_dijkstra_headline():
    tex = Tex("{{Dijkstra's}}{{ algorithm}}", color = GRAY).scale(1.5).to_corner(LEFT + UP)
    back = SurroundingRectangle(tex, color = BACKGROUND_COLOR_DARK, fill_opacity = 1, fill_color = BACKGROUND_COLOR_DARK)
    return Group(back, tex).set_z_index(100000)

def tex_astar_headline():
    tex = Tex("{{A*}}{{ algorithm}}", color = GRAY).scale(1.5).to_corner(LEFT + UP)
    back = SurroundingRectangle(tex, color = BACKGROUND_COLOR_DARK, fill_opacity = 1, fill_color = BACKGROUND_COLOR_DARK)
    return Group(back, tex).set_z_index(100000)
