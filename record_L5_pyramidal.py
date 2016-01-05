
from neuron import h
from params.demofig1_params import *

# ------ soma ------

soma = h.Section(name='soma')

# parameters for cell j4a.hoc
soma.L = 35 
soma.nseg = 1 
soma.diam = 25

# passive membrane channels
soma.insert('pas')
soma.Ra = ra
soma.cm = c_m
soma.g_pas = 1./rm
soma.e_pas = v_init

# na+ channels
soma.insert('na')


# ------ axon ------

#iseg = h.Section(name='iseg')
#hill = h.Section(name='hill')


# ---- dendrite ----


# for sec in h.allsec():
#     sec.insert('pas')


# --- stimulation ---

st = h.IClamp(soma(0.5))
st.dur = 900
st.delay = 5

st.amp = 0.1

v_soma = h.Vector()   
t = h.Vector()        
v_soma.record(soma(0.5)._ref_v)
t.record(h._ref_t)

h.load_file("stdrun.hoc")
h.init()
h.tstop = 1000
h.run()

#import pickle
#fp = open('data/


import pylab as pl

pl.plot(t,v_soma)

pl.savefig('img/L5_record.png')


