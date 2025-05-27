import numpy as np
import matplotlib.pyplot as plt

#Esses foram os parâmetros que eu estimei inicialmente. Nesse código eles funcionaram bem. 
Vin = 12            
L = 1e-3            
C = 10e-6           
R = 10              
Fs = 100e3          # frequência de chaveamento  
D = 0.5             # Duty cycle
Ts = 1 / Fs         # Período

#Tensão média de saída deve ser: 6 V (concordando com -- Voutmed = D * Vin)
#Corrente média no indutor (ILmed): 0.6 A (Lei de Ohm: ILmed = Voutmed / R)
#Variação de corrente no indutor (delta_IL): 30mA ((Vin - Voutmed) * D / L) * Ts 
#ou seja, a corrente no indutor vária +-15mA em torno de 0,6A. Logo, Imin=0,585 e Imax=0,615 quando 
#as condições iniciais forem os valores médios esperados. 


# Ciclos/Tempo de simulação 
# (nesse caso o circuito estabiliza entre 150 e 200 cilcos - fui na tentativa e erro até estabilizar)
num_ciclos = 200
t_total = num_ciclos * Ts
dt = Ts / 1000       # Tempo total de ciclos de chaveamento - dividido em 1000 amostras por ciclo.
t = np.arange(0, t_total, dt) 


#  Vetores e Condiçõ9es Iniciais 
IL = np.zeros_like(t)       
Vc = np.zeros_like(t)       
IL[0] = 0     #Aqui quanto mais próximo esses valores iniciais estiverem dos valores médios
Vc[0] = 0     #mais exatos serão os resultados de Iminimo e Imaximo. 


for i in range(1, len(t)):
    ton = D * Ts   #Tempo da chave ligada
    t_in_ciclo = t[i] % Ts    #Local Ciclo Atual
    
    if t_in_ciclo < ton:
        VL = Vin - Vc[i-1]   # Chave fechada (ligada): V sobre o indutor = Vin - Vout
    else:
        VL = -Vc[i-1]          # Chave aberta (desligada): V sobre o indutor = -Vout


    
    dIL = VL / L * dt          # atualiza a corrente no indutor. 
    IL[i] = IL[i-1] + dIL
    Ic = IL[i] - Vc[i-1] / R          # Corrente no capacitor usando lei dos nós para atualizar VC

    dVc = Ic / C * dt            # atualiza tensão no capacitor
    Vc[i] = Vc[i-1] + dVc       #valor calculado anterior (i-1) + valor atual 


    

Voutmed = np.mean(Vc[int(0.5 * len(t)):])      # quando o circuito já atingiu o regime permanente
ILmed = np.mean(IL[int(0.5 * len(t)):])
IL_min = np.min(IL) 
IL_max = np.max(IL)
modo = "CONTÍNUO" if IL_min >= 0 else "DESCONTÍNUO"



print(f"Tensão média de saída (Voutmed): {Voutmed:.2f} V")     # a tensão média de saída tem que tender para 6V
print(f"Corrente média no indutor (ILmed): {ILmed:.3f} A")     
print(f"Corrente mínima no indutor: {IL_min:.3f} A")
print(f"Corrente máxima no indutor: {IL_max:.3f} A")
print(f"Modo de operação: {modo}")


plt.figure(figsize=(10, 5))
plt.plot(t * 1e6, IL, label='Corrente no Indutor [A]')
plt.plot(t * 1e6, Vc, label='Tensão no Capacitor (Saída) [V]')    #a ondulação da tensão de saída é reduzida pelo capacitor
plt.axhline(Voutmed, color='gray', linestyle='--', label='Vout Médio')
plt.title('Conversor Buck - Modo Contínuo com Capacitor de Saída')
plt.xlabel('Tempo [μs]')
plt.ylabel('Valor')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
