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

#define RAW_SIZE (1024) 
#define DEFAULT_SAMPLE_RATE 1024000
static int samplingPeriod = 1; //seconds
static std::string numberOfBins = "256";
static std::string numberOfSpectraToAvg = "32";
static rtlsdr_dev_t *dev = NULL;
  
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
  	//std::cout << dev; 
    int r = rtlsdr_read_sync(dev, array, out_block_size, &n_read);
    bytes = write(sockfd, array, RAW_SIZE);
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
    int sockfd;
    struct sockaddr_in serveraddr;
    struct hostent *server;

  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) 
      printf("ERROR opening socket");

  ///* gethostbyname: get the server's DNS entry */
  //server = gethostbyname("wings");
  //if (server == NULL) {
  //    fprintf(stderr,"ERROR, no such host as\n");
  //    exit(0);
  //}

  memset(&serveraddr, '0', sizeof(serveraddr));
  /* build the server's Internet address */
  //bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  //bcopy((char *)server->h_addr, 
  //      (char *)&serveraddr.sin_addr.s_addr, server->h_length);
  serveraddr.sin_port = htons(9999);

  if(inet_pton(AF_INET, "127.0.0.1", &serveraddr.sin_addr)<=0)  
  { 
     printf("Invalid address/ Address not supported \n"); 
     return; 
  }

  /* connect: create a connection with the server */
  if (connect(sockfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) < 0) 
    printf("ERROR connecting");
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
        sleep(1);
    }

    return 0;
}
