import argparse

def split_chains_by_residue_number(pqr_path, output_path):
    """
    Converte um arquivo .pqr para .pdb, separando cadeias com base na enumeração dos resíduos.
    Sempre que o número do resíduo diminui, uma nova cadeia é iniciada.
    """
    chain_ids = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    current_chain_index = 0
    current_chain = chain_ids[current_chain_index]
    last_residue_number = None

    with open(pqr_path, 'r') as file:
        lines = file.readlines()

    new_lines = []

    for line in lines:
        if line.startswith(('ATOM', 'HETATM')):
            try:
                residue_number = int(line[22:26])
            except ValueError:
                new_lines.append(line)
                continue

            if last_residue_number is not None:
                if residue_number < last_residue_number and current_chain_index + 1 < len(chain_ids):
                    current_chain_index += 1
                    current_chain = chain_ids[current_chain_index]

            last_residue_number = residue_number

            # Atualiza o chain ID (coluna 22)
            new_line = line[:21] + current_chain + line[22:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(output_path, 'w') as out_file:
        out_file.writelines(new_lines)

    print(f"[✔] Arquivo salvo com cadeias separadas: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Separar cadeias em um arquivo .pqr com base na enumeração dos resíduos.")
    parser.add_argument("-i", "--input", required=True, help="Arquivo .pqr de entrada")
    parser.add_argument("-o", "--output", required=True, help="Arquivo .pdb de saída")

    args = parser.parse_args()

    split_chains_by_residue_number(args.input, args.output)
