#!/bin/bash

python3 -m venv myenv
source myenv/bin/activate
echo '#### Checking python ####'
which python3
python3 -V

echo '#### Install requirements ####'
pip install --no-cache-dir -r ./requirements.txt
pip install pytest-cov

echo '#### Run tests & coverage ####'
pytest --cov=main utests --junitxml=./xmlReport/output.xml
python -m coverage xml

echo '### deactivate virtual environment ###'
deactivate
echo '### done jenkins script ###'