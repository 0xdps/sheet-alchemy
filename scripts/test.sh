#!/bin/bash

# SheetAlchemy CI Runner - GitHub Actions with act and Docker
# Usage: ./ci [OPTIONS]
# 
# Options:
#   --help, -h           Show this help message
#   --job JOB            Run specific job (test, build, all) [default: test]
#   --python VERSION     Run specific Python version (3.8, 3.9, 3.10, 3.11, 3.12, 3.13) [default: 3.9]
#   --os OS              Run specific OS (ubuntu-latest, windows-latest, macos-latest) [default: ubuntu-latest]
#   --event EVENT        Trigger specific event (push, pull_request) [default: push]
#   --fast               Run local script instead of Docker (faster but less accurate)
#   --dry-run            Show what would be executed without running
#   --list               List available workflows and jobs

set -e  # Exit on any error

# Default values
JOB="test"
PYTHON_VERSION="3.9"
OS="ubuntu-latest"
EVENT="push"
FAST_MODE=false
DRY_RUN=false
LIST_MODE=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}  🚀 SheetAlchemy Local CI Runner${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_usage() {
    echo -e "${CYAN}Usage: $0 [OPTIONS]${NC}"
    echo ""
    echo -e "${YELLOW}Options:${NC}"
    echo -e "  ${GREEN}--help, -h${NC}           Show this help message"
    echo -e "  ${GREEN}--job JOB${NC}            Run specific job (test, build, all) [default: test]"
    echo -e "  ${GREEN}--python VERSION${NC}     Python version (3.8, 3.9, 3.10, 3.11, 3.12, 3.13) [default: 3.9]"
    echo -e "  ${GREEN}--os OS${NC}              OS (ubuntu-latest, windows-latest, macos-latest) [default: ubuntu-latest]"
    echo -e "  ${GREEN}--event EVENT${NC}        Event (push, pull_request) [default: push]"
    echo -e "  ${GREEN}--fast${NC}               Run local script instead of Docker (faster)"
    echo -e "  ${GREEN}--dry-run${NC}            Show what would be executed"
    echo -e "  ${GREEN}--list${NC}               List available workflows and jobs"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo -e "  ./ci                                    # Run test job with Python 3.9 on Ubuntu"
    echo -e "  ./ci --job all --python 3.11           # Run all jobs with Python 3.11"
    echo -e "  ./ci --job build                       # Run only build job"
    echo -e "  ./ci --fast                            # Run fast local checks"
    echo -e "  ./ci --python 3.8 --os ubuntu-latest  # Test Python 3.8 on Ubuntu"
    echo -e "  ./ci --list                            # List available options"
}

check_dependencies() {
    echo -e "${BLUE}🔍 Checking dependencies...${NC}"
    
    # Check if act is installed
    if ! command -v act &> /dev/null; then
        echo -e "${RED}❌ act is not installed. Install with: brew install act${NC}"
        exit 1
    fi
    
    # Check if Docker is running
    if ! docker ps &> /dev/null; then
        echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Dependencies check passed${NC}"
}

list_workflows() {
    echo -e "${CYAN}📋 Available workflows and jobs:${NC}"
    act --list
    echo ""
    echo -e "${YELLOW}Supported options:${NC}"
    echo -e "${GREEN}Jobs:${NC} test, build, all"
    echo -e "${GREEN}Python versions:${NC} 3.8, 3.9, 3.10, 3.11, 3.12, 3.13"
    echo -e "${GREEN}Operating systems:${NC} ubuntu-latest, windows-latest, macos-latest"
    echo -e "${GREEN}Events:${NC} push, pull_request"
}

run_fast_local() {
    echo -e "${YELLOW}🏃 Running fast local CI (without Docker)...${NC}"
    echo ""
    
    # Install dependencies
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    python -m pip install --upgrade pip > /dev/null 2>&1
    pip install -e . > /dev/null 2>&1
    pip install -e ".[dev]" > /dev/null 2>&1
    
    # Run checks
    echo -e "${BLUE}🔍 Running flake8...${NC}"
    flake8 sheetalchemy --count --select=E9,F63,F7,F82 --show-source --statistics
    
    echo -e "${BLUE}🖤 Checking formatting...${NC}"
    black --check sheetalchemy/
    
    echo -e "${BLUE}📋 Checking imports...${NC}"
    isort --check-only sheetalchemy/
    
    echo -e "${BLUE}🧪 Running tests...${NC}"
    pytest tests/ --cov=sheetalchemy --cov-report=term-missing
    
    echo -e "${GREEN}🎉 Fast local CI completed!${NC}"
}

run_act_docker() {
    local job="$1"
    local python_ver="$2"
    local os="$3"
    local event="$4"
    
    echo -e "${BLUE}🐳 Running GitHub Actions with act and Docker...${NC}"
    echo -e "${CYAN}Configuration:${NC}"
    echo -e "  Job: ${GREEN}$job${NC}"
    echo -e "  Python: ${GREEN}$python_ver${NC}"
    echo -e "  OS: ${GREEN}$os${NC}"
    echo -e "  Event: ${GREEN}$event${NC}"
    echo ""
    
    local act_cmd="act $event --container-architecture linux/amd64"
    
    # Add job specification
    if [[ "$job" != "all" ]]; then
        act_cmd="$act_cmd --job $job"
    fi
    
    # Add matrix parameters
    act_cmd="$act_cmd --matrix python-version:$python_ver --matrix os:$os"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}🔍 Dry run - would execute:${NC}"
        echo -e "${CYAN}$act_cmd${NC}"
        return
    fi
    
    echo -e "${BLUE}⚡ Executing: ${CYAN}$act_cmd${NC}"
    echo ""
    
    eval $act_cmd
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            print_header
            print_usage
            exit 0
            ;;
        --job)
            JOB="$2"
            shift 2
            ;;
        --python)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        --os)
            OS="$2"
            shift 2
            ;;
        --event)
            EVENT="$2"
            shift 2
            ;;
        --fast)
            FAST_MODE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --list)
            LIST_MODE=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
done

# Main execution
print_header

if [[ "$LIST_MODE" == "true" ]]; then
    list_workflows
    exit 0
fi

# Validate job parameter
if [[ ! "$JOB" =~ ^(test|build|all)$ ]]; then
    echo -e "${RED}❌ Invalid job: $JOB. Must be one of: test, build, all${NC}"
    exit 1
fi

# Validate Python version
if [[ ! "$PYTHON_VERSION" =~ ^(3\.[8-9]|3\.1[0-3])$ ]]; then
    echo -e "${RED}❌ Invalid Python version: $PYTHON_VERSION${NC}"
    echo -e "${YELLOW}Supported versions: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13${NC}"
    exit 1
fi

# Validate OS
if [[ ! "$OS" =~ ^(ubuntu-latest|windows-latest|macos-latest)$ ]]; then
    echo -e "${RED}❌ Invalid OS: $OS${NC}"
    echo -e "${YELLOW}Supported OS: ubuntu-latest, windows-latest, macos-latest${NC}"
    exit 1
fi

if [[ "$FAST_MODE" == "true" ]]; then
    run_fast_local
else
    check_dependencies
    run_act_docker "$JOB" "$PYTHON_VERSION" "$OS" "$EVENT"
fi

echo ""
echo -e "${GREEN}✨ CI execution completed!${NC}"