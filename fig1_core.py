
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


from params.fig1_params import *


def init_cell(cell_path, spines=True):

    '''
    cell: path to cell definiton
    '''

    h('forall delete_section()')

    # ---- conditions ----

    h.celsius = temp

    # ---- soma & dendrite ----

    h.xopen(cell_path)

    soma = h.soma

    dendritic = []

    # segment lengths should be not longer than 50um
    # contains soma!
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

    if spines:

        for sec in dendritic_only:
            a = 0.
            for seg in sec.allseg():
                a += seg.area()
            F = (sec.L*spine_area*spine_dens + a)/a
            sec.L = sec.L*F**(2/3.)
            for seg in sec.allseg():
                seg.diam = seg.diam * F**(1/3.)


    # ---- axon ----

    # initial segment between hillock + myelin
    iseg = h.Section(name='iseg')
    iseg.L = iseg_L
    iseg.nseg = iseg_nseg
    soma_compl_area = 0
    for seg in soma:
        soma_compl_area += seg.area()
    print soma_compl_area
    iseg.diam = (soma_compl_area/(4.*np.pi))**(0.5)/10.

    # axon hillock
    hill = h.Section(name='hill')
    hill.L = hill_L
    hill.nseg = hill_nseg
    taper_diam(hill, 4*iseg.diam, iseg.diam)



    myelin = [h.Section(name="myelin %d" % i) for i 
              in range(n_axon_seg)]
    for myelin_sec in myelin:
        myelin_sec.nseg = myelin_nseg # each of the 5 sections has 5 segments
        myelin_sec.L = myelin_L
        myelin_sec.diam = iseg.diam

    node = [h.Section(name="node %d" % i) for i 
            in range(n_axon_seg)]
    for node_sec in node:
        node_sec.nseg = node_nseg
        node_sec.L = node_L
        node_sec.diam = iseg.diam*0.75


    # syntax: childsec.connect(parentsec, parentx, childx)
    hill.connect(soma, 0.5, 0)
    iseg.connect(hill, 1 , 0)
    myelin[0].connect(iseg, 1, 0)
    node[0].connect(myelin[0], 1, 0)

    for i in range(n_axon_seg-1):
         myelin[i+1].connect(node[i], 1, 0)
         node[i+1].connect(myelin[i+1], 1 ,0)


    # ---- mechanisms ----

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

    axon = [iseg, hill, myelin, node]

    return soma, dendritic_only, axon


    # st = h.IClamp(soma(0.5))
    # st.dur = st_dur
    # st.delay = st_delay

    # st.amp = st_amp

    # v_soma = h.Vector()   
    # t = h.Vector()        
    # v_soma.record(soma(0.5)._ref_v)
    # t.record(h._ref_t)

    # return v_soma, t
