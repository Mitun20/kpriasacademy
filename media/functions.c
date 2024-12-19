#include<stdio.h>

int g = 0;
int func1()
{
    int l = 0;
    static int s = 0;
    l = l + 1;
    g = g + 1;
    s = s + 1;

    printf("%d %d %d\n",l,g,s);



}



int main()
{

    func1();
    func1();
    func1();

}




