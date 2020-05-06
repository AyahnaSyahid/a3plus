#include <cstdlib>
#include <iostream>

int ibagiArea(int a, int b, int c, int d)
{
    int tmpa = a, tmpb = b;
    int min = c < d ? c : d;
    int max = c > d ? c : d;
    int cnta = 0, cntb = 0;
    int p = 0, l = 0;
    while(tmpa > min)
    {
        if( tmpa%min < tmpa%max)
        {  
            tmpa -= min;
            p++;
            } else {
                tmpa -= max;
                l++;
                }
        }
    int ra[p+l];
    for(int x = 0; x < p; x++)
    {
        ra[x] = 1;
        cnta += b/max;
        }
    for(int x = 0; x < l; x++)
    {
        ra[p+x] = 0;
        cnta += b/min;
        }

    p = 0;
    l = 0;

    while(tmpb > min)
    {
        if(tmpb%min < tmpb%max)
        {
            tmpb -= min;
            p++;
            } else {
                tmpb -= max;
                l++;
                }
        }
    int rb[p+l];
    for(int x = 0; x < p; x++)
    {
        rb[x] = 1;
        cntb += a/max;
        }
    for(int x = 0; x < l; x++)
    {
        rb[x+p] = 0;
        cntb += a/min;
        }
    return cnta > cntb ? cnta : cntb;
    }

int main(int argc, const char *argv[])
{
    int a, b, c, d;
    a = atoi(argv[1]);
    b = atoi(argv[2]);
    c = atoi(argv[3]);
    d = atoi(argv[4]);
    std::cout << ibagiArea(a, b, c, d) << std::endl;
    }
