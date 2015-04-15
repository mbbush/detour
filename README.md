# detour
Calculate the detour each of two drivers would have to make to 
pick up and drop off the other.

google.py does this using the Google Distance Matrix API, and includes
i/o.
earth.py is a library for distance computations on a spherical earth, 
and includes a function earth.detour that determines which of two drivers 
would make the shorter detour if traveling in straight lines. It does not 
have any i/o.
