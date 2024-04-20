/*
Name: Hadi Abdelaal
Script: Grading Script
*/


#include<iostream>
using namespace std;
int main()
{

    //Create placeholder for 5 assignments and set initial average to 0
    int grade[5], i;
    float sum = 0, avg;

    //This will ask for the grades of the 5th assignment. 
    std::cout << "\n Enter Student's grades for the 5 assignments: \n -----------------------------------------------";

    //Output assignment designations.
    std::cout << "\n Assignment 1: ";
    cin >> grade[0];
    std::cout << "\n Assignment 2: ";
    cin >> grade[1];
    std::cout << "\n Assignment 3: ";
    cin >> grade[2];
    std::cout << "\n Assignment 4: ";
    cin >> grade[3];
    std::cout << "\n Assignment 5: ";
    cin >> grade[4];

    //This will calculate the sum of all assignments.
    for (i = 0; i < 5; i++)
    {
        sum = sum + grade[i];
    }

    //This will calculate the average, then print the letter grade based on the average of the grades. 
    std::cout << "-----------------------------------------------\n Sum of all graded assignments = " << sum;
    avg = sum / 5;
    std::cout << "\n Average: " << avg;
   std::cout << "\n Final Calculated Grade: ";

    if (avg > 89)
    {
        cout << "A";
    }
    else if (avg > 79 && avg <= 89)
    {
        cout << "B";
    }
    else if (avg > 69 && avg <= 79)
    {
        cout << "C";
    }
    else if (avg > 59 && avg <= 69)
    {
        cout << "D";
    }
    else
    {
        cout << "F";
    }
    return 0;
}