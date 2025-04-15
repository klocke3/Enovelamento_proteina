from pdbfixer import PDBFixer
from openmm.app import *
from openmm import *
from openmm.unit import *

# Carrega o PDB gerado anteriormente
fixer = PDBFixer(filename='/content/Enovelamento_proteina/peptideo_linear.pdb')

# Define o pH e adiciona hidrogênios ausentes
fixer.findMissingResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(pH=7.0)

# Salva a estrutura corrigida
with open('peptideo_corrigido.pdb', 'w') as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)

# Agora carrega a estrutura corrigida com OpenMM
pdb = PDBFile('peptideo_corrigido.pdb')
forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

# Cria o sistema e simulação
system = forcefield.createSystem(pdb.topology,
                                 nonbondedMethod=NoCutoff,
                                 constraints=HBonds)
integrator = VerletIntegrator(0.001*picoseconds)
simulation = Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)

# Calcula energia sem minimizar
state = simulation.context.getState(getEnergy=True)
energy = state.getPotentialEnergy()
print("⚡ Energia total após correção com PDBFixer:", energy)
