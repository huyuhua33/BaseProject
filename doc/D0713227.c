#include<stdio.h>
#include<stdlib.h>
#include<time.h> 

int main()
{
	int n,m,i,j,position[2]={0};;
	
	FILE *fptr;
	fptr=fopen("D0713227.csv","w");
	srand(time(NULL));
	while(1)//input 
	{
		scanf("%d %d", &m, &n);//amount of map 
		scanf("%d %d",&position[0],&position[1]);//bug position
		if(m<=40||m>2||n<=20||n>2)//if legal
		{
			break;//go
		}
		else//else print error
		{
			printf("ERROR");
		}
	}
	
	int *ptr = malloc(m * n * sizeof(int));//call m*n memory 
    for(i = 0; i < m; i++) //to zero
	{
        for( j = 0; j < n; j++)
		{
            *(ptr + n*i + j) = 0;
        }
    }
	int flag=0,s_flag=1,count=0,r=rand()%8,m_x=position[0]-1,m_y=position[1]-1;
	*(ptr+n*m_x+m_y)=1;
	while(s_flag!=(m*n)&&count!=50000)//if index dosent have 0 or count 50000 times =>pop out
    {
    	r=rand()%8;
    	//eight position to go
    	/*
    		2 1 0
    		4 * 3
    		7 6 5
    	*/
	    switch(r)
		{
			case 0:
				m_x--,m_y++;
				break;
			case 1:
				m_x--;
				break;
			case 2:
				m_x--,m_y--;
				break;
			case 3:
				m_y++;
				break;
			case 4:
				m_y--;
				break;
			case 5:
				m_x++,m_y++;
				break;
			case 6:
				m_x++;
				break;
			case 7:		
				m_x++,m_y--;
				break;
		}
		
		if(m_x<0)//if hit wall=>go back to original index
		{
			if(r==0)
			{
				m_y--;
			}
			if(r==2)
			{
				m_y++;
			}
			m_x++;
			flag=1;
		}
		if(m_x>=m)
		{
			if(r==7)
			{
				m_y++;
			}
			if(r==5)
			{
				m_y--;
			}
			m_x--;
			flag=1;
		} 
		if(m_y<0)
		{
			if(r==2)
			{
				m_x++;
			}
			if(r==7)
			{
				m_x--;
			}
			m_y++;
			flag=1;
		}
		if(m_y>=n)
		{
			if(r==0)
			{
				m_x++;
			}
			if(r==5)
			{
				m_x--;
			}
			m_y--;
			flag=1; 
		}
		
		if (flag!=1)
		{
			if((*(ptr + n*m_x + m_y ))==0)//counting is there still have 0 in the index?
			{
				s_flag+=1;	
			}
			*(ptr + n*m_x + m_y ) +=1;	//+1
			count+=1;
		}
	 	flag=0;
	}
	
	fprintf(fptr,"counting:%d\n",count);
	for(i = 0; i < m; i++) 
	{
	    for( j = 0; j < n; j++) 
		{
			if(j==n-1)//if last one 
			{
				fprintf(fptr , "%d\n", *(ptr+n*i+j));//go next row	
			}
			else
			{
				fprintf(fptr, "%d,", *(ptr+n*i+j));	//write file
			} 
	    } 
	} 
	return 0;
}



