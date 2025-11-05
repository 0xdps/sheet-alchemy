#!/bin/bash

# SheetAlchemy PyPI Publishing Script
# Usage: ./scripts/publish.sh [--test] [--dry-run]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Parse arguments
TEST_PYPI=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            TEST_PYPI=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--test] [--dry-run]"
            echo ""
            echo "Options:"
            echo "  --test     Upload to TestPyPI instead of PyPI"
            echo "  --dry-run  Show what would be done without executing"
            echo "  --help     Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}  🚀 SheetAlchemy PyPI Publishing${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [[ "$TEST_PYPI" == "true" ]]; then
    echo -e "${YELLOW}📋 Target: TestPyPI (test.pypi.org)${NC}"
else
    echo -e "${GREEN}📋 Target: Production PyPI (pypi.org)${NC}"
fi

if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${BLUE}🔍 Mode: Dry run (no actual upload)${NC}"
fi

echo ""

# Step 1: Run tests
echo -e "${BLUE}🧪 Step 1: Running tests...${NC}"
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}  Would run: ./ci --fast${NC}"
else
    ./ci --fast
    echo -e "${GREEN}  ✅ Tests passed${NC}"
fi
echo ""

# Step 2: Get current version
echo -e "${BLUE}📊 Step 2: Checking version...${NC}"
CURRENT_VERSION=$(python -c "import sheetalchemy; print(sheetalchemy.__version__)")
echo -e "${GREEN}  Current version: $CURRENT_VERSION${NC}"
echo ""

# Step 3: Clean build
echo -e "${BLUE}🧹 Step 3: Cleaning previous builds...${NC}"
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}  Would run: rm -rf build/ dist/ *.egg-info/${NC}"
else
    rm -rf build/ dist/ *.egg-info/
    echo -e "${GREEN}  ✅ Cleaned build artifacts${NC}"
fi
echo ""

# Step 4: Build package
echo -e "${BLUE}📦 Step 4: Building package...${NC}"
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}  Would run: python -m build${NC}"
else
    python -m build
    echo -e "${GREEN}  ✅ Package built successfully${NC}"
    
    # Show built files
    echo -e "${BLUE}  Built files:${NC}"
    ls -la dist/
fi
echo ""

# Step 5: Validate package
echo -e "${BLUE}✅ Step 5: Validating package...${NC}"
if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}  Would run: python -m twine check dist/*${NC}"
else
    python -m twine check dist/*
    echo -e "${GREEN}  ✅ Package validation passed${NC}"
fi
echo ""

# Step 6: Upload package
echo -e "${BLUE}🚀 Step 6: Uploading to PyPI...${NC}"

if [[ "$DRY_RUN" == "true" ]]; then
    if [[ "$TEST_PYPI" == "true" ]]; then
        echo -e "${YELLOW}  Would run: python -m twine upload --repository testpypi dist/*${NC}"
    else
        echo -e "${YELLOW}  Would run: python -m twine upload dist/*${NC}"
    fi
else
    if [[ "$TEST_PYPI" == "true" ]]; then
        echo -e "${YELLOW}  Uploading to TestPyPI...${NC}"
        python -m twine upload --repository testpypi dist/*
        echo ""
        echo -e "${GREEN}🎉 Successfully uploaded to TestPyPI!${NC}"
        echo -e "${BLUE}📋 Test installation:${NC}"
        echo -e "   pip install -i https://test.pypi.org/simple/ sheetalchemy==$CURRENT_VERSION"
        echo -e "${BLUE}📋 TestPyPI URL:${NC}"
        echo -e "   https://test.pypi.org/project/sheetalchemy/"
    else
        echo -e "${GREEN}  Uploading to Production PyPI...${NC}"
        python -m twine upload dist/*
        echo ""
        echo -e "${GREEN}🎉 Successfully published to PyPI!${NC}"
        echo -e "${BLUE}📋 Installation:${NC}"
        echo -e "   pip install sheetalchemy==$CURRENT_VERSION"
        echo -e "${BLUE}📋 PyPI URL:${NC}"
        echo -e "   https://pypi.org/project/sheetalchemy/"
    fi
fi

echo ""
echo -e "${GREEN}✨ Publishing process completed!${NC}"

if [[ "$DRY_RUN" == "false" && "$TEST_PYPI" == "false" ]]; then
    echo ""
    echo -e "${PURPLE}📢 Don't forget to:${NC}"
    echo -e "  1. Create a GitHub release with tag v$CURRENT_VERSION"
    echo -e "  2. Update documentation if needed"
    echo -e "  3. Announce the release"
fi