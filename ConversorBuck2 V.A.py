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
t_total = 0.002                     # Tempo total da simulação (2 ms)
t = np.arange(0, t_total, Ts)       # Vetor de tempo

# Vetores para o Gráfico
I_L = np.zeros_like(t)
V_out = np.zeros_like(t)

# Condições iniciais
iL = 0
vout = 0

# Simulação passo a passo
for i in range(1, len(t)):
    if (t[i] % Ts) < D * Ts:
        # Modo ON: Vin aplicado no indutor, chave fechada e indutor carregando
        vL = Vin - vout
    else:
        # Modo OFF: diodo conduz, indutor descarrega sobre a carga
        vL = -vout

    # Atualiza corrente do indutor (método de Euler)
    di = (vL / L) * Ts
    iL += di     #soma com o valor anterior não repetindo valores e atualizando apenas o tempo 

    # Atualiza tensão de saída (queda sobre resistor)
    vout = iL * R

    # Armazena os resultados para o gráfico
    I_L[i] = iL
    V_out[i] = vout

# Resultados
print("Corrente máxima no indutor:", np.max(I_L))
print("Tensão média de saída:", np.mean(V_out))

# Gráfico
plt.plot(t, I_L, label='Corrente no Indutor')
plt.plot(t, V_out, label='Tensão de Saída')
plt.xlabel('Tempo')
plt.ylabel('Valor')
plt.title('Simulação Realista do Conversor Buck')
plt.grid(True)
plt.legend()
plt.show()