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

	static int if_else_without_block_1(int n) {
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

    static int if_fun_call_n2(int n) {
        if (if_1(n)) {
            return if_else_1();
        } else {
            return if_for_n2();
        }
    }

    static int if_for_n2(int n) {
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
		if_else_without_block_1(n);
		if_1(n);
		if_fun_call_n2(n);
		if_for_n2(n);
	}
}