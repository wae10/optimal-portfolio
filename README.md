# Optimal Portfolio Solver
![efficient portfolio graph](https://github.com/wae10/optimal-portfolio/blob/main/images/efficient_portfolio.png)
![terminal menu](https://github.com/wae10/optimal-portfolio/blob/main/images/terminal.png)


# Setup
## Virtual Environment
```
pyenv virtualenv 3.9.0 optimal
pyenv activate optimal
```

## Installation
Download PyPortfolioOpt module in virtual environment.
```
https://github.com/robertmartin8/PyPortfolioOpt
```
Clone/download the project and run:
```
python setup.py install
```
Or:
```
pip install PyPortfolioOpt
```

## Usage
```python script.py```

## Common Issues 
### Solver / GLPK Related
I ran into an issue with this on Mac when trying to incorporate the PyPortfolioOpt module. This fixed it:
```
brew install gsl fftw suite-sparse glpk
git clone https://github.com/cvxopt/cvxopt.git
cd cvxopt
git checkout `git describe --abbrev=0 --tags`
export CVXOPT_BUILD_FFTW=1    # optional
export CVXOPT_BUILD_GLPK=1    # optional
export CVXOPT_BUILD_GSL=1     # optional
python setup.py install
```
