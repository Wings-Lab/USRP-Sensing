#include <rtl-sdr.h>
//#include <condition_variable>
#include <memory>
#include <string>
//#include <cstdint>
#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <cstdlib>
#include <ncurses.h>
#include "convenience.hpp"

#define RAW_SIZE 64*1024 
#define DEFAULT_SAMPLE_RATE 1024000
static int samplingPeriod = 1; //seconds
static std::string numberOfBins = "256";
static std::string numberOfSpectraToAvg = "32";
static rtlsdr_dev_t *dev = NULL;

struct sockaddr_in    serveraddr;
static int                   sockfd;

static void set_up_device() 
{
    int dev_index = 0;
	int r;
	dev_index = verbose_device_search("0");
	r = rtlsdr_open(&dev, (uint32_t)dev_index);
    if (r < 0) 
    {
        printf("Failed to open device");
		exit (1);
	}
    verbose_set_sample_rate(dev, DEFAULT_SAMPLE_RATE);
    verbose_set_frequency(dev, 915800000);
    verbose_gain_set(dev, 1);
    verbose_ppm_set(dev, 0);
    verbose_reset_buffer(dev);
}


static	int exec_raw() 
{
    int r = 0;
    int                   bytes = 0;
    uint32_t out_block_size = RAW_SIZE;
    unsigned char *array = NULL;
    array = (unsigned char *)malloc(RAW_SIZE);
    if (array == NULL)
    {
        printf("No memory\n");
        return 0;
    }
    int n_read = RAW_SIZE;
    r = rtlsdr_read_sync(dev, array, out_block_size, &n_read);
    bytes = sendto(sockfd, array, RAW_SIZE, 0, (struct sockaddr *)&serveraddr, sizeof(serveraddr));
    if (r < 0 || bytes < 0) 
    {
	    printf("Error in reading");
        return (1);
    }
    else 
    {
        printf("Read iq successful\n");
	    return (0);
    }
}

void open_socket()
{
  int                   bytes = 0;

  sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0)
    printf("ERROR opening socket");

  memset(&serveraddr, 0, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_port = htons(9999); 
  //serveraddr.sin_addr.s_addr = inet_addr("130.245.144.143"); /* IP of Controller */
  serveraddr.sin_addr.s_addr = inet_addr("130.245.144.114"); /* IP of Controller */
}

int main()
{
    int counter = 0;
  
    set_up_device();
    open_socket();

    while (true) 
    {
	    counter++;
        exec_raw();
        if (counter == 100)
           break;
    }

    return 0;
}
