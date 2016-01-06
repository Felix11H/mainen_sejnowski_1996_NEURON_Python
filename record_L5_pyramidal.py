
from neuron import h


ra        = 150.
global_ra = ra
rm        = 30000.
c_m       = 0.75
cm_myelin = 0.04
g_pas_node = 0.02

v_init    = -70.
h.celsius   = 37.

Ek = -90.
Ena = 60.

gna_dend = 20.
gna_node = 30000.
gna_soma = gna_dend

gkv_axon = 2000.
gkv_soma = 200.

gca = 0.3
gkm = 0.1
gkca = 3.

gca_soma = gca
gkm_soma = gkm
gkca_soma = gkca



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
soma.gbar_na = gna_soma
soma.insert('kv')
soma.gbar_kv = gkv_soma

soma.insert('km')
soma.gbar_km = gkm_soma
soma.insert('kca')
soma.gbar_kca = gkca_soma
soma.insert('ca')
soma.gbar_ca = gca_soma
soma.insert('cad')



# --- stimulation ---

st = h.IClamp(soma(0.5))
st.dur = 900
st.delay = 5

st.amp = 0.2

v_soma = h.Vector()   
t = h.Vector()        
v_soma.record(soma(0.5)._ref_v)
t.record(h._ref_t)


# --- simulation control 


tstop = 100

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




import pickle 

f = open('data/L5_record.p', 'wb')
pickle.dump((list(t),list(v_soma)), f)
f.close()

for i in xrange(140,150):
    print t[i], v_soma[i]

import pylab as pl

pl.plot(t,v_soma)
pl.xlim(0,100)
#pl.ylim(-80,10)
pl.savefig('img/L5_record.png')


