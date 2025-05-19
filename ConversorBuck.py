import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do conversor
Vin = 12  
L = 1e-3  
R = 10    
C = 1e-6  
Fs = 100e3 
D = 0.5  

# Tempo de simulação
Ts = 1 / Fs
t = np.arange(0, 0.002, Ts)

# Corrente no indutor
I_L = np.zeros_like(t)
V_out = np.zeros_like(t)
# Ciclo "on"
for i in range(len(t)):
    if t[i] < D * Ts:
        I_L[i] = Vin/L * t[i]
        V_out[i] = Vin * D * (t[i]/Ts)
    else:
        I_L[i] = Vin/L * (Ts * D) - Vin/R * (t[i]-Ts*D)
        V_out[i] = Vin*D

# Tensão de saída
V_out = I_L * R

# Mostrar alguns valores
print("Tempo (s):", t[:10])
print("Corrente no Indutor (A):", I_L[:10])
print("Tensão de Saída (V):", V_out[:10])
print("Corrente máxima no indutor (A):", np.max(I_L))
print("Tensão média de saída (V):", np.mean(V_out))
print("Último valor da tensão de saída (V):", V_out[-1])

plt.plot(t, I_L, label='Corrente do Indutor')
plt.plot(t, V_out, label='Tensão de Saída')
plt.xlabel('Tempo (s)')
plt.ylabel('Valor')
plt.title('Simulação do Conversor Buck')
plt.legend()
plt.grid(True)
plt.show()

