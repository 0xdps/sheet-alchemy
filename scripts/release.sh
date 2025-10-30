#!/bin/bash

# SheetAlchemy Release Helper
# Usage: ./scripts/release.sh [version]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Check if version is provided
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Error: Version number required${NC}"
    echo -e "${BLUE}Usage: $0 <version>${NC}"
    echo -e "${BLUE}Example: $0 2.1.0${NC}"
    exit 1
fi

NEW_VERSION="$1"

# Validate version format (basic semver check)
if [[ ! $NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}❌ Error: Invalid version format. Use semantic versioning (e.g., 2.1.0)${NC}"
    exit 1
fi

echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${PURPLE}  🚀 SheetAlchemy Release Helper${NC}"
echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Get current version
CURRENT_VERSION=$(python -c "import sheetalchemy; print(sheetalchemy.__version__)" 2>/dev/null || echo "unknown")
echo -e "${BLUE}📊 Current version: ${GREEN}$CURRENT_VERSION${NC}"
echo -e "${BLUE}🎯 New version: ${GREEN}$NEW_VERSION${NC}"
echo ""

# Check if we're on trunk branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "trunk" ]; then
    echo -e "${YELLOW}⚠️  Warning: You're on branch '$CURRENT_BRANCH', not 'trunk'${NC}"
    echo -e "${BLUE}💡 Consider switching to trunk: git checkout trunk${NC}"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  Warning: You have uncommitted changes${NC}"
    git status --short
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run tests
echo -e "${BLUE}🧪 Running tests...${NC}"
./ci --fast
echo -e "${GREEN}✅ Tests passed${NC}"
echo ""

# Update version in __init__.py
echo -e "${BLUE}📝 Updating version...${NC}"
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" sheetalchemy/__init__.py
rm sheetalchemy/__init__.py.bak

# Verify the change
UPDATED_VERSION=$(python -c "import sheetalchemy; print(sheetalchemy.__version__)")
if [ "$UPDATED_VERSION" != "$NEW_VERSION" ]; then
    echo -e "${RED}❌ Error: Failed to update version${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Version updated to $NEW_VERSION${NC}"
echo ""

# Show git diff
echo -e "${BLUE}📋 Changes to commit:${NC}"
git diff sheetalchemy/__init__.py
echo ""

# Commit the version change
echo -e "${BLUE}💾 Committing version bump...${NC}"
git add sheetalchemy/__init__.py
git commit -m "Bump version to $NEW_VERSION"
echo -e "${GREEN}✅ Version bump committed${NC}"
echo ""

# Push changes
echo -e "${BLUE}📤 Pushing changes...${NC}"
git push origin $CURRENT_BRANCH
echo -e "${GREEN}✅ Changes pushed${NC}"
echo ""

# Create git tag
echo -e "${BLUE}🏷️  Creating git tag...${NC}"
git tag "v$NEW_VERSION"
git push origin "v$NEW_VERSION"
echo -e "${GREEN}✅ Tag v$NEW_VERSION created and pushed${NC}"
echo ""

echo -e "${GREEN}🎉 Release preparation completed!${NC}"
echo ""
echo -e "${PURPLE}📋 Next steps:${NC}"
echo -e "${BLUE}1.${NC} Go to GitHub: https://github.com/0xdps/g-odm/releases"
echo -e "${BLUE}2.${NC} Create a new release using tag: ${GREEN}v$NEW_VERSION${NC}"
echo -e "${BLUE}3.${NC} Add release notes describing changes"
echo -e "${BLUE}4.${NC} Publish the release"
echo -e "${BLUE}5.${NC} GitHub Actions will automatically publish to PyPI"
echo ""
echo -e "${YELLOW}💡 The automated workflow will:${NC}"
echo -e "   • Run full test suite"
echo -e "   • Build the package" 
echo -e "   • Validate everything"
echo -e "   • Publish to PyPI"
echo -e "   • Create deployment summary"
echo ""
echo -e "${GREEN}✨ All done! Your release is ready.${NC}"