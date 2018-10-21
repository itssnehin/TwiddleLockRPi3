//https://stackoverflow.com/questions/20953907/how-to-generate-assembly-listings-in-codeblocks
#include <stdio.h>
#include <stdlib.h>
int main()
{
    int sorta[20];

    //Determine number of elements in array
    int nElements = sizeof(sorta)/sizeof(sorta[0]);

    //Create an array with random ints
    for(int i = 0; i < nElements; i++)
    {
        sorta[i] = rand();
    }

    //print unsorted array
    for(int i = 0; i < nElements; i++)
    {
        printf("%d\n",sorta[i]);
    }

    // sort array
    for (int j = 0; j < nElements; j++)
    {
        for(int i = 0; i < nElements-1; i++)
        {
            //printf("%d\n", sorta[i]);
            if (sorta[i]>sorta[i+1])
                {
                    int b,a;
                    b = sorta[i+1];
                    a = sorta[i];
                    sorta[i+1] = a;
                    sorta[i] =b;
                }
        }
    }


    printf("\n");

    //print sorted array
    for(int i = 0; i < nElements; i++)
    {
        printf("%d\n",sorta[i]);
    }
}
