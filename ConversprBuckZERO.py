import numpy as np
import matplotlib.pyplot as plt


Vin = 12  
L = 1e-3  
R = 100     
Fs = 100e3 
D = 0.5           
Ts = 1 / Fs      

#Cálculos/Valores
Voutmed = D * Vin                        # Tensão média de saída
ILmed = Voutmed / R                     # Corrente média no indutor

delta_IL = ((Vin - Voutmed) * D  / L) * Ts  # Variação de corrente no indutor
IL_min = ILmed - delta_IL / 2
IL_max = ILmed + delta_IL / 2

# === Mostrar valores analíticos ===
print(f"Tensão média de saída (Voutmed): {Voutmed:.2f} V")
print(f"Corrente média no indutor (ILmed): {ILmed:.3f} A")
print(f"Variação da corrente no indutor (delta_IL): {delta_IL:.3f} A")
print(f"Corrente mínima no indutor: {IL_min:.3f} A")
print(f"Corrente máxima no indutor: {IL_max:.3f} A")
modo = "CONTÍNUO" if IL_min > 0 else "DESCONTÍNUO"
print(f"Modo de operação: {modo}")

#  Vetor de tempo 
num_ciclos = 1
t = np.arange(0, num_ciclos * Ts, Ts / 1000)  # 1000 amostras por ciclo  

# Corrente no indutor
IL_0 = np.zeros_like(t)

for i in range(len(t)):
    if t[i] < D * Ts:
        # ON: corrente sobe linearmente
        IL_0[i] = (Vin / L) * t[i]
    else:
        # OFF: corrente desce linearmente
        t_off = t[i] - D * Ts
        IL_0[i] = (Vin / L) * D * Ts - (Voutmed / R) / L * t_off

# Tensão de saída 
Vout = IL_0 * R

#  Gráficos 
plt.figure(figsize=(10, 5))
plt.plot(t * 1e6, IL_0, label='Corrente no Indutor [A]')
plt.plot(t * 1e6, Vout, label='Tensão de Saída [V]')
plt.title('Simulação Analítica do Conversor Buck (1 ciclo)')
plt.axhline(Voutmed, color='gray', linestyle='--', label='Vout Médio (6 V)')
plt.xlabel('Tempo [μs]')
plt.ylabel('Valor')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

