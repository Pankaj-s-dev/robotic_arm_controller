#include <stdio.h>
#include<istream>
#include<stdio.h>

int main(){
    std::string data = "{p}{12}{13}{34}\r\n";
    const char *converted_data = data.c_str();
    printf("%s", converted_data);
    char *fina_data;
    int a, b, c;
    std::sscanf(converted_data, "{%s}{%d}{%d}{%d}",fina_data, &a, &b, &c);
    printf("Final data%s  a%d, b%d, c%d",fina_data, a,b,c);
}