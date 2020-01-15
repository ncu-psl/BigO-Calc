int partition(int arr, int low, int high){
    int i = low -1;
    int tmp;
    for(int j = low; j < high; j++){
        if(arr[j] < arr[high]){
            i++;
            tmp = arr[j];
            arr[j] = arr[i];
            arr[i] = tmp;
        }
    }
    tmp = arr[i+1];
    arr[i+1] = arr[high];
    arr[high] = tmp;
    return i+1;
}