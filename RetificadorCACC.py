import numpy as np
import matplotlib.pyplot as plt

# Inicia o código com a parte de RETIFICAÇÃO e FILTRAGEM do sinal AC 

# Sinal AC
f_ac = 60  # frequência da rede
V_rms = 220    #Tensão da rede 
V_p = V_rms * np.sqrt(2)      # Vpico = Vrms * raiz de 2
t_ac = np.linspace(0, 0.1, 100000)  # Aqui cria um vetor de tempo de 0 a 0,1 s com 100.000 pontos.
v_ac = V_p * np.sin(2 * np.pi * f_ac * t_ac)  #Gera a senoide.  ( W0= 2 * π * f_ac -- frequência para rad/s)  (Vac= Vpico.sen.(2pi.f.t))


# Retificação 
v_retif = np.abs(v_ac)    # simular a retificação da V alternada - retificação de onda completa.  # É equivalente a simular 4 diodos em ponte.
# np.abs() retorna o valor absoluto de cada elemento do vetor. Ou seja, os valores negativos viram positivos.


# Filtro capacitivo 
window_size = 1000        # Tamanho da janela para média móvel (para calcular o valor filtrado em um ponto, o código vai considerar os 1000 pontos vizinhos e fazer a média.)
v_filt = np.convolve(v_retif, np.ones(window_size)/window_size, mode='same')  
# np.ones(window_size)/window_size cria um vetor de tamanho 1000, com todos os elementos iguais a 1 /pelo tamanho da janela (1000)
#np.convolve(...) realiza uma convolução: onde "desliza" uma função sobre outra.  Retificada /¨¨\_/¨¨\_ e Filtrada ¨¨¨¨¨¨¨¨¨¨¨¨
# mode='same' faz que o vetor resultante tenha o mesmo tamanho que o vetor de entrada.



# Tensão média pós filtragem
# Aqui calcula a tensão média da entrada retificada e filtrada
# Ignorando a metade inicial (0,5).
#Esse valor vai ser a tensão de entrada CC do conversor Buck.
Vin = np.mean(v_filt[int(0.5 * len(v_filt)):])  

#Vin= 198,07 ( calculado)

# Nesse caso, como eu já tenho Vin e Vout_desejado. Calculo o Duty Cycle (D)(12/198,07)=0,0606

#CONVERSOR BUCK

L = 1e-3           # Indutância 
C = 10e-6          # Capacitância 
R = 10             # Carga resistiva 
Fs = 100e3         # Frequência de chaveamento
Ts = 1 / Fs         # Período de chaveamento
Vout_desejado = 12
D = Vout_desejado / Vin  # Duty Cycle agora calculado 


# Tempo de simulação
# Ciclos/Tempo de simulação 
# (nesse caso o circuito estabiliza entre 150 e 200 cilcos - fui na tentativa e erro até estabilizar)
num_ciclos = 200
t_total = num_ciclos * Ts
dt = Ts / 1000      # Tempo total de ciclos de chaveamento - dividido em 1000 amostras por ciclo.
t = np.arange(0, t_total, dt)


# Vetores de simulação
IL = np.zeros_like(t)
Vc = np.zeros_like(t)
IL[0] = 0
Vc[0] = 0

for i in range(1, len(t)):
    ton = D * Ts     #Tempo da chave ligada
    t_in_ciclo = t[i] % Ts     #Local Ciclo Atual
    
    if t_in_ciclo < ton:
        VL = Vin - Vc[i-1]  # Chave fechada (ligada): V sobre o indutor = Vin - Vout
    else:
        VL = -Vc[i-1]       # Chave aberta (desligada): V sobre o indutor = -Vout

    dIL = (VL / L) * dt      # atualiza a corrente no indutor.
    IL[i] = IL[i-1] + dIL
    Ic = IL[i] - (Vc[i-1] / R)      # Corrente no capacitor usando lei dos nós para atualizar VC
    dVc = (Ic / C) * dt               # atualiza tensão no capacitor
    Vc[i] = Vc[i-1] + dVc            #valor calculado anterior (i-1) + valor atual



Voutmed = np.mean(Vc[int(0.5 * len(t)):])        # quando o circuito já atingiu o regime permanente 
ILmed = np.mean(IL[int(0.5 * len(t)):])
IL_min = np.min(IL)
IL_max = np.max(IL)
modo = "CONTÍNUO" if IL_min >= 0 else "DESCONTÍNUO"


print(f"Tensão média de saída (Voutmed): {Voutmed:.2f} V")
print(f"Corrente média no indutor (ILmed): {ILmed:.3f} A")
print(f"Corrente mínima no indutor: {IL_min:.3f} A")
print(f"Corrente máxima no indutor: {IL_max:.3f} A")
print(f"Modo de operação: {modo}")
print(f"Vin (retificada e filtrada): {Vin:.2f} V")
print(f"Tensão de pico: {V_p:.2f} V")                                                   
print(f"Duty Cycle aplicado: {D:.4f}")

# Gráficos
plt.figure(figsize=(12, 6))
plt.plot(t * 1e6, IL, label='Corrente no Indutor [A]')
plt.plot(t * 1e6, Vc, label='Tensão no Capacitor (Saída) [V]')
plt.axhline(Voutmed, color='gray', linestyle='--', label='Vout Médio')
plt.title('Conversor Buck com Entrada Real de Rede Retificada')
plt.xlabel('Tempo [μs]')
plt.ylabel('Valor')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()