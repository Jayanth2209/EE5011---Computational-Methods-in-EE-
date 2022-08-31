#include <math.h>
int i, j, n1, m, ns, ns0;
double den, dift, ho, hp, w;
double *xa, *ya, *x, *y, *dy;   // Window to use by Polynomial Interpolation
c[0] = d[0] = 0.0;
xa = xarr; ya = yarr;
for (j = 0, n1 = 0; j < N; j++) {
    // Loop over xarr points
    x = &xx[j]; y = &yy[j];
    dy = &dyy[j];
    for (i = n1, ns = M-1; i < M; i++) {
        // Loop over x points
        if (*x <= xarr[i]) {
            ns = i;
            break;
        }
    }
    if (i == n1) {
        for (ns = n/2; i >= 0; i--) {
            if (*x > xarr[i]) {
                ns = i;
                break;
            }
        }
    }
    n1 = ns - n/2;
    n1 = (n1 < 0) ? 0 : n1; // Eliminate negative values of n1
    n1 = ((n1 + n >= M) ? M-n-1 : n1); // Eliminate values of n1 that are too large
    xa = &xarr[n1]; ya = &yarr[n1];
    ns -= n1; ns = ((ns < n/2) ? n/2 : ns); // Eliminate values of ns that are too small
    ns0 = ns;
    // From here it's basically the NR Code
    for (i = 0; i <= n; i++) {
        c[i] = ya[i];
        d[i] = ya[i];
    }
    *y = ya[ns--];
    for (m = 1; m <= n; m++) {
        for (i = 0; i <= n-m; i++) {
            ho = xa[i] - *x;
            hp = xa[i+m] - *x;
            w = c[i+1] - d[i];
            if ((den = ho - hp) == 0.0) {
                // Error
                exit(1);
            }
            den = w/den;
            d[i] = hp*den;
            c[i] = ho*den;
        }
        *y += (*dy = ((2*ns < (n-m)) ? c[ns+1] : d[ns--]));
    } // m loop
} // j loop
