// 29-April-2020 - Under COVID-19
#include <stdlib.h>
#include <stdio.h>

int iCalculate(int a, int b, int c, int d)
{
    int ta = a ; // local a
    int pcount = 0, lcount = 0;          // unused here
    int mn = c < d ? c : d;              // minimum value of c vs d
    int mx = c > d ? c : d;              // maximum value of c vs d
    if(ta < c) return 0;                 // nothing todo if a < c
    if(a < mn || b < mn) return 0;
    if(ta == 0) return 0;
    int rv = 0;                          // return value
    int rest[2] = { 0, 0 };              // holds res

    while(ta >= mn)
    {
        if(!ta) break; //
        //printf("1 ta : %d | rv : %d | %d | %d | %d\n", ta, rv, mn, mx, rest[0]);
        if(ta % mn < ta % mx)
        {
            ta -= mn;
            //printf("1 ta : %d | rv : %d | %d | %d | %d\n", ta, rv, mn, mx, rest[0]);
            pcount++;
            if(b < mx)return rv;
            rv += b / mx;
            if(b % mx >= mn)
            {
                rest[1] = b % mx;
                }
            } else
        {
                ta -= mx ;
                //printf("2 ta : %d | rv : %d | %d | %d | %d\n", ta, rv, mn, mx, rest[0]);
                lcount++;
                rv += b / mn;
            }
        rest[0] = pcount * mn;
        }
    //printf("R1 Running recurse with : %d %d %d %d\n", rest[0], rest[1], c, d);
    int rv1 = iCalculate(rest[0], rest[1], c, d);
    //printf("R2 Running recurse with : %d %d %d %d\n", rest[1], rest[0], c, d);
    int rv2 = iCalculate(rest[1], rest[0], c, d);
    rv += (rv1 > rv2 ? rv1 : rv2);
    return rv;
    }

int help(const char name[])
{
    printf("\n\tUsage:  %s pBahan lBahan pArea [lArea]\n\n", name);
    return 0;
    }

int main(int argc, const char * argv[]){
    // argument berisi 5 ;
    int r1, r2;
    if(argc < 4 ) return help(argv[0]);
    const char *a = argv[1], *b = argv[2], *c = argv[3], *d;
    d = argc > 4 ? argv[4] : argv[3];
    // atoi(const * char)
    // --------- alfanumeric to integer ------------

    r1 = iCalculate(atoi(a), atoi(b), atoi(c), atoi(d));
    r2 = iCalculate(atoi(b), atoi(a), atoi(c), atoi(d));
    printf("%d\n", r1 > r2 ? r1 : r2);
    }
