#By: Luis Agapito
import numpy as np
import xml.etree.ElementTree as et
import os
import scipy.io as sio
import subprocess
#nkpoints = 155
#nbands   = 25

prefix = 'Pt'
nspin    = 1 
#1 : collinear & non-spin polarized
#2 : collinear & spin polarized
#1 = noncollinear (SOC) & non-spin polarized

#band_a   = 16
#band_b   = 17
Ha2eV    = 27.211396132

p=subprocess.Popen("grep Fermi scf.out | cut -c 25-36",stdout=subprocess.PIPE,shell=True)
(output,err) = p.communicate()
Ef = float(output)
print "Fermi level in scf.out is %f eV"%Ef

#     number of k points=   279  Methfessel-Paxton smearing, width (Ry)=  0.0200
p=subprocess.Popen("grep 'number of k points=' bands.out | cut -c 25-30",stdout=subprocess.PIPE,shell=True)
(output,err) = p.communicate()
nkpoints = int(float(output))
print "Number of kpoints in bands.out is %d eV"%nkpoints

#     number of Kohn-Sham states=           18
p=subprocess.Popen("grep 'number of Kohn-Sham states=' bands.out | cut -c 33-45",stdout=subprocess.PIPE,shell=True)
(output,err) = p.communicate()
nbands = int(float(output))
print "Number of bands in bands.out is %d eV"%nbands


eigs = np.zeros((nbands,nkpoints,nspin))
for ispin in range(nspin):
    for ik in range(nkpoints):
      if nspin==1:
         tree=et.parse(prefix+'.save/K%05d/eigenval.xml'%(ik+1));
      else:
         tree=et.parse(prefix+'.save/K%05d/eigenval%d.xml'%(ik+1,ispin+1));
      root=tree.getroot()
      for eig0 in root.iter('EIGENVALUES'):
          eig1 = eig0.text.split('\n')[1:nbands+1]
          eigs[:,ik,ispin] = np.asarray(map(float,eig1))*Ha2eV - Ef

sio.savemat('bands.mat',{'eigs':eigs})
##spin up bandgap
#e_band_a = max(eigs[band_a-1,:,0])
#e_band_b = min(eigs[band_b-1,:,0])      
#print "Spin up e1=%f,e2=%f,Egap=%f"%(e_band_a,e_band_b,e_band_b-e_band_a)
#
##spin down bandgap
#e_band_a = max(eigs[band_a-1,:,1])
#e_band_b = min(eigs[band_b-1,:,1])      
#print "Spin down e1=%f,e2=%f,Egap=%f"%(e_band_a,e_band_b,e_band_b-e_band_a)


#<?xml version="1.0"?>
#<?iotk version="1.2.0"?>
#<?iotk file_version="1.0"?>
#<?iotk binary="F"?>
#<?iotk qe_syntax="F"?>
#<Root>
#  <INFO nbnd="35" ik="1" ispin="1"/>
#  <UNITS_FOR_ENERGIES UNITS="Hartree"/>
#  <EIGENVALUES type="real" size="35">
#-2.811438898263705E-001

#SOC without polarization
#<?xml version="1.0"?>
#<?iotk version="1.2.0"?>
#<?iotk file_version="1.0"?>
#<?iotk binary="F"?>
#<?iotk qe_syntax="F"?>
#<Root>
#  <INFO nbnd="18" ik="1"/>
#  <UNITS_FOR_ENERGIES UNITS="Hartree"/>
#  <EIGENVALUES type="real" size="18">
# 2.672673587905708E-001
