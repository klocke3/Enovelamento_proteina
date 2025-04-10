import sys
from simtk.openmm.app import *
from simtk.openmm import *
from simtk import unit
from openmmforcefields.generators import SystemGenerator

if len(sys.argv) != 3:
    print('Usage: python prepareProtein.py input.pdb output')
    print('Creates output_minimised.pdb from the input PDB')
    exit(1)

pdb_in = sys.argv[1]
pdb_out = sys.argv[2]
print('Minimizando estrutura:', pdb_in)

# Carrega o PDB original
pdb = PDBFile(pdb_in)

# Gera o sistema com força padrão
system_generator = SystemGenerator(forcefields=['amber/ff14SB.xml', 'amber/tip3p_standard.xml'])
system = system_generator.create_system(pdb.topology)

# Define integrador e simulação
integrator = LangevinIntegrator(300 * unit.kelvin, 1 / unit.picosecond, 0.002 * unit.picoseconds)
simulation = Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)

# Minimização
print('⏳ Minimizando energia...')
simulation.minimizeEnergy()

# Salva estrutura minimizada
with open(pdb_out + '_minimised.pdb', 'w') as outfile:
    positions = simulation.context.getState(getPositions=True, enforcePeriodicBox=False).getPositions()
    PDBFile.writeFile(pdb.topology, positions, file=outfile, keepIds=True)

print('✅ Minimização concluída! Arquivo salvo como', pdb_out + '_minimised.pdb')
