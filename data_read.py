import os.path
import numpy as np

###==================================================================================
def GetOutCar(path,need):            # extract information from OUTCAR
	
	with open(path+'OUTCAR','r') as f:
		lines = f.readlines()

	PosList0 = [i for i,line in enumerate(lines) if 'k-points           NKPTS' in line]
	nkpt = int(lines[PosList0[-1]].strip().split()[3])
	nbnd = int(lines[PosList0[-1]].strip().split()[-1])
	
	if need == 'nkpt': return nkpt             # number of kpoints
	elif need == 'nbnd': return nbnd           # number of bands  
	elif need == 'lattice':
		PosList1 = [i for i,line in enumerate(lines) if 'direct lattice vectors' in line]
		lattice = np.zeros((3,3))
		for i in range(3):
			lattice[i,:] = list(map(float,lines[PosList1[-1]+1+i].strip().split()[0:3]))
		return lattice
	elif need == 'recip':
		PosList2 = [i for i,line in enumerate(lines) if 'reciprocal lattice vectors' in line]
		recip = np.zeros((3,3))
		for i in range(3):
			recip[i,:] = list(map(float,lines[PosList2[-1]+1+i].strip().split()[3::]))
		return recip
	elif need == 'ckpts':             # kpoints in Cartesian Coordinate
		PosList3 = [i for i,line in enumerate(lines) if 'k-points in units of 2pi/SCALE and weight' in line]
		ckpts = np.zeros((nkpt,3))
		for i in range(nkpt):
			ckpts[i,:] = list(map(float,lines[PosList3[-1]+1+i].strip().split()[0:3]))
		dist = np.power(np.power(np.diff(ckpts,axis=0),2).sum(axis=1),0.5)   
		xkpts = np.concatenate(([0],dist),axis=0).cumsum()	
		return xkpts
	elif need == 'fkpts':
		PosList4 = [i for i,line in enumerate(lines) if 'k-points in reciprocal lattice and weights' in line]
		fkpts = np.zeros((nkpt,3))
		for i in range(nkpt):
			fkpts[i,:] = list(map(float,lines[PosList4[-1]+1+i].strip().split()[0:3]))
		return fkpts
	elif need == 'fermi':
		PosList5 = [i for i,line in enumerate(lines) if 'E-fermi' in line]
		fermi = float(lines[PosList5[-1]].strip().split()[2])
		return fermi

###===============================================================================================
def GetEiGen(path,soc):                                   # extract band information from EIGENVAL

	with open(path+'EIGENVAL','r') as f:
		lines = f.readlines()

	enum = int(lines[5].strip().split()[0])       # number of electrons
	nkpt = int(lines[5].strip().split()[1])       # number of KPOINTS
	nbnd = int(lines[5].strip().split()[2])       # number of bands
	
	if soc == 0 or soc == 1:
		band = []; kpt = []
		for i in range(nkpt):
			k_idx = 7 + i*(nbnd+2)
			for j in range(nbnd):
				b_idx = k_idx + j + 1
				band.append(float(lines[b_idx].strip().split()[1]))

		bands = np.array(band).reshape(nkpt,nbnd)
		return bands

	elif soc == -1:
		upband = []; downband = [];kpt = []
		for i in range(nkpt):
			k_idx = 7 + i*(nbnd+2)
			for j in range(nbnd):
				b_idx = k_idx + j + 1
				upband.append(float(lines[b_idx].strip().split()[1]))
				downband.append(float(lines[b_idx].strip().split()[2]))

		upbands = np.array(upband).reshape(nkpt,nbnd)
		downbands = np.array(downband).reshape(nkpt,nbnd)
		return upbands,downbands

###=======================================
def ReadEband(path1,path2,soc): 

	if soc==0 or soc==1:
		xpts = GetOutCar(path1,'ckpts')            # find all kpoints to plot band 
		band = GetEiGen(path1,soc)
		np.save(path1+'Eigen.npy',band)
		fermi_energy = GetOutCar(path2,'fermi') 
		band = band-fermi_energy
		bands = np.c_[xpts,band]
		np.save(path1+'Eband.npy',bands)
    
	elif soc==-1:
		xpts = GetOutCar(path1,'ckpts')            # find all kpoints to plot band 
		upband,downband = GetEiGen(path1,soc)
		fermi_energy = GetOutCar(path2,'fermi') 
		upband = upband-fermi_energy
		downband = downband-fermi_energy
		np.save(path1+'EigenUp.npy',upband)
		np.save(path1+'EigenDown.npy',downband)
		upbands = np.c_[xpts,upband]
		downbands = np.c_[xpts,downband]
		np.save(path1+'EbandUp.npy',upbands)
		np.save(path1+'EbandDown.npy',downbands)
    
###=======================================
path1='./1band_cal/'
path2='./2dos_cal/'
soc = -1   ### 0: without soc; 1: soc; -1: spin-polarized
ReadEband(path1,path2,soc) 
