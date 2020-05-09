rm -rf .pytest_cache
export PYTHONPATH="/Users/tobj/Devprojects/blog_oo/"
export ENVIRONMENT="dev"
echo "Running pytest..."
pytest -v
#export MYPYPATH="/Users/tobj/Devprojects/blog_oo/"
#echo "Running mypy checks..."
#mypy --ignore-missing-imports .