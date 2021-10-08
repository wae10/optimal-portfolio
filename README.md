# Optimal Portfolio Solver
## https://my-optimal-portfolio.herokuapp.com/
![efficient portfolio graph](https://github.com/wae10/optimal-portfolio/blob/main/images/efficient_portfolio.png)
![terminal menu](https://github.com/wae10/optimal-portfolio/blob/main/images/terminal.png)

# Currently Running on a Heroku Web App
Access the demo at:
```
https://my-optimal-portfolio.herokuapp.com/
```

# Setup Instructions for More Functionality
## Virtual Environment
Create a virtual environment to store packages. Example:
```
pyenv virtualenv 3.9.0 optimal
pyenv activate optimal
```

## Packages
Install packages in virtual environment with pip.
```
pip install -r requirements.txt
```

## Usage
```python script.py```

## Common Issues 
### Solver / GLPK Related
I ran into an issue with this on Mac when trying to incorporate the PyPortfolioOpt package. This fixed it:
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
 