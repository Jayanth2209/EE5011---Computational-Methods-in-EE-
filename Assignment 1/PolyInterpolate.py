from scipy import *
from matplotlib.pyplot import *
import weave

def PolyInt(xarr, yarr, xx, n):
    M = len(xarr)
    N = len(xx)
    c = zeros((n+1,1))
    d = zeros((n+1,1))
    yy = zeros(xx.shape)
    dyy = zeros(xx.shape)
    
    code = """
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
    """

    weave.inline(code, ['xarr', 'yarr', 'M', 'xx', 'yy', 'dyy', 'N', 'c', 'd', 'n'], compiler = 'gcc')
    return ([yy, dyy, xx])

def SINXX2(LENX,XX,N):
    X = linspace(0,1,LENX)
    AVGERR = []
    MAXERR = []

    for n in N:
        [YY, dYY, XX] = PolyInt(X, sin(X + X**2), XX, int(n))
        Y0 = sin(XX + XX**2)

        AVGERR.append(mean(abs(YY - Y0)))
        MAXERR.append(max(abs(YY - Y0)))
        #print("Average Error in Polynomial Interpolation of %dth Order (X sampled at %d Points): %f" % (n, len(X), mean(abs(YY - Y0))))

        plot(XX, YY, 'ro', XX, Y0, 'b')
        title('Polynomial Interpolation of %dth Order (X sampled at %d Points)' % (n, len(X)))
        xlabel('X')
        ylabel('Y')
        show()
        semilogy(XX, abs(YY - Y0), 'ro', XX, abs(dYY), 'b')
        title('Error in Polynomial Interpolation of %dth Order (X sampled at %d Points)' % (n, len(X)))
        xlabel('X')
        ylabel('Error')
        legend(['Error', 'Derivative'])
        show()
    
    return ([AVGERR, MAXERR])

# QUESTION 1
n = [4] # Order of Polynomial Interpolation
LENX = 5    # Number of points to sample X at
XX = linspace(-0.5,1.5,200)
#[A1, M1] = SINXX2(LENX,XX,n)
#print("Average Error in Polynomial Interpolation of %dth Order (X sampled at %d Points): %f" % (n[0], LENX, A1[0]))
#print("Maximum Error in Polynomial Interpolation of %dth Order (X sampled at %d Points): %f" % (n[0], LENX, M1[0]))

# QUESTION 2
n = [4] # Order of Polynomial Interpolation
LENX = 30   # Number of points to sample X at
XX = linspace(-0.5,1.5,200)
#[A2, M2] = SINXX2(LENX,XX,n)
#print("Average Error in Polynomial Interpolation of %dth Order (X sampled at %d Points): %f" % (n[0], LENX, A2[0]))
#print("Maximum Error in Polynomial Interpolation of %dth Order (X sampled at %d Points): %f" % (n[0], LENX, M2[0]))

# QUESTION 3 & 4
n = array([3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]) # Order of Polynomial Interpolation
LENX = 30   # Number of points to sample X at
XX = linspace(-0.5,1.5,200)
"""
[A3, M3] = SINXX2(LENX,XX,n)
FIG, AX = subplots()
AX.plot(n, A3, 'r', label = 'Average Error')
AX.plot(n, M3, 'b', label = 'Maximum Error')
AX.set_title('Average and Maximum Error in Polynomial Interpolation (X sampled at %d Points)' % (LENX))
AX.set_xlabel('Order of Polynomial Interpolation')
AX.set_ylabel('Error')
AX.legend()
show()
"""

# QUESTION 5
n = array([8,9,10,11,12,13,14,15,16,17]) # Order of Polynomial Interpolation

X = arange(0.1,0.95,0.005)
Y = sin(X*pi)/(sqrt(1-X**2))
XX = linspace(0.1,0.9,1000)
MAXERR = []

for i in n:
    [YY, dYY, XX] = PolyInt(X, Y, XX, i)
    Y0 = sin(XX*pi)/(sqrt(1-XX**2))
    print("Maximum Error in Polynomial Interpolation of %dth Order (X sampled at %d Points): %f" % (i, len(X), max(abs(YY - Y0))))
    MAXERR.append(max(abs(YY - Y0)))
    plot(XX, YY, 'ro', XX, Y0, 'b')
    title('Polynomial Interpolation of %dth Order (X sampled at %d Points)' % (i, len(X)))
    xlabel('X')
    ylabel('Y')
    #show()
    semilogy(XX, abs(YY - Y0), 'ro', XX, abs(dYY), 'b')
    title('Error in Polynomial Interpolation of %dth Order (X sampled at %d Points)' % (i, len(X)))
    xlabel('X')
    ylabel('Error')
    legend(['Error', 'Derivative'])
    #show()

for err in MAXERR:
    if (err < 0.00001):
        print("Order of Polynomial Interpolation that produces less than 0.000001 error: %d" % (n[MAXERR.index(err)]))
        break