#include <stdio.h>

void hello_world() {
	printf("Hello World!\n");
}

int is_odd(int n) {
	int odd = 0;
	if (n % 2 == 0) {
		odd = 0;
	} else {
		odd = 1;
	}
	return odd;
}

int calc_sum(int n) {
	int sum = 0;
	for (i = 1; i <= n; i++) {
		sum += i;
	}

	return sum;
}

int calc_odd_sum(int n) {
	int sum = 0;
	for (i = 1; i <= n; i++) {
	    if(is_odd(i)) {
		    sum = sum + i;
	    }
	}

	return sum;
}

int factorial(int n) {
	if (n <= 1)
		return 1;
	return n * factorial(n - 1);
}

int main() {
	int n;
	hello_world();
	is_odd(n);
	calc_sum(n);
	factorial(n);
}
