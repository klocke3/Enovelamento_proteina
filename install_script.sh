#!/bin/bash

# Função para exibir a barra de progresso
progress_bar() {
    local current_step=$1
    local total_steps=$2
    local width=50

    # Verifica se total_steps é maior que zero para evitar divisão por zero
    if [ $total_steps -eq 0 ]; then
        echo "Erro: o número total de etapas não pode ser zero."
        exit 1
    fi

    # Calcula a porcentagem
    local percent=$(( (100 * current_step) / total_steps ))
    # Calcula o progresso feito
    local done=$((current_step * width / total_steps))
    # Calcula o espaço restante
    local left=$((width - done))
    # Gera a parte preenchida da barra
    local fill=$(printf "%${done}s" | tr ' ' '#')
    # Gera a parte vazia da barra
    local empty=$(printf "%${left}s" | tr ' ' '-')

    echo -ne "\r[${fill}${empty}] ${percent}%"
}

# Lista de pacotes a instalar
packages=(
  "PeptideBuilder"
  "py3Dmol"
  "MDAnalysis"
  "libstdc++6"
  "Miniconda3"
  "Openff-toolkit"
  "Openmm-Forcefields"
  "Mdtraj"
  "Plotly"
  "Kaleido"
  "Pdb2Pqr"
  "PDBfixer"
)

# Função para determinar o comando de instalação de acordo com o pacote
get_install_command() {
    local package_name=$1
    case $package_name in
        "PeptideBuilder")
            echo "pip install biopython -q >/dev/null 2>&1 && pip install git+https://github.com/mtien/PeptideBuilder.git -q >/dev/null 2>&1"
            ;;
        "py3Dmol")
            echo "pip install py3Dmol -q >/dev/null 2>&1"
            ;;
        "MDAnalysis")
            echo "pip install --upgrade MDAnalysis -q >/dev/null 2>&1"
            ;;
        "libstdc++6")
            echo "sudo apt-get install -y libstdc++6 -q >/dev/null 2>&1"
            ;;
        "Miniconda3")
            echo "wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh -b -f -p /usr/local >/dev/null 2>&1"
            ;;
        "Openff-toolkit")
            echo "conda install -c conda-forge openff-toolkit -y -q >/dev/null 2>&1"
            ;;
        "Openmm-Forcefields")
            echo "conda install -c conda-forge openmmforcefields -y -q >/dev/null 2>&1"
            ;;
        "Mdtraj")
            echo "conda install -c conda-forge mdtraj -y -q >/dev/null 2>&1"
            ;;
        "Plotly")
            echo "conda install -c plotly plotly -y -q >/dev/null 2>&1"
            ;;
        "Kaleido")
            echo "pip install -U kaleido -q >/dev/null 2>&1"
            ;;
        "Pdb2Pqr")
            echo "conda install -c conda-forge pdb2pqr -y -q >/dev/null 2>&1"
            ;;
        "PDBfixer")
            echo "conda install -c conda-forge pdbfixer -y -q >/dev/null 2>&1"
            ;;
        *)
            echo "echo 'Comando desconhecido para $package_name'"
            ;;
    esac
}

total_steps=${#packages[@]}
current_step=0

echo "Iniciando a instalação de pacotes..."

# Loop de instalação
for pkg in "${packages[@]}"; do
    ((current_step++))  # Incrementa a etapa
    progress_bar $current_step $total_steps
    echo -e "\nInstalando $pkg..."
    
    # Obter o comando de instalação correto
    install_command=$(get_install_command $pkg)
    
    # Executar o comando de instalação
    eval $install_command

    sleep 1  # Simula a instalação (substitua com a instalação real)
    echo "$pkg instalado com sucesso! ✅"
done

echo -e "\nTodos os pacotes foram instalados com sucesso! 🎉"
