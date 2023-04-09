from numpy import sqrt, sin, cos, tan, arccos, arctan 

def cartesian_to_cylindrical(x, y, z):
    return sqrt(x ** 2 + y ** 2), arctan(y/x), z

def cartesian_to_spherical(x, y, z):
    rho, theta = sqrt(x ** 2 + y ** 2 + z ** 2), arctan(y / x)
    phi = arccos(z / rho)
    
    return rho, theta, phi

def cylindrical_to_cartesian(r, theta, z):
    return r * cos(theta), r * sin(theta), z

def spherical_to_cartesian(rho, theta, phi):
    return rho * sin(phi) * cos(theta), rho * sin(phi) * sin(theta), rho * cos(phi)
