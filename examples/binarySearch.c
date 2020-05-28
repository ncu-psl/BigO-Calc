int binarysearch(int data, int key, int n){
    int low = 0;
    int high = n - 1;
    while (low <= high){
        low = 0;
        int mid = (low + n) / 2;
        if (data[mid] == key){
            return mid;
        }
        else if (data[mid] < key){
            low = (low + high)/2 + 1;
        }
        else if (data[mid] > key){
            high = (low + high)/2 - 1;
        }
        
    }
    return -1;
}