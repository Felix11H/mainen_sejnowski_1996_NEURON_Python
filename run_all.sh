
x86_64/special demofig1_rec.hoc

python plot_from_hoc_data.py data/fig1_L3_aspiny_hoc.dat
python plot_from_hoc_data.py data/fig1_L4_stellate_hoc.dat
python plot_from_hoc_data.py data/fig1_L2_3_pyramid_hoc.dat
python plot_from_hoc_data.py data/fig1_L5_pyramid_hoc.dat

python fig1_lab.py "cells/lcAS3.hoc" 0.05 "fig1_L3_aspiny" 0
python fig1_lab.py "cells/j7.hoc" 0.07 "fig1_L4_stellate" 1
python fig1_lab.py "cells/j8.hoc" 0.1 "fig1_L2_3_pyramid" 1
python fig1_lab.py "cells/j4a.hoc" 0.2 "fig1_L5_pyramid" 1

