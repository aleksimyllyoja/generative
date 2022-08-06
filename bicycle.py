from helpers import *
from random import *

W = 300
H = 218

def lpdist(l1, l2, p):
    p1=np.array(l1)
    p2=np.array(l2)
    p3=np.array(p)
    return np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)

paths = []

def wheel(x, y, r, thickness=3):
    wpaths = []
    for i in range(thickness):
        wpaths.extend(circle(x, y, r-i*0.3))
    return wpaths

def bicycle(bike_width, bike_height):

    bpaths = []

    r1 = uniform(bike_width/10, bike_width/5)
    r2 = r1 #uniform(bike_width/8, bike_width/5)

    c1_center = [r1, bike_height-r1]
    c2_center = [
        2*r1+r2+uniform(r2/2, bike_width-2*r1-2*r2),
        bike_height-r2
    ]

    wheel_thickness = randint(1, 6)
    back_wheel = wheel(c1_center[0], c1_center[1], r1, wheel_thickness)
    front_wheel = wheel(c2_center[0], c2_center[1], r2, wheel_thickness)

    bpaths.append(back_wheel)
    bpaths.append(front_wheel)

    control_angle = uniform(pi/8, -pi/8)
    tangent_point = [
        c1_center[0]+cos(control_angle)*r1,
        c1_center[1]+sin(control_angle)*r1
    ]

    seat_tube_l1 = uniform(0, bike_width/40)
    lower_seat_tube = [
        tangent_point[0]+cos(control_angle+pi/2)*seat_tube_l1,
        tangent_point[1]+sin(control_angle+pi/2)*seat_tube_l1
    ]

    seat_tube_l2 = uniform(bike_width/6, bike_width/3)
    upper_seat_tube = [
        lower_seat_tube[0]+cos(control_angle-pi/2)*seat_tube_l2,
        lower_seat_tube[1]+sin(control_angle-pi/2)*seat_tube_l2
    ]

    seat_tube = move(
        [upper_seat_tube, lower_seat_tube],
        uniform(bike_width/20, bike_width/10), 0
    )

    seat_post_angle = atan2(seat_tube[1][1]-seat_tube[0][1], seat_tube[1][0]-seat_tube[0][0])

    seat_post_length = uniform(bike_height/60, bike_height/10)
    seat_post_top = [
        seat_tube[0][0]-cos(seat_post_angle)*seat_post_length,
        seat_tube[0][1]-sin(seat_post_angle)*seat_post_length
    ]
    seat_post = [seat_post_top, seat_tube[0]]

    seat_height = uniform(bike_height/50, bike_height/40)
    seat_width = uniform(bike_width/20, bike_width/10)
    seat = ellipse(seat_post_top[0], seat_post_top[1], seat_width, seat_height)

    #bpaths.append(seat)
    bpaths.append(seat_post)
    bpaths.append(seat_tube)

    control_angle2 = uniform(-pi/2, -2*pi/3)
    head_tube_radius = uniform(r2+bike_height/15, r2+bike_height/5)

    head_tube = [
        c2_center[0]+cos(control_angle2)*head_tube_radius,
        c2_center[1]+sin(control_angle2)*head_tube_radius,
    ]

    top_tube = [seat_tube[0], head_tube]
    down_tube = [seat_tube[1], head_tube]

    seat_stay = [seat_tube[0], c1_center]
    chain_stay = [seat_tube[1], c1_center]

    control_angle3 = uniform(-2*pi/3, -pi)
    bc_length = uniform(0, bike_width/7)

    fork_control_point = [
        c2_center[0]+cos(control_angle3)*bc_length,
        c2_center[1]+sin(control_angle3)*bc_length
    ]

    bike_fork = bezier([
        head_tube,
        fork_control_point,
        c2_center
    ])

    fork_ext_length = uniform(bike_height/60, bike_height/10)
    fork_angle = atan2(bike_fork[-2][1]-bike_fork[-1][1], bike_fork[-2][0]-bike_fork[-1][0])
    fork_ext_top = [
        head_tube[0]-cos(fork_angle)*fork_ext_length,
        head_tube[1]-sin(fork_angle)*fork_ext_length
    ]
    fork_ext = [fork_ext_top, head_tube]


    handlebar_angle = uniform(0, -pi/3)

    handlebar_length = uniform(bike_height/60, bike_height/10)
    handlebar = bezier([
        [
            fork_ext_top[0] + cos(handlebar_angle)*handlebar_length,
            fork_ext_top[1] + sin(handlebar_angle)*handlebar_length
        ],
        [
            fork_ext_top[0] + cos(handlebar_angle+pi/4)*handlebar_length/2,
            fork_ext_top[1] + sin(handlebar_angle+pi/4)*handlebar_length/2
        ],
        fork_ext_top,
        [
            fork_ext_top[0] - cos(handlebar_angle-pi/2)*handlebar_length/2,
            fork_ext_top[1] - sin(handlebar_angle-pi/2)*handlebar_length/2
        ],
        [
            fork_ext_top[0] - cos(handlebar_angle)*handlebar_length,
            fork_ext_top[1] - sin(handlebar_angle)*handlebar_length
        ],
    ])

    #bpaths.append(handlebar)

    bpaths.append(fork_ext)
    bpaths.append(bike_fork)

    bpaths.append(top_tube)
    bpaths.append(down_tube)

    bpaths.append(seat_stay)
    bpaths.append(chain_stay)

    return bpaths

def many_bikes():
    m = 3
    xc = 4
    yc = 3
    for x in range(xc):
        for y in range(yc):
            bpaths = bicycle(W/xc-m*(xc+1), H/yc-m*(yc+1))
            #bpaths = [skewy(p, pi/10) for p in bpaths]
            paths.extend([move(p, x*W/xc+m*(x+1), y*H/yc+m*(y+1)) for p in bpaths])

def one_bike():
    bpaths = [skewx(p, 0) for p in bicycle(W-10, H-10)]
    paths.extend([move(p, 5, 5) for p in bpaths])

many_bikes()
#one_bike()
print(len(paths))
plot_paths(paths)


f = open('bicycle_5.json', 'w')
f.write(str(paths))
