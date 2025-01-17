'''
PRESENTACIÓN FÍSICA COMPUTACIONAL - BLOQUE I
INTRODUCCIÓN A LA MODELIZACIÓN EN FÍSICA

MÉTODOS DE RUNGE KUTTA

Víctor Mira Ramírez
74528754Z
vmr48@alu.ua.es

Marco Mas Sempere
74392068V
mmsm13@alu.ua.es
'''
############################
# IMPORTACIÓN DE LIBRERÍAS #
############################

# locales
from runge_kutta import *
from plot_func import *
from edp import *
from eficiencia import *
# externas
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

############################
# DEFINICIÓN DE PARÁMETROS #
############################

L = 5.        # Dominio espacial
Nx = 150      # Puntos espaciales
dx = L/Nx     # Paso espacial

T = 5.        # Tiempo total
Nt = int(2e4) # Puntos temporales
dt = T/Nt     # Paso temporal

c = 1.        # Velocidad de la onda
m = 1.        # Masa del campo
D = 1.        # Coeficiente de difusión

n = 2         #Parametro de la condicion inicial

x = np.linspace(0, L, Nx)
t = np.linspace(0, T, Nt)

##################
# EDP A RESOLVER #
##################
# Parámetros de las EDP
params_diff = (D, dx)
params_kg = (c, m, dx)
params_schr = (1.0, m, dx, np.zeros(Nx))  # Potencial V(x) = 0
params_wave = (c, dx)

# Condiciones de estabilidad
estabilidad_diff = D*dt/dx**2
...
...
...

# Condiciones iniciales
u0_diff = np.exp(-((x-L/2)**2)/(2*0.5**2)) # Gaussiana centrada en L/2
u0_schr = np.sin(n*np.pi*x/L)  + 0j      # Seno con n+1 nodos
...
phi0_kg = np.exp(-((x-L/2)**2)/(2*0.5**2)) # Campo gaussiano
u0_kg = np.array([phi0_kg, np.zeros(Nx)])  # Estado inicial kg

# Resolución de las EDP
############
# DIFUSIÓN #
############
if estabilidad_diff >= 0.5:
        raise Exception('Condición de estabilidad no satisfecha')
u_diff_RKII_G = RKII_G(u0_diff, t, diffusion, params_diff)
u_diff_RKIV = RKIV(u0_diff, t, diffusion, params_diff)

################
# KLEIN-GORDON #
################
sol_RKIV = RKIV(u0_kg, t, klein_gordon, params_kg)
u_kg_RKIV  = sol_RKIV[:,0,:] # Campo phi
du_kg_RKIV = sol_RKIV[:,1,:] # Velocidad dphi/dt



################
# SCHRODINGER #
################
sol_RKIV = RKIV(u0_schr, t, schrodinger, params_schr)
sol_RKII_G = RKII_G(u0_schr, t, schrodinger, params_schr)
sol_RKIII_G = RKIII_G(u0_schr, t, schrodinger, params_schr)
sol_RKVI = RKVI(u0_schr, t, schrodinger, params_schr)

u_schr_RKIV  = np.real(sol_RKIV[:,:])/np.max(np.real(sol_RKIV))    # Campo phi
u_schr_RKII_G  = np.real(sol_RKII_G[:,:])/np.max(np.real(sol_RKII_G))    # Campo phi
u_schr_RKIII_G  = np.real(sol_RKIII_G[:,:])/np.max(np.real(sol_RKIII_G))    # Campo phi
u_schr_RKVI  = np.real(sol_RKVI[:,:])/np.max(np.real(sol_RKVI))    # Campo phi

u_schr_anal = np.zeros((Nt,Nx))
for i in range(Nt):
    u_schr_anal[i,:] = np.sin(n*np.pi*x[:]/L)*np.cos(-((n**2)*(np.pi**2)*t[i])/(2*L**2))

error2 = error_schr(u_schr_anal, u_schr_RKII_G, dx)
error3 = error_schr(u_schr_anal, u_schr_RKIII_G, dx)
error4 = error_schr(u_schr_anal, u_schr_RKIV, dx)
error6 = error_schr(u_schr_anal, u_schr_RKVI, dx)

