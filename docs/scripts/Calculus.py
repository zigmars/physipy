# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import physipy
from physipy import Dimension
from fractions import Fraction
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

import numpy as np
import scipy.integrate as integrate
import scipy.constants as csts
from physipy import s, m, sr, K, units, constants
from physipy import quad
import physipy
import matplotlib.pyplot as plt

# %% [markdown]
# # Calculus : numerical toolbox

# %% [markdown]
# Some usefull numerical functions are provided, which basicaly consists in dimension-wrapped functions.
# The wrapping operation is needed because no mean to hook the handling of Quantity object is avalaible (as it is for numpy's functions and ufuncs).

# %% [markdown]
# ## Integrate with quad

# %% [markdown]
# Lets integrate planck's law : [we know the expected result is $\sigma T^4/\pi$](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law):

# %%
# physical constants
hp = constants["h"]
c = constants["c"]
kB = constants["k"]
sigma = constants["Stefan_Boltzmann"]

nm = units["nm"]
mum = units["mum"]

# %%
# blackbody at temperature 300K
Tbb = 300*K

# note : computing this factor once saves from overflow problems
x = hp*c / (kB * Tbb)
x_ = csts.h * csts.c /(csts.k * 300)

# Planck's law
def planck(lmbda):
    return 2*hp*c**2/lmbda**5 * 1/(np.exp(x/lmbda)-1) /sr

def planck_(lmbda):
    return 2 * csts.h * csts.c / lmbda**5 * 1 / (np.exp(x_/lmbda)-1)

# expected value
expected = sigma * Tbb**4 / (np.pi*sr)

# %%
lmbda_start = 0.001*nm
lmbda_stop = 1000*mum

res, _ = quad(planck, lmbda_start, lmbda_stop)

# %%
print(res)
print(expected)
print("error : ", res/expected-1)

# %% [markdown]
# The convergence can be seen : 

# %%
integrands = []
ech_stop = np.logspace(2, 4, 20)*mum
ech_stop.favunit = mum
for lmbda_stop in ech_stop:
    res, _ = quad(planck, lmbda_start, lmbda_stop)
    integrands.append(res)

# %%
integrands = physipy.quantity.utils.list_of_Q_to_Q_array(integrands)

# %%
from physipy import setup_matplotlib
setup_matplotlib()

plt.semilogx(ech_stop, integrands, "o", label="integral")
plt.axhline(expected, label="expected value")
plt.legend()


# %% [markdown]
# The processing time is quite longer with Quantities. Use this wrapper when speed is not mandatory.

# %%
# %timeit quad(planck_, lmbda_start.value, lmbda_stop.value)
# %timeit quad(planck, lmbda_start, lmbda_stop)

# %% [markdown]
# Other writing possible:

# %%
def planck(lmbda, T):
    x = hp*c / (kB * T)
    return 2*hp*c**2/lmbda**5 * 1/(np.exp(x/lmbda)-1) /sr

res, _ = quad(lambda lmbda: planck(lmbda, 300*K), lmbda_start, lmbda_stop)
print(res)

# %% [markdown]
# Other writing possible : 

# %%
res, _ = quad(planck, lmbda_start, lmbda_stop, args=(300*K,))
print(res)

# %% [markdown]
# ## Root solver

# %% [markdown]
# A wrapper of `scipy.optimize.root`:

# %%
from physipy.quantity.calculus import root

def toto(t):
    return -10*s + t


# %%
print(root(toto, 0*s))


# %%
def tata(t, p):
    return -10*s*p + t

print(root(tata, 0*s, args=(0.5,)))

# %% [markdown]
# A wrapper of `scipy.optimize.brentq`:

# %%
from physipy.quantity.calculus import brentq


# %%
print(brentq(toto, -10*s, 10*s))
print(brentq(tata, -10*s, 10*s, args=(0.5,)))


# %%
