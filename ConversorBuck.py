import numpy as np
import matplotlib.pyplot as plt


Vin = 12  
L = 1e-3  
R = 10    
C = 1e-6  
Fs = 100e3 
D = 0.5  

# Tempo de simulação
Ts = 1 / Fs
t = np.arange(0, 0.002, Ts)  # Vetor de tempo de 0 até 2 ms com passo de 10microsegundos Ts

# Corrente no indutor
I_L = np.zeros_like(t)     #np.zeros_lik... cria um vetor do mesmo tamanho preenchido com zeros.
V_out = np.zeros_like(t)   #Para armazenar valores caculados. Para o gráfico

# Ciclo "on" / Primeiro ciclo    SIMULAÇÃO DE APENAS UM CICLO (corrente subindo e descendo linerarmente
for i in range(len(t)):      # ele não atualiza o valor anterior. Ele aplica as equações de um único ciclo
    if t[i] < D * Ts:        # a todos os instantes de tempo sem atualizar as condições iniciais de cada ciclo
        I_L[i] = Vin/L * t[i]
        V_out[i] = Vin * D * (t[i]/Ts)
    else:
        I_L[i] = Vin/L * (Ts * D) - Vin/R * (t[i]-Ts*D)
        V_out[i] = Vin*D


V_out = I_L * R

# Mostrar os 10 primeiros valores e plotar o gráfico
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

