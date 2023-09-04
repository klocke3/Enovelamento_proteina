# OpenMM simulation example

This repo is an effort to work out how to run a simulation of a protein-ligand complex with OpenMM.

What I'm looking for is for this to be as simple as possible:
1. read protein from PDB file
2. read ligand ideally from molfile or SDF
3. combine the protein and ligand into a complex
4. parameterise the ligand using GAFF
5. simulate
6. analyse

Many thanks to @jchodera and others in the OpenMM community for help in putting these scripts together.

## Versions and branches

OpenMM and its related tools change quite a bit over time. The original work here was based on OpenMM version 7.4,
and the tools have now been updated for newer versions. Because the code is somewhat version dependent I have created
branches for specific versions. The code on master branch will typically be for the latest version I have used (not
always the latest version of OpenMM).

### History

#### 2020
* initial version based on OpenMM 7.4
* main tools are for simulating a ligand-protein complex with and without solvent

#### Sep 2023
* updated for OpenMM 7.7
* better handling of commandline options (using argparse)

## simulateProtein.py: Basic Protein Simulation

Minimal example of setting up a protein and doing a simple minimisation.

Not much to say about this.

## simulateComplex.py: Basic Complex Simulation

How to set up a protein-ligand complex simulation.

After some help from @jchodera I put together this example to help illustrate this.

Note: currently this is running with OpenMM 7.4.2 because https://github.com/openmm/openmm/issues/2683
makes it difficult to use 7.5.0.

```
 python simulateComplex.py protein.pdb ligand1.mol output 5000
```
The arguments:

1. protein.pdb - a protein with hydrogens ready to simulate (as done in [simulateProtein.py]()
2. ligand1.mol - ligand in molfile format
3. The name to use as the base name of the results.
4. The number of iterations for the simulation. The step size is defined in the script as 2 femtoseconds.

The ligand is read using RDKit and then processed to:
* Add hydrogens
* Define the stereochemistry

The protein is then read in PDB format and added to a Modeller object.
The ligand is then added to the Modeller to generate the complex.
The system is then prepared using the appropriate force fields.


Try the simulation as:

```
python simulateComplex.py protein.pdb ligand1.mol output 5000
Warning: Unable to load toolkit 'OpenEye Toolkit'. The Open Force Field Toolkit does not require the OpenEye Toolkits, and can use RDKit/AmberTools instead. However, if you have a valid license for the OpenEye Toolkits, consider installing them for faster performance and additional file format support: https://docs.eyesopen.com/toolkits/python/quickstart-python/linuxosx.html OpenEye offers free Toolkit licenses for academics: https://www.eyesopen.com/academic-licensing
Processing protein.pdb and ligand1.mol with 5000 steps generating outputs output_complex.pdb output_minimised.pdb output_traj.pdb output_traj.dcd
using platform CPU
Reading ligand
Adding hydrogens
Reading protein
Preparing complex
System has 4666 atoms
Preparing system

Welcome to antechamber 17.3: molecular input file processor.

acdoctor mode is on: check and diagnosis problems in the input file.
-- Check Format for sdf File --
   Status: pass
-- Check Unusual Elements --
   Status: pass
-- Check Open Valences --
   Status: pass
-- Check Geometry --
      for those bonded   
      for those not bonded   
   Status: pass
-- Check Weird Bonds --
   Status: pass
-- Check Number of Units --
   Status: pass
acdoctor mode has completed checking the input file.

Info: Total number of electrons: 80; net charge: 0

Running: /home/timbo/miniconda3/envs/openmm-74/bin/sqm -O -i sqm.in -o sqm.out


Welcome to antechamber 17.3: molecular input file processor.

acdoctor mode is on: check and diagnosis problems in the input file.
-- Check Format for mol2 File --
   Status: pass
-- Check Unusual Elements --
   Status: pass
-- Check Open Valences --
   Status: pass
-- Check Geometry --
      for those bonded   
      for those not bonded   
   Status: pass
-- Check Weird Bonds --
   Status: pass
-- Check Number of Units --
   Status: pass
acdoctor mode has completed checking the input file.


Uses Periodic box: False , Default Periodic box: [Quantity(value=Vec3(x=2.0, y=0.0, z=0.0), unit=nanometer), Quantity(value=Vec3(x=0.0, y=2.0, z=0.0), unit=nanometer), Quantity(value=Vec3(x=0.0, y=0.0, z=2.0), unit=nanometer)]
Minimising ...
Equilibrating ...
Starting simulation with 5000 steps ...
#"Step","Potential Energy (kJ/mole)","Temperature (K)"
5000,-18315.23210555748,332.45093440432925
Simulation complete in 97.02251291275024 seconds at 330 K
```

The files `output_complex.pdb`, `output_minimised.pdb` and `output_traj.dcd` are generated.
The first is the complex, the second is that complex mimimised ready for simulation, the third the MD trajectory in DCD format.

See the code for details and gotchas.

## simulateComplexWithSolvent.py: Simulation with explicit solvent

```
python simulateComplexWithSolvent.py protein.pdb ligand1.mol output 5000
```

Build on the previous [simulateComplex.py]() example by including explicit solvent.
The system now has 58,052 atoms and takes quite a lot longer to simulate, almost 2 mins using
my laptop's GeForce GTX 1050 GPU. A 1ns simulation takes just under one hour.

Output is similar to the previous example.
See the code for details and gotchas.


## Protein and ligand preparation

The previous methods were a bit of a cheat as they used a protein that had been fully prepared for
simulation. It's pretty unlikely you will start with a protein in that state. There are 2 scripts that
illustrate how preparation can be done. The aim is to be able to do this entirely within OpenMM, but it seems
that's not quite possible.

The scripts are:

[prepareProtein.py]()
```
 python prepareProtein.py protein.pdb protein
```
This strips out everything that is not the protein, fixes problems in the protein, adds hydrogens and writes the
file `protein_prepared.pdb`. That file can be used as inputs to the previous simulations.

[prepareComplex.py]()
```
 python prepareComplex.py data/Mpro-x0387_0_apo-desolv.pdb Mpro-x0387_0
```
This aims to build a PDB file with protein and ligand (and optionally the crystallographic waters) that is
ready for simulation. It writes the files `protein_prepared.pdb` and `ligand_prepared.pdb`.
It doesn't do everything that's needed, so other toolkits will be required:
- ligand does not have hydrogens added
- ligand can only be written to PDB format

## Analysis

The MD trajectories are analysed using [MDTraj](http://mdtraj.org/) and the script [analyse.py]().
```
python analyse.py trajectory.dcd topology.pdb output
```
This requires the trajectory to be written out using the DCD reporter. The topology can be read from the minimised
starting point of the MD run. This can be used for simulations with or without water.

The RMSD of the ligand and the protein C-alpha atoms compared to the start of the trajectory are displayed in a chart
that is generated using [Plotly](https://plotly.com/graphing-libraries/)) with the name output.svg (where 'output' is the
last parameter passed to the `analyse.py` script).

Example analysis:
![Example analysis](analyse.svg?raw=true "Example analysis]")

For complexes that are stable the RMSDs should not change dramatically. For a complex that is unstable the ligand may 
detach from the protein and the RMSD will increase dramatically. Relatively long simulations will be needed, maybe in the 
order of 100s of ns (input welcome on this and on how valid these simulations will be without explicit water).

## Improvements

Suggestions for how to improve these scripts and/or additional examples are welcome.
