#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔍 Checking documentation coherence..."

# Run pytest with detailed output
pytest tests/documentation/test_core_docs_coherence.py -v

# Check the exit status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Documentation is coherent!${NC}"
else
    echo -e "${RED}❌ Documentation coherence issues found${NC}"
    echo "Please check the test output above and fix any issues"
    exit 1
fi
