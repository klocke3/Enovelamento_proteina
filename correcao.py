from pdbfixer import PDBFixer
from openmm.app import PDBFile

fixer = PDBFixer(filename="/content/Enovelamento_proteina/peptideo_linear_ajustado.pdb")
fixer.findMissingResidues()
fixer.findMissingAtoms()
fixer.addMissingAtoms()
fixer.addMissingHydrogens(pH=7.4)

with open("/content/Enovelamento_proteina/peptideo_linear_final.pdb", "w") as f:
    PDBFile.writeFile(fixer.topology, fixer.positions, f)
