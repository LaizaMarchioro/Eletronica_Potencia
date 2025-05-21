import numpy as np
import matplotlib.pyplot as plt

Vin = 36        
L = 220e-6        
R = 10          
C = 1e-6        
Fs = 50000     
D = 0.33333333333   #Duty Cycle       

# Tempo de simulação
t_sim = 5e-3        # 5 ms de simulação
dt = 1 / (fsw * 200)     # Passo de tempo pequeno para precisão
t = np.arange(0, t_sim, dt)

# Vetores para o Gráfico
I_L = np.zeros_like(t)
V_out = np.zeros_like(t)

# C.I
iL = 0
vout = 0

# Simulação passo a passo
for i in range(1, len(t)):
    if (t[i] % Ts) < D * Ts:  #calcula o tempo dentro do ciclo
        # Modo ON: Vin aplicado no indutor, chave fechada e indutor carregando
        vL = Vin - vout
    else:
        # Modo OFF: diodo conduz, indutor descarrega sobre a carga
        vL = -vout

    # Atualiza corrente do indutor 
    di = (vL / L) * Ts
    iL += di     #soma com o valor anterior não repetindo valores e atualizando apenas o tempo 

    # Atualiza V de saída 
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