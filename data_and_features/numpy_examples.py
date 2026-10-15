
# %% 1. Why NumPy? Python loop vs vectorised
import time
import numpy as np

n = 10_000_000
xs = list(range(n))
arr = np.arange(n)

t = time.perf_counter()
doubled_list = [x * 2 for x in xs]
t_loop = time.perf_counter() - t

t = time.perf_counter()
doubled_arr = arr * 2
t_vec = time.perf_counter() - t

print(f"Python loop: {t_loop:.3f} s")
print(f"NumPy:       {t_vec:.3f} s  (about {t_loop / t_vec:.0f}x faster)")


# %% 2. Creating arrays
a = np.array([1, 2, 3])                 # from a list
b = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])         # from nested lists

print(np.zeros((2, 3)))                 # all zeros
print(np.ones((2, 3)))                  # all ones
print(np.arange(0, 10, 2))              # [0 2 4 6 8]
print(np.linspace(0, 1, 5))             # 5 evenly spaced numbers from 0 to 1
print(np.eye(3))                        # identity matrix

rng = np.random.default_rng(seed=0)     # reproducible random numbers
print(rng.normal(size=(2, 3)))


# %% 3. Shape, dtype and indexing
X = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])

print("shape:", X.shape)                # (2, 3): rows, columns
print("dtype:", X.dtype)                # float64
print("ndim: ", X.ndim)                 # 2
print("size: ", X.size)                 # 6 values in total

print("X[0, 1]  =", X[0, 1])            # row 0, column 1 -> 2.0
print("X[:, 0]  =", X[:, 0])            # whole first column
print("X[1, :]  =", X[1, :])            # whole second row
print("X[:, 1:] =\n", X[:, 1:])         # all rows, columns 1 and onwards

# Changing the dtype
print(X.astype(np.int32))


# %% 4. Reshaping
v = np.arange(12)
print(v.reshape(3, 4))                  # 3 rows, 4 columns
print(v.reshape(2, -1).shape)           # -1 means "work it out": (2, 6)
print(v.reshape(3, 4).T.shape)          # transpose: (4, 3)


# %% 5. Axes: the axis you name is the one that disappears
X = np.arange(12).reshape(3, 4)
print(X)

print("axis=0:", X.sum(axis=0))         # one value per column -> shape (4,)
print("axis=1:", X.sum(axis=1))         # one value per row    -> shape (3,)
print("all:   ", X.sum())               # a single number

print("mean per column:", X.mean(axis=0))
print("max per row:    ", X.max(axis=1))


# %% 6. Broadcasting: (n, d) combined with (d,)
rng = np.random.default_rng(0)
X = rng.normal(loc=50, scale=10, size=(5, 3))   # 5 samples, 3 features

mu = X.mean(axis=0)                     # shape (3,)
std = X.std(axis=0)                     # shape (3,)
Z = (X - mu) / std                      # (5, 3) - (3,) -> (5, 3)

print("mu:      ", mu.round(2))
print("Z means: ", Z.mean(axis=0).round(2) + 0.0)   # approximately 0
print("Z stds:  ", Z.std(axis=0).round(2))    # approximately 1

# Broadcasting also works between a column and a row
col = np.array([[0], [10], [20]])       # shape (3, 1)
row = np.array([1, 2, 3])               # shape (3,)
print(col + row)                        # shape (3, 3)


# %% 7. Boolean masks
ages = np.array([22, 35, 41, 58, 64])

mask = ages > 40
print(mask)                             # [False False  True  True  True]
print(ages[mask])                       # [41 58 64]
print(ages[(ages > 30) & (ages < 60)])  # combine with & and |  (use parentheses)
print("how many over 40:", (ages > 40).sum())

# Replace values using a mask
capped = ages.copy()
capped[capped > 60] = 60
print(capped)

# np.where: choose between two values
print(np.where(ages >= 40, "senior", "junior"))


# %% 8. A small dataset as arrays: features X and labels y
# Illustrative values (bill length mm, flipper length mm, body mass g)
X = np.array([[39.1, 181, 3750],
              [46.1, 211, 4500],
              [49.0, 196, 4350],
              [38.6, 189, 3600]])