plt.figure()
plt.plot(t, error2, label='error RKII_G')
plt.plot(t, error3, label='error RKIII_G')
plt.plot(t, error4, label='error RKIV')
plt.plot(t, error6, label='error RKVI')
plt.legend()
plt.show()


# Plots que irán en el archivo plot_func.py

# Difusión
fig, ax = plt.subplots(figsize=(7, 7))
plt.tight_layout()
line_RKII_G, = ax.plot(x, u_diff_RKII_G[0], label='RKIIG')
line_RKIV, = ax.plot(x, u_diff_RKIV[0], label='RKIV')
ax.set_xlim(np.min(x), np.max(x))
ax.set_xlabel('x')
ax.set_ylabel('u(x, t)')
ax.set_title('Evolución temporal de la Ecuación de Difusión')
ax.legend()

def update(frame):
    line_RKII_G.set_ydata(u_diff_RKII_G[frame])
    line_RKIV.set_ydata(u_diff_RKIV[frame])
    return line_RKII_G, line_RKIV

ani = FuncAnimation(fig, update, frames=range(0,Nt,5), blit=True, interval=1)
plt.show()



# Klein-Gordon
fig, ax = plt.subplots()
ax.set_xlim(np.min(x), np.max(x))
ax.set_ylim(-1.1*np.abs(np.min(du_kg_RKIV)), 1.1*np.abs(np.max(du_kg_RKIV)))
ax.set_xlabel("x")
ax.set_ylabel(r"$\phi(x,t)$")
ax.set_title("Evolución temporal del campo $\\phi(x, t)$")

line_phi_RKIV,  = ax.plot([], [], label="phi(x,t) - RKIV")
line_dphi_RKIV, = ax.plot([], [], label="dphi(x,t)/dt - RKIV")
time_text = ax.text(0.8*L, 0.8*np.max(u_kg_RKIV), '', fontsize=12)
ax.legend()

def update(frame):
    line_phi_RKIV.set_data(x, u_kg_RKIV[frame])
    line_dphi_RKIV.set_data(x, du_kg_RKIV[frame])
    time_text.set_text(f"t = {np.round(t[frame],2)}s")
    return line_phi_RKIV, line_dphi_RKIV, time_text

ani = FuncAnimation(fig, update, frames=range(0,Nt,5), blit=True, interval=1)
plt.show()



# Schrodinger

fig, ax = plt.subplots()
ax.set_xlim(np.min(x), np.max(x))
ax.set_ylim(-1.1*np.abs(np.min(u_schr_RKIV)), 1.1*np.abs(np.max(u_schr_RKIV)))
ax.set_xlabel("x")
ax.set_ylabel(r"$\phi(x,t)$")
ax.set_title("Evolución de Schrodinger $\\phi(x, t)$")

line_phi_RKII_G,  = ax.plot([], [], label="phi(x,t) - RKII_G")
line_phi_RKIII_G,  = ax.plot([], [], label="phi(x,t) - RKIII_G")
line_phi_RKIV,  = ax.plot([], [], label="phi(x,t) - RKIV")
line_phi_RKVI,  = ax.plot([], [], label="phi(x,t) - RKVI")

line_phi_anal,  = ax.plot([], [], label="phi(x,t) - analítica")
time_text = ax.text(0.8*L, 0.8*np.max(u_schr_RKIV), '', fontsize=12)
ax.legend()

def update(frame):
    line_phi_RKII_G.set_data(x, u_schr_RKII_G[frame])
    line_phi_RKIII_G.set_data(x, u_schr_RKIII_G[frame])
    line_phi_RKIV.set_data(x, u_schr_RKIV[frame])
    line_phi_RKVI.set_data(x, u_schr_RKVI[frame])

    line_phi_anal.set_data(x, u_schr_anal[frame])
    time_text.set_text(f"t = {np.round(t[frame],2)}s")
    return line_phi_RKII_G, line_phi_RKIII_G, line_phi_RKIV, line_phi_RKVI, line_phi_anal, time_text

ani = FuncAnimation(fig, update, frames=range(0,Nt,5), blit=True, interval=1)
plt.show()