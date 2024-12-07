#!/bin/bash

# Conda Environment Setup Script for RAG Metrics Evaluator

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Environment name
ENV_NAME="rag-metrics-eval"

# Function to check if Conda is installed
check_conda() {
    if ! command -v conda &> /dev/null; then
        echo -e "${YELLOW}Conda is not installed. Please install Anaconda or Miniconda first.${NC}"
        exit 1
    fi
}

# Function to handle existing environment
handle_existing_environment() {
    # Check if environment exists
    if conda env list | grep -q "$ENV_NAME"; then
        echo -e "${YELLOW}Environment '$ENV_NAME' already exists.${NC}"
        
        # Prompt user for action
        read -p "Do you want to (u)pdate, (r)emove and recreate, or (c)ancel? [u/r/c]: " action
        
        case $action in
            [Uu])
                echo -e "${GREEN}Updating existing environment...${NC}"
                conda env update -n "$ENV_NAME" -f environment.yml
                ;;
            [Rr])
                echo -e "${RED}Removing existing environment and recreating...${NC}"
                conda env remove -n "$ENV_NAME"
                create_environment
                ;;
            [Cc])
                echo -e "${YELLOW}Environment setup cancelled.${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option. Exiting.${NC}"
                exit 1
                ;;
        esac
    else
        create_environment
    fi
}

# Function to create Conda environment
create_environment() {
    echo -e "${GREEN}Creating Conda environment '$ENV_NAME'...${NC}"
    conda env create -f environment.yml
}

# Function to activate environment
activate_environment() {
    echo -e "${GREEN}Activating environment...${NC}"
    conda activate "$ENV_NAME"
}

# Function to install Jupyter kernel
install_kernel() {
    echo -e "${GREEN}Installing Jupyter kernel...${NC}"
    python -m ipykernel install --user --name "$ENV_NAME" --display-name "RAG Metrics Eval"
}

# Function to verify installation
verify_installation() {
    echo -e "${GREEN}Verifying installation...${NC}"
    python -c "import ragas; print('RAGAS version:', ragas.__version__)"
}

# Main script
main() {
    check_conda
    handle_existing_environment
    activate_environment
    install_kernel
    verify_installation
    
    echo -e "${GREEN}Setup complete! Activate the environment with 'conda activate $ENV_NAME'${NC}"
}

# Run main function
main
