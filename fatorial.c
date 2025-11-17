#include <stdio.h>
#include <locale.h>

int fatorar(int a);

int main()
{
    setlocale(LC_ALL, "Portuguese");
    int num = 0;
    
    printf("Digite o número que desejas fatorar: ");
    scanf("%d", &num);
    
    if (num < 0) printf("Número inválido!");
    else printf("%d! = %d", num, fatorar(num));

    return 0;
}

int fatorar(int a){
    if (a == 0) return 1;
    return a *= fatorar(a - 1);
}