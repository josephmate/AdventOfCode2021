#include <stdio.h>

int one_digit(int prev, int input, int q, int r, int s) {
   int remainder = (prev % 26) + r;
   if (remainder != input) {
     return (prev / q)*26 + (input + s);
   } else {
     return prev / q;
   }
}

int LENGTH = 14;
int Q[] = {1, 1, 1, 26, 1, 1, 26, 1, 26, 1 , 26, 26, 26, 26};
int R[] = {12, 13, 12, -13, 11, 15, -14, 12, -8, 14, -9, -11, -6, -5};
int S[] = {1, 9, 11, 6, 6, 1, 13, 5, 7, 2, 10, 14, 7, 1};

int is_valid_faster(int inputs[]) {
    int prev = 0;
    for(int i = 0; i < LENGTH; i++) {
        prev = one_digit(prev, inputs[i], Q[i], R[i], S[i]);
    }
    return prev == 0;
}

void find_monad_faster() {                // 58 days
    for(int a = 9; a >= 1; a--) {         // 6.5 days
      for(int b = 9; b >= 1; b--) {       // 17.41500 hours
        for(int c = 9; c >= 1; c--) {     // 116.1 minutes
          for(int d = 9; d >= 1; d--) {   // 12.9 min
            for(int e = 9; e >= 1; e--) { // 86 sec
              printf("%d\n", e);
              for(int f = 9; f >= 1; f--) {
                for(int g = 9; g >= 1; g--) {
                  for(int h = 9; h >= 1; h--) {
                    for(int i = 9; i >= 1; i--) {
                      for(int j = 9; j >= 1; j--) {
                        for(int k = 9; k >= 1; k--) {
                          for(int l = 9; l >= 1; l--) {
                            for(int m = 9; m >= 1; m--) {
                              for(int n = 9; n >= 1; n--) {
                                int inputs[] = {a, b, c, d, e, f, g, h, i, j, k, l, m, n};
                                if (is_valid_faster(inputs)) {
                                  printf("[%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d]\n", a, b, c, d, e, f, g, h, i, j, k, l, m, n);
                                  return;
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
}


int main() {
  find_monad_faster();
}
