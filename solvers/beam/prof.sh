$*
gprof $1 gmon.out | gprof2dot | dot -Tpng -o prof.png