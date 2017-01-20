# Generate a triangle velocity pattern
#
#    /\              max_rpm
#   /  \
#  /    \    /-----  0
#        \  /   
#         \/         min_rpm
# <---ramp---><--pause--> 

import math

ppr = 2000.0
#min_rpm = -1000.0
#max_rpm = 1000.0
min_rpm =  -100.0
max_rpm = 100.0
ramp = 0.5
pause = 0.5
nsamples = 1000000

segs =  ( 
    (0, 0), 
    (ramp/4.0, max_rpm),
    (3*ramp/4.0, min_rpm),
    (ramp, 0),
    (ramp+pause, 0)
)

dt = (ramp+pause)/nsamples
slew = (max_rpm - min_rpm)/ramp * 2

jitter = max_rpm * ppr / 60.0 * dt
print "jitter ", 100.0 * jitter, "%"

def header(f):
    global nsamples,ramp,pause
    f.write("data length,%d\n" % nsamples)
    f.write("frequency,%f\n" %  (1.0 / (ramp+pause)))
    f.write("amp,%f\n" % 5.0)
    f.write("offset,0.000000000\n")
    f.write("phase,0.000000000\n")
    f.write("xpos,value\n")

fa = open("pysim_A.csv", "w")
fb = open("pysim_B.csv", "w")
header(fa)
header(fb)

(t1, rpm1) = segs[0]
ph1 = 0

for (t2, rpm2) in segs[1:]:
    t = t1
    rpm = rpm1
    slew = (rpm2-rpm1) / (t2-t1)
    while (t <= t2):
        rpm = rpm1 + slew * (t-t1)
        ph = ph1 + (rpm1 * (t-t1) + 0.5 * slew * (t-t1) *(t-t1)) * ppr / 60.0
        if (ph % 1 > 0.5): out_A = 5
        else: out_A = 0
        if ((ph+0.25) % 1 > 0.5): out_B = 5
        else: out_B = 0
        fa.write("%f,%f\n" % (t,out_A))
        fb.write("%f,%f\n" % (t,out_B))
        t += dt
    t1 = t-dt
    rpm1 = rpm
    ph1 = ph

print "end"
