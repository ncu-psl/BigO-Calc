import java.util.*;

class Main {

	static int if_else_1(int n) {
		int odd=0;
		if (n%2==0) {
			odd=0;
		} else {
			odd=1;
		}

		return odd;
	}

	static int if_else_without_block(int n) {
		int odd=0;
		if (n%2==0)
			odd=0;
		else
			odd=1;

		return odd;
	}

	static int if_1(int n) {
		int odd=1;
		if (n%2==0)
			odd=0;

		return odd;
	}

    static int if_fun_call(int n) {
        if (if_1(n)) {
            return if_else_1();
        } else {
            return if_else_without_block();
        }
    }

    static int if_fun_call(int n) {
        int k=0;
        if (if_1(n)) {
            for(int i=0;i<n;i++) {
                for(int j=0;j<n;j++) {
                    k++;
                }
            }
        } else {
            k=1;
        }
        return k;
    }

	public static void main (String[] args) {
		int n = 5;
		if_else_1(n);
		if_1(n);
	}
}