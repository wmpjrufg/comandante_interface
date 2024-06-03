import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

def atualizar_grafico(frame, x, y):
    # Adicionar novos dados
    x.append(frame)
    y.append(random.uniform(0, 0.6))
    
    # Limitar o número de pontos no gráfico para manter a visualização mais limpa
    if len(x) > 100:
        x.pop(0)
        y.pop(0)
    
    # Limpar o eixo e plotar os dados atualizados
    plt.clf()
    plt.plot(x, y, 'b-', marker='o')
    plt.title('Gráfico em Tempo Real')
    plt.axhline(y=0.2, color='r', linestyle='--')
    plt.xlabel('Tempo')
    plt.ylabel('Valores acumulados')
    plt.grid(True)

    if y[-1] <= 0.2:
        print('Necessita de reposição!!')
    else:
        print("Cheio!!")

# Inicializar os dados
x = []
y = []

# Criar a figura e o eixo
fig = plt.figure()
ani = animation.FuncAnimation(fig, atualizar_grafico, fargs=(x, y), interval=1000, save_count=len(x))

plt.show()