y = np.array(["Adelie", "Gentoo", "Chinstrap", "Adelie"])

print("X shape:", X.shape)              # (n, d) = (4, 3)
print("y shape:", y.shape)              # (n,)    = (4,)

# One row per sample, one column per feature
print("First sample:     ", X[0])
print("Mean body mass:   ", X[:, 2].mean())
print("Adelie samples:\n", X[y == "Adelie"])


# %% 9. Loading a CSV into NumPy
import io

csv_text = """bill_length,flipper,body_mass,species
39.1,181,3750,Adelie
46.1,211,4500,Gentoo
49.0,196,4350,Chinstrap
38.6,189,3600,Adelie
"""
# With a real file, replace io.StringIO(csv_text) by "penguins.csv"
data = np.genfromtxt(io.StringIO(csv_text), delimiter=",",
                     skip_header=1, usecols=(0, 1, 2))
labels = np.genfromtxt(io.StringIO(csv_text), delimiter=",",
                       skip_header=1, usecols=3, dtype=str)

print(data)
print(labels)


# %% 10. JSON to an array
import json

json_text = """
[
  {"name": "A", "age": 25, "salary": 400000},
  {"name": "B", "age": 60, "salary": 410000},
  {"name": "C", "age": 41, "salary": 520000}
]
"""
records = json.loads(json_text)
X = np.array([[r["age"], r["salary"]] for r in records])   # flatten to columns
print(X)
print(X.shape)


# %% 11. An image is an array
# A tiny 5x5 grayscale "image": 0 = black, 255 = white
img = np.zeros((5, 5), dtype=np.uint8)
img[1:4, 1:4] = 128                     # grey square
img[2, 2] = 255                         # white centre pixel
print(img)
print("shape:", img.shape, " dtype:", img.dtype)

# A colour image has an extra axis: (height, width, channels)
rgb = np.zeros((5, 5, 3), dtype=np.uint8)
rgb[:, :, 0] = 255                      # fill the red channel
print("rgb shape:", rgb.shape)

# Flatten the image to one feature vector with 25 features
print("flattened:", img.reshape(-1).shape)


# %% 12. Categorical features: one-hot encoding
cities = np.array(["Oslo", "Bergen", "Tromsø", "Oslo"])
categories = np.unique(cities)          # sorted: ['Bergen' 'Oslo' 'Tromsø']
print(categories)

index = np.searchsorted(categories, cities)   # [1 0 2 1]
one_hot = np.eye(len(categories))[index]
print(one_hot)
# Each row has exactly one 1: no false ordering between the cities


# %% 13. Missing values with NaN
X = np.array([[1.0, 2.0],
              [np.nan, 3.0],
              [5.0, np.nan]])

print(np.isnan(X))                      # where are the gaps?
print("missing per column:", np.isnan(X).sum(axis=0))

print("mean:   ", X.mean(axis=0))       # NaN spreads through the calculation
print("nanmean:", np.nanmean(X, axis=0))  # ignores the NaNs

col_means = np.nanmean(X, axis=0)
X_filled = np.where(np.isnan(X), col_means, X)   # fill gaps with column means
print(X_filled)


# %% 14. Saving and loading arrays
X = np.arange(6).reshape(2, 3)

np.save("X.npy", X)                     # one array, binary format
X_back = np.load("X.npy")
print(np.array_equal(X, X_back))        # True

np.savetxt("X.csv", X, delimiter=",", fmt="%d")   # plain text, human-readable
print(open("X.csv").read())


# %% 15. Common pitfalls
a = np.arange(5)
b = a                                   # NOT a copy: both names point to the same data
b[0] = 99
print(a)                                # a changed too!

c = np.arange(5)
d = c.copy()                            # a real copy
d[0] = 99
print(c)                                # c is unchanged

# Integer division and dtype surprises
print(np.array([1, 2, 3]) / 2)          # float result: [0.5 1.  1.5]
print(np.array([1, 2, 3], dtype=np.uint8) - 5)   # wraps around (unsigned integers)
