

from neuron import h

import numpy as np
from itertools import izip

def taper_diam(sec,zero_bound,one_bound):
    ''' 
    mctavish 2010 
    http://www.neuron.yale.edu/phpbb/viewtopic.php?f=2&t=2131
    '''
    dx = 1./sec.nseg
    for (seg, x) in izip(sec, np.arange(dx/2, 1, dx)):
        seg.diam=(one_bound-zero_bound)*x+zero_bound



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



# soma = h.Section(name='soma')

# # parameters for cell j4a.hoc
# soma.L = 35 
# soma.nseg = 1 
# soma.diam = 25



h.xopen("cells/j4a.hoc")

soma = h.soma

dendritic = []

for sec in h.allsec():
    diam = sec.diam
    n = sec.L/50.+1
    sec.nseg = int(n) # needed in Python, automatic in hoc
    if h.n3d()==0:
        sec.diam = diam
    dendritic.append(sec)
    

dendritic_only = []
for sec in dendritic:
    if sec != h.soma:
        dendritic_only.append(sec)

assert len(dendritic)-1 == len(dendritic_only)


# ---- spines ---

spine_dens = 1.
spine_area = 0.83

for sec in dendritic_only:
    a = 0.
    for seg in sec.allseg():
        a += seg.area()
    F = (sec.L*spine_area*spine_dens + a)/a
    sec.L = sec.L*F**(2/3.)
    for seg in sec.allseg():
        seg.diam = seg.diam * F**(1/3.)
        #print seg.diam


# --- axon --- 

# initial segment between hillock + myelin
iseg = h.Section(name='iseg')
iseg.L = 15.
iseg.nseg = 5
iseg.diam = (soma(0.5).area()/(4.*np.pi))**(0.5)/10.

# axon hillock
hill = h.Section(name='hill')
hill.L = 10.
hill.nseg = 5

taper_diam(hill, 4*iseg.diam, iseg.diam)

#h.cas(hill)
#h('diam(0:1) = 4*1.4790199:1.4790199')


n_axon_seg = 5

myelin = [h.Section(name="myelin %d" % i) for i 
          in range(n_axon_seg)]
for myelin_sec in myelin:
    myelin_sec.nseg = 5 # each of the 5 sections has 5 segments
    myelin_sec.L = 100.
    myelin_sec.diam = iseg.diam

node = [h.Section(name="node %d" % i) for i 
        in range(n_axon_seg)]
for node_sec in node:
    node_sec.nseg = 1
    node_sec.L = 1.
    node_sec.diam = iseg.diam*0.75


# childsec.connect(parentsec, parentx, childx)
hill.connect(soma, 0.5, 0)
iseg.connect(hill, 1 , 0)
myelin[0].connect(iseg, 1, 0)
node[0].connect(myelin[0], 1, 0)

for i in range(n_axon_seg-1):
     myelin[i+1].connect(node[i], 1, 0)
     node[i+1].connect(myelin[i+1], 1 ,0)

#h.topology()


for sec in h.allsec():
    sec.insert('pas')
    sec.Ra = ra
    sec.cm = c_m
    sec.g_pas = 1./rm
    sec.e_pas = v_init

    sec.insert('na')

# dendrite
for sec in dendritic_only:
    sec.gbar_na = gna_dend
    sec.insert('km')
    sec.gbar_km = gkm
    sec.insert('kca')
    sec.gbar_kca = gkca
    sec.insert('ca')
    sec.gbar_ca = gca
    sec.insert('cad')


# na+ channels
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


for myelin_sec in myelin:
    myelin_sec.cm = cm_myelin
    myelin_sec.gbar_na = gna_dend
        
hill.gbar_na = gna_node
iseg.gbar_na = gna_node

for node_sec in node:
    node_sec.g_pas = g_pas_node
    node_sec.gbar_na = gna_node

iseg.insert('kv')
iseg.gbar_kv = gkv_axon

hill.insert('kv') 
hill.gbar_kv = gkv_axon

for sec in h.allsec():
    if h.ismembrane('k_ion'):
        sec.ek = Ek
    if h.ismembrane('na_ion'):
        sec.ena = Ena
        h.vshift_na = -5
    if h.ismembrane('ca_ion'):
        sec.eca = 140
        h.ion_style("ca_ion",0,1,0,0,0)
        h.vshift_ca = 0




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

h.dt = 0.025
tstop = 500

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

import pickle 

f = open('data/L5_record_full_cell.p', 'wb')
pickle.dump((list(t),list(v_soma)), f)
f.close()

# for i in xrange(140,150):
#     print t[i], v_soma[i]


# --- plotting ---

import pylab as pl

pl.plot(t,v_soma)
#pl.xlim(0,160)
#pl.ylim(-80,60)
pl.savefig('data/img/L5_record_full_cell.png')


