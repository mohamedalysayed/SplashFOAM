"""
This file contains the dictionaries connecting the GUI text to the OpenFOAM dictionary entries.

"""
grad_schemes = {"Gauss Linear":"Gauss linear","Cell Limited Gauss Linear":"cellLimited Gauss Linear 1","faceLimited Gauss Linear":"faceLimited Gauss Linear 1","Least Squares":"leastSquares"}

div_schemes = {"Gauss Linear":"Gauss linear","Gauss Upwind":"Gauss upwind","Gauss Linear Upwind":"Gauss linearUpwind grad(U)",
               "Gauss Limited Linear":"Gauss limitedLinear 1",}
temporal_schemes = {"Euler":"Euler","Crank-Nicolson":"crankNicolson","Steady State":"steadyState"}