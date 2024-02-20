import multiprocessing as mp
import matplotlib.pyplot as plt

# Definir una función para modificar el valor compartido
def modificar_valor(valor, indice, nuevo_valor):
    print(f"Valor compartido antes de la modificación: {list(valor)}")
    valor[indice] = nuevo_valor
    print(f"Valor compartido después de la modificación: {list(valor)}")

if __name__ == '__main__':
    # Crear un valor compartido entre procesos para los datos numéricos
    datos_compartidos = mp.Array('i', [100, 150, 200, 250])  # Valores iniciales para Q1, Q2, Q3, Q4

    # Crear una lista vacía para guardar los valores de los Forecasts
    valores_forecasts = []

    # Crear cuatro procesos que llaman a la función modificar_valor para cada trimestre
    procesos = []
    for i in range(4):
        proceso = mp.Process(target=modificar_valor, args=(datos_compartidos, i, datos_compartidos[i] + 10))
        procesos.append(proceso)

    # Iniciar los procesos y guardar los valores de los Forecasts
    for proceso in procesos:
        proceso.start()
        proceso.join()
        valores_forecasts.append(list(datos_compartidos))

    # Imprimir el valor final de los datos compartidos
    print("Valores compartidos finales:", list(datos_compartidos))

    # Crear un gráfico de líneas con los valores de los Forecasts
    trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
    for i, valores in enumerate(valores_forecasts):
        plt.plot(trimestres, valores, label=f'Forecast {i+1}')

    plt.xlabel('Trimestre')
    plt.ylabel('Valor')
    plt.title('Modelo de datos con valores compartidos')
    plt.legend()
    plt.savefig('data/procesed/forecast.png')