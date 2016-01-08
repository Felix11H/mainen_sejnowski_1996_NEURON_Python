
from neuron import h

import sys
import pickle 
import pylab as pl

from fig1_core import *
from params.fig1_params import *


def fig1_make(cell_path, st_amp, label, spines=True):

    soma, dendrite, axon = init_cell(cell_path, spines)

    # --- stimulation ---

    st = h.IClamp(soma(0.5))
    st.dur = st_dur
    st.delay = st_del
    st.amp = st_amp

    v_soma = h.Vector()   
    t = h.Vector()        
    v_soma.record(soma(0.5)._ref_v)
    t.record(h._ref_t)
 
    h.dt = dt

    def initialize():
        h.finitialize(v_init)
        h.fcurrent()

    def integrate():
        while h.t<tstop:
            h.fadvance()

    def run():
        initialize()
        integrate()

    run()


    # --- data saving --- 

    f = open('data/%s_python.p' % label, 'wb')
    pickle.dump((list(t),list(v_soma)), f)
    f.close()

    # --- plotting ---

    pl.plot(t,v_soma)
    #pl.xlim(0,160)
    #pl.ylim(-80,60)
    pl.savefig('data/img/%s_python.png' % label)


if __name__=='__main__':
    fig1_make(sys.argv[1], float(sys.argv[2]), sys.argv[3], spines=bool(int(sys.argv[4])))
