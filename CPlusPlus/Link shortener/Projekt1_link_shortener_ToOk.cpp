#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <cmath>
#include <sstream>
#include <string>


using namespace std;

int main(int argc, char** argv) {

fstream file; /*variable for opened file*/
file.open("plik1.txt", ios::in | ios::out | ios::app); /*opening the file*/
file.close();
int program_stop = 0;
do
	{
		/*counter for number of rows - if data base still have space*/
		file.open("plik1.txt", ios::in | ios::out); /*opening the file*/
		file.clear();
		file.seekg (0, ios::beg);
		long number_of_rows_in_the_file=1;
		string line_to_counter;
		if(getline(file,line_to_counter))
			{
				while (!file.eof())
					{
						getline(file,line_to_counter);
						number_of_rows_in_the_file++;
					}
			}
		else
			{
				number_of_rows_in_the_file = 0;
			};
		file.close();
		/*counter for number of rows - if data base still have space*/
		file.open("plik1.txt", ios::in | ios::out); /*opening the file*/
		if (file.good() == true && number_of_rows_in_the_file < 916132832) /*if the file is ok and data base it not full then processing else not*/
			{
				system("cls");
				/*main instructions*/
				cout << endl << "	Welcome in the program which will shorten your link" << endl;
				cout << "	Program make the provided string shorter to 5 digits to format: scinacz.pl/AAAAA," << endl;
				cout << "	where A is sign from sets: {0-9}, {a-z}, {A-Z}" << endl << endl;
				cout << "	Press:" << endl;
				cout << "	 - 1 if you want to check if your link is already in the data base or shorten it;" << endl;
				if (number_of_rows_in_the_file != 0)
					{
						cout << "	 - 2 if you want to see full list of links - before and after shortening;" << endl;
					}
				cout << "	 - any other key if you want to close the programm" << endl;
				
				/*main instructions*/
				int program_mode;
				cin >> program_mode;
				if (program_mode == 1)
				{
					/*coming to the begining of the file*/
					file.clear();
					file.seekg (0, ios::beg);
					/*coming to the begining of the file*/
					cout << "Please input link which you would like to shorten:" << endl;
					string input_link;
					cin >> input_link;
					int link_already_shortened = 0;
					if (number_of_rows_in_the_file != 0)
						{
							/*checking if the inputted link is already existing*/
							string line1;
							while (getline(file, line1))
								{
									istringstream loop1(line1);
									string long_link1, short_link1;
									if (!(loop1 >> long_link1 >> short_link1)) {break;}
									if (long_link1 == input_link)
										{
											link_already_shortened=1;
											cout << "Link which you have inputted " << long_link1 << " was already shortened to scinacz.pl/" << short_link1 << endl;
										}
								}
							/*checking if the inputted link is already existing*/
						}
					/*if th link does not exist in the data base - shortening algorithm*/
					if (link_already_shortened == 0)
						{
							int loop_stop = 0;
							while (loop_stop == 0)
								{
									/*creation of short link*/
									string slownik_znakow = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
									string shortened_link = "";
									for (int i = 0; i < 5; i ++)
										{
											if (i ==0)
												{
													shortened_link = "00000";
												}
											int random_number = floor(rand() * 62 / RAND_MAX);
											shortened_link[i] = slownik_znakow[random_number];
										};
									/*creation of short link*/
									/*going to the beginning of the file*/
									file.clear();
									file.seekg (0, ios::beg);
									/*going to the beginning of the file*/
									/*checking if short link is already existing*/
									int link_status = 0;
									if (number_of_rows_in_the_file != 0)
										{
											while (!file.eof())
												{
													string line1;
													while (getline(file, line1))
														{
															istringstream loop1(line1);
															string long_link1, short_link1;
															if (!(loop1 >> long_link1 >> short_link1)) {break;}
															if (short_link1 == shortened_link)
																{
																	link_status = 1;
																	if (link_status == 1)
																		{
																			break;
																		}
																}
														}
												}
										}
									else
										{
											link_status = 0;
										};
									if (link_status == 1) //still remain in the loop of assigning new short link
										{
											loop_stop=0;
										}
									if (link_status == 0) //short link is unique - writing it to the data base
										{
											loop_stop = 1;
											file.close();
											file.open("plik1.txt", ios::in | ios::out);
											file.clear();
											file.seekg (0, ios::beg);
											string line3;
											int write_in_first_row = 0;
											file.seekg (0, ios::end);
											cout << "Your link " << input_link << ", was shortened to scinacz.pl/" << shortened_link << endl;
											if (number_of_rows_in_the_file == 0)
												{
													file << input_link << "\t" << shortened_link;
												}
											else
												{
													file << endl << input_link << "\t" << shortened_link;
												};
											file.close();
										}
								}
						}
					file.close();
					system("pause");
				};
				if (program_mode == 2 && number_of_rows_in_the_file != 0)
				{
					/*presentation of full data base*/
					/*going to the beginning of the file*/
					file.clear();
					file.seekg (0, ios::beg);
					/*going to the beginning of the file*/
					cout << "Full data base of links is as follows:" << endl << endl;
					string line2;
					while (getline(file, line2))
						{
							istringstream iss2(line2);
							string long_link2, short_link2;
							if (!(iss2 >> long_link2 >> short_link2)) { break; };
							cout << "Long link: " << long_link2 <<" and the short link for it is: scinacz.pl/" << short_link2 << endl;
						}
					cout << endl << "This is the full data base." << endl << endl << endl;
					/*presentation of full data base*/
					file.close();
					system("pause");
				}
				if ((program_mode == 2 && number_of_rows_in_the_file == 0) || (program_mode) != 1 && program_mode != 2) 
				{
					cout << "Program will be closed." << endl;
					program_stop = 1;
					system("pause");
				}
			}
		else
			{
				cout << "Program cannot work. Please close the app and try once again." << endl;
				cout << "Please check if data base file is properly installed on the system or if it has less than 916132832 rows (restriction to the data base)." << endl;
				program_stop=1;
			}
		file.close();
	} while (program_stop != 1);

return 0;

}