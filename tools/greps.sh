#!/bin/sh

echo "mSUGRA"
echo "=================================="
grep -i -r -n --include "*.tex" msugra *
echo "=================================="

echo "TODO"
echo "=================================="
grep -i -r -n --include "*.tex" todo *
echo "=================================="

echo "cutflow"
echo "=================================="
grep -i -r -n --include "*.tex" cutflow *
echo "=================================="

echo "SMS"
echo "=================================="
grep -i -r -n --include "*.tex" sms *
echo "=================================="

echo "\\MET"
echo "=================================="
grep -r -n --include "*.tex" \\MET *
echo "=================================="

echo "PtW"
echo "=================================="
grep -r -n --include "*.tex" PtW *
echo "=================================="

echo "Ptl"
echo "=================================="
grep -r -n --include "*.tex" Ptl *
echo "=================================="
