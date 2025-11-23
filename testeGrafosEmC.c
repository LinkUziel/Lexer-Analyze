#include <stdio.h>
#define MAX_VERTICES 10

int grafo[MAX_VERTICES][MAX_VERTICES];
int numVertices;

void inicializarGrafo(int vertices){
    numVertices = vertices;
    for (int i = 0; i < numVertices; i++){
        for (int j = 0; j < numVertices; j++){
            grafo[i][j] = 0;
        }
    }
}

void adicionarAresta(int origem, int destino){
    grafo[origem][destino] = 1;
    grafo[destino][origem] = 1;
}

void imprimirGrafo(){
    printf("Matriz de Adjacência:\n");
    for (int i = 0; i < numVertices; i++){
        for (int j = 0; j < numVertices; j++){
            printf("%d ", grafo[i][j]);
        }
        printf("\n");
    }
}

int main(){
    inicializarGrafo(10);
   
   
    for(int i=1;i<9;i++){
            adicionarAresta(0, i);
            adicionarAresta(9, i);
            if (i != 4){
                adicionarAresta(i, i);
            }
            for (int j = 8; j > 0; j--){
                if (i + j == 9) {
                    adicionarAresta(i, j);
                }
            }
        }
   
    imprimirGrafo();
    return 0;
}
