## virtual environment
envcreate optimal
workon optimal

## Installation
### setup
download: https://github.com/robertmartin8/PyPortfolioOpt
python setup.py install

### solver instructions (I ran into an issue with this on Mac when trying to incorporate the PyPortfolioOpt module)
brew install gsl fftw suite-sparse glpk
git clone https://github.com/cvxopt/cvxopt.git
cd cvxopt
git checkout `git describe --abbrev=0 --tags`
export CVXOPT_BUILD_FFTW=1    # optional
export CVXOPT_BUILD_GLPK=1    # optional
export CVXOPT_BUILD_GSL=1     # optional
python setup.py install

### Usage
python script.py