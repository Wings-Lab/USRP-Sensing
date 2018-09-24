#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/sctp.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define RAW_SIZE 1024*1024

void rtl_receive()
{
  int                   n;
  int                   sockfd;
  char                  buf[RAW_SIZE];
  socklen_t             clientlen;
  struct sockaddr_in    serveraddr;
  struct sockaddr_in    clientaddr;
  int                   portno = 9999;

  sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0)
    printf("ERROR opening socket\n");

  memset(&serveraddr, 0, sizeof(serveraddr));
  memset(&clientaddr, 0, sizeof(clientaddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_addr.s_addr = INADDR_ANY;
  serveraddr.sin_port = htons(portno);

  if (bind(sockfd, (struct sockaddr *) &serveraddr, sizeof(serveraddr)) < 0)
    printf("ERROR on binding\n");

  while(1)
  {
    n = recvfrom(sockfd, buf, RAW_SIZE,
                MSG_WAITALL, ( struct sockaddr *) &clientaddr, &clientlen);
    if (n < 0)
      printf("ERROR in recvfrom\n");
    else
    {
      printf("Message received: %d\n", n);
    }
  }
}

int main()
{
  rtl_receive();
}
