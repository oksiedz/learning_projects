#include <iostream>
#include <ctime>
#include <fstream>
#include <string>
#include <conio.h>
#include <stdlib.h>
#include <cstdlib>
#include <windows.h>
#include <sstream>
#include <cmath>
#include <algorithm>


using namespace std;

class Cechy
{ public:
	string imie;
	int rok_urodzenia;
	int miesiac_urodzenia;
	int dzien_urodzenia;
	string nazwa_dnia_urodzenia;
	string znak_zodiaku;
	char plec;
	string faza_ksiezyca;
	string horoskop_link;
};

Cechy Funboy; 					//Tworzymy dynamiczna tablice obiektow
Cechy tFunboy[10];				// Tworzymy tablice obiektow
Cechy oFunboy; 					//obiekt oFunboy opisany przez klase Cechy
Cechy *pFunboy; 				//deklaracja wskaznika do obiektu
Cechy *ptFunboy = &tFunboy[0];	//przypisanie wskaznikowi wartosci

//-------------------------------------------------------------------------------------
bool f_CzyJestYearUrodzenia ( int v_year )
{
int vl_length=0, vl_rok	= v_year;
	SYSTEMTIME st;
	GetSystemTime(&st);
	//cout << "Podany rok to " << v_year<< endl;
	//cout << "Biezacy rok to " << st.wYear<< endl;
	cin.clear();
	cin.sync();
	//sprawdzam z ilu cyfr sklada sie liczba v_year
	do
	{	vl_rok = vl_rok/10;
		vl_length++;
	} while (vl_rok > 0);

	if (v_year		>	st.wYear 		//jesli podany rok jest wiekszy niz biezacy rok
		|| st.wYear-150	>	v_year		//lub jesli biezacy rok - 150 lat jest wiekszy niz podany rok
		|| vl_length	!=	4)			//lub ilosc cyfr w roku jest <> 4 
		{	cout<< "Podałeś niewłaściwy rok urodzenia. Spróbuj jeszcze raz." << endl;
			getch();
			return false;
		}
	else if (v_year == st.wYear )		//jesli podany rok jest rowny biezacemu
		{	cout<< "Jetes za młody na korzystanie z komputera." << endl;
			getch();
			exit(0);
			return false;
		}
	return true;
}
//-------------------------------------------------------------------------------------
bool f_CzyJestMountUrodzenia ( int v_month )
{	cin.clear();
	cin.sync();
	if (v_month>12 || v_month<1)		//jesli podany miesiac nie istnieje
		{	cout<< "Podałeś niewłaściwy miesiąc urodzenia. Spróbuj jeszcze raz" << endl;
			getch();
			return false;
		}
	return true;
}

//-------------------------------------------------------------------------------------
bool f_CzyJestDayUrodzenia ( int v_day, int v_month, int v_year )
{
	int vl_max_day, i=0;
	int vl_tab_31[7]={1,3,5,7,8,10,12};
	int vl_tab_30[4]={4,6,9,11};
	int vl_tab_28[1]={2};

	cin.clear();
	cin.sync();

	//jesli miesiac to luty
	if (v_month==2 )
	{	//okreslenie czy rok byl przestepny
		if((v_year%4==0 && !(v_year%100==0)) || (v_year%400==0))
			{vl_max_day = 29;}
		else
			{vl_max_day = 28;}

		for( i=0; i < sizeof(vl_tab_28)/sizeof(int); i++)
		{	if( vl_tab_28[i] == v_month && (v_day>0 && v_day<vl_max_day+1))
				return true;
			else
				cout<< "W roku "<<v_year<<" ilość dni w lutym wynosiła: "<<vl_max_day<<endl;
		}
	}
	else
	{	//cout<<"jesli miesiac ma 31 dni"<<endl;
		for( i=0; i < sizeof(vl_tab_31)/sizeof(int); i++)
		{	if( vl_tab_31[i] == v_month && (v_day>0 && v_day<32))
				{	//cout<<"i: "<< i <<" "<<vl_tab_31[i]<<"v_month"<<v_day<<endl;
					return true; }
		}
		//cout<<"jesli miesiac ma 30 dni"<<endl;
		for( i=0; i < sizeof(vl_tab_30)/sizeof(int); i++)
		{	if( vl_tab_30[i] == v_month && (v_day>0 && v_day<31))
			{	//cout<<"i: "<< i <<" "<<vl_tab_30[i]<<"v_month"<<v_day<<endl;
				return true;}
		}
	}
	return false;
}
//---------------------------------------------------------------
void f_ZmienKolor(string value)
{
	if (value == "Niedziela")
	{
		system("Color 0E");
	}
	else if (value == "Poniedziałek")
	{
		system("Color 0A");
	}
	else if (value == "Wtorek")
	{
		system("Color 0B");
	}
	else if (value == "Środa")
	{
		system("Color 0C");
	}
	else if (value == "Czwartek")
	{
		system("Color 03");
	}
	else if (value == "Piątek")
	{
		system("Color 04");
	}
	else
	{
		system("Color 02");
	};
}

//-------------------------------------------------------------------------------------
string f_OdgadnijDzienUrodzin ( int v_day, int v_month, int v_year )
{
	time_t czas;
	struct tm * data;
	const char * dzien_tygodnia[] = { "Niedziela", "Poniedziałek","Wtorek", "Środa", "Czwartek", "Piątek", "Sobota" };

	time( & czas );
	data = localtime( & czas );
	data->tm_year = v_year - 1900;
	data->tm_mon = v_month - 1;
	data->tm_mday = v_day;

	mktime( data );
	f_ZmienKolor(dzien_tygodnia[ data->tm_wday ]);
	return dzien_tygodnia[ data->tm_wday ];
}
//-------------------------------------------------------------------------------------
bool f_CzyPoprawneImie ( string v_name )
{
	int vl_NameLength, i, j, vl_ZnalezionaLiterka=0;
	//char tl_ZbiorZnakow[88]={"ABCDEFGHIJKLMNOPQRSTUVWXYZĄĆĘŁŃÓŚŻŹabcdefghijklmnopqrstuvwxyząćęłńóśżź"};
	string v_szukanyZnak="0123456789!@#$%^&*()_+={}[]:\";'<>,.?/|\'\\";
	size_t znalezionaPozycja = v_name.find( v_szukanyZnak );
	if( znalezionaPozycja != std::string::npos )
		{	cout<< "Wpisane imie jest niepoprawne. Sprobuj jeszcze raz.";
			return false;
		}
return true;
}
//-------------------------------------------------------------------------------------
string f_ImieInitCap ( string v_name )
{	string T_male="ąęśżźćółń";
	string T_duze="ĄĘŚŻŹĆÓŁŃ";
	string lv_name = v_name, lv_DuzaLiterka;
	int lv_polozenie=0;
	
	for (int j=0; j<T_male.length(); j++)
	{	if (lv_name[0]==T_male[j])
			{	lv_polozenie = j; 
				exit;
			}
	}
	if (lv_polozenie >0 )
	{	lv_DuzaLiterka=T_duze[lv_polozenie];
		lv_name.replace(0,1,lv_DuzaLiterka);
	}
	else
		lv_name[0] = toupper(lv_name[0]);

	//for (int j=0; j<lv_name.length(); j++)
	//{	cout<<lv_name[j] <<endl;
	//}

return lv_name;
}
//-------------------------------------------------------------------------------------
/*wyznaczanie plci*/
char f_SprawdzPlec (string v_name)
{
	const string v_imiemeskie[] = {"Barnaba", "Bonawentura", "Jarema", "Jona", "Kosma", "Dyzma"};
	const string v_imiezenskie[] = {"Beatrycze", "Dżanan", "Mariam", "Miriam", "Megi", "Noemi", "Rut", "Szarlin"};
	int v_nietypoweimie = 0;
	for (int i = 0; i < 6; i++)
	{
		if (v_name == v_imiemeskie[i])
		{
			return 'M';
			int v_nietypoweimie = 1;
			break;
		}
	};
	for (int i = 0; i < 8; i++)
	{
		if (v_name == v_imiezenskie[i])
		{
			return 'K';
			int v_nietypoweimie = 1;
			break;
		}
	};
	if (v_nietypoweimie == 0)
	{
		if (v_name[v_name.length() - 1] == 'a')
		{	
			return 'K';
		}
		else
		{
			return 'M';
		};
	}
}

string f_PlecSlownie(char v_gender)
{
	if (v_gender == 'K')
	{
		return "Kobieta";
	}
	else
	{
		return "Mężczyna";
	}
}
/*wyznaczanie plci*/
/*znak zodiaku*/
string f_Zodiak(int v_day, int v_month)
{
	switch (v_month)
		{
			case 1:
				if (v_day < 20) {return "Koziorożec";}
				else{return "Wodnik";};
				break;
			case 2:
				if (v_day < 19) {return "Wodnik";}
				else{return "Ryby";};
				break;
			case 3:
				if (v_day < 21) {return "Ryby";}
				else{return "Baran";};
				break;
			case 4:
				if (v_day < 20) {return "Baran";}
				else{return "Byk";};
				break;
			case 5:
				if (v_day < 23) {return "Byk";}
				else{return "Bliźnięta";};
				break;
			case 6:
				if (v_day < 22) {return "Bliźnięta";}
				else{return "Rak";};
				break;
			case 7:
				if (v_day < 23) {return "Rak";}
				else{return "Lew";};
				break;
			case 8:
				if (v_day < 24) {return "Lew";}
				else{return "Panna";};
				break;
			case 9:
				if (v_day < 23) {return "Panna";}
				else{return "Waga";};
				break;
			case 10:
				if (v_day < 23) {return "Waga";}
				else{return "Skorpion";};
				break;
			case 11:
				if (v_day < 22) {return "Skorpion";}
				else{return "Strzelec";};
				break;
			case 12:
				if (v_day < 22) {return "Strzelec";}
				else{return "Koziorożec";};
				break;
		};
}
/*znak zodiaku*/
/*link do horoskopu*/

string f_ZamienZnak(string v_zodiak)
{
	if (v_zodiak == "Koziorożec")
	{
		return "Koziorozec";
	}
	else if (v_zodiak == "Bliźnięta")
	{
		return "Bliznieta";
	}
	else
	{
		return v_zodiak;
	}
}

string f_HoroskopLink (string v_zodiac)
{
	string url = "https://www.horoskop360.pl/horoskop-";
	string url_part2 = f_ZamienZnak(v_zodiac);
	url_part2[0] = tolower(url_part2[0]);
	return url + url_part2;
}

int f_OtworzLinkHoroskop (string v_zodiac)
{
	string v_url;
	v_url = f_HoroskopLink(v_zodiac);
	ShellExecuteA(NULL, "open", v_url.c_str(), NULL, NULL, SW_SHOWNORMAL);
	return 0;
}
/*link do horoskopu*/
/*wyznaczanie fazy ksiezyca w dniu urodzin*/
double f_FazaKsiezycRang(float value)
{
	int value_1;
	value_1 = 360 * (value / 360 - floor(value / 360));
	if (value_1 < 0)
	{
		value_1 = value_1 + 360;
	};
	return value_1;
}

int f_PrzeksztalcMiesiac (int v_month)
{
	if (v_month < 2)
	{
		return v_month;
	}
	else
	{
		return v_month + 12;
	};
}

int f_PrzeksztalcRok (int v_month, int v_year)
{
	if (v_month < 2)
	{
		return v_year;
	}
	else
	{
		return v_year - 1;
	};
}

float f_FazaKsiezycaPodfunkcja1(int year, int month, int day)
{
	return floor(365.25 * (year + 4716)) + floor(30.6001 * (month + 1)) + day + (2 - floor(year / 100) + floor(floor(year / 100) / 4)) - 1524.5;
}

float f_FazaKsiezycaPodfunkcja2(float value)
{
	return (value - 2451545) / 36525;
}

float f_FazaKsiezycaPodfunkcja3(float value)
{
	return (value + (0.5 / 24) - 2451545) / 36525;
}

float f_FazaKsiezycaPodfunkcja4(float value)
{
	return f_FazaKsiezycRang(297.8502042 + 445267.1115168 * value - (0.00163 * value * value) + value * value * value / 545868 - value * value * value * value / 113065000);
}

float f_FazaKsiezycaPodfunkcja5(float value)
{
	return f_FazaKsiezycRang(357.5291092 + 35999.0502909 * value - 0.0001536 * value * value + value * value * value / 24490000);
}

float f_FazaKsiezycaPodfunkcja6(float value)
{
	return f_FazaKsiezycRang(134.9634114 + 477198.8676313 * value - 0.008997 * value * value + value * value * value / 69699 - value * value * value * value / 14712000);
}

float f_FazaKsiezycaPodfunkcja7(float value1, float value2, float value3)
{
	return 180 - value1 - (6.289 * sin((3.1415926535 / 180) * ((value2)))) + (2.1 * sin((3.1415926535 / 180) * ((value3)))) - (1.274 * sin((3.1415926535 / 180) * (((2 * value1) - value2)))) - (0.658 * sin((3.1415926535 / 180) * ((2 * value1)))) - (0.214 * sin((3.1415926535 / 180) * ((2 * value2)))) - (0.11 * sin((3.1415926535 / 180) * ((value1))));
}

float f_FazaKsiezycaPodfunkcja8(float value)
{
	return (1 + cos((3.1415926535 / 180) * (value))) / 2;
}

float f_FazaKsiezycaPodfunkcja9(float value1, float value2)
{
	if ((value2 - value1) < 0)
	{
		return -1 * value1;
	}
	else
	{
		return value1;
	}
}

float f_FazaKsiezycaPodfunkcja10(float value)
{
	return 100 * value;
}

float f_Fazaksiezyca(int v_year, int v_month, int v_day)
{
	int month, year, day;
	float jdp, tzd, tzd2, elm, elm2, ams, ams2, aml, aml2, asd, asd2, phi1, phi2;
	day = v_day;
	month = f_PrzeksztalcMiesiac(v_month);
	year = f_PrzeksztalcRok(v_month, v_year);
	jdp = f_FazaKsiezycaPodfunkcja1(year, month, day);
	tzd = f_FazaKsiezycaPodfunkcja2(jdp);
	tzd2 = f_FazaKsiezycaPodfunkcja3(jdp);
	elm = f_FazaKsiezycaPodfunkcja4(tzd);
	elm2 = f_FazaKsiezycaPodfunkcja4(tzd2);
	ams = f_FazaKsiezycaPodfunkcja5(tzd);
	ams2 = f_FazaKsiezycaPodfunkcja5(tzd2);
	aml = f_FazaKsiezycaPodfunkcja6(tzd);
	aml2 = f_FazaKsiezycaPodfunkcja6(tzd2);
	asd = f_FazaKsiezycaPodfunkcja7(elm, aml, ams);
	asd2 = f_FazaKsiezycaPodfunkcja7(elm2, aml2, ams2);
	phi1 = f_FazaKsiezycaPodfunkcja8(asd);
	phi2 = f_FazaKsiezycaPodfunkcja8(asd2);
	//cout << "Faza ksiezyca: " << f_FazaKsiezycaPodfunkcja10(f_FazaKsiezycaPodfunkcja9(phi1, phi2)) << endl;
	return f_FazaKsiezycaPodfunkcja10(f_FazaKsiezycaPodfunkcja9(phi1, phi2));
}

string f_FazaKsiezycaSlownie(float faza_ksiezyca)
{
	if (faza_ksiezyca >= -5 && faza_ksiezyca <= 5)
	{
		return "Nów";
	}
	else if (faza_ksiezyca > 5 && faza_ksiezyca < 45)
	{
		return "Rosnący sierp";
	}
	else if (faza_ksiezyca >= 45 && faza_ksiezyca <= 55)
	{
		return "Pierwsza kwadra";
	}
	else if (faza_ksiezyca > 55 && faza_ksiezyca < 95)
	{
		return "Rosnący garb";
	}
	else if (faza_ksiezyca >= 95 && faza_ksiezyca <= -95)
	{
		return "Pełnia";
	}
	else if (faza_ksiezyca > -95 && faza_ksiezyca < -55)
	{
		return "Zanikający garb";
	}
	else if (faza_ksiezyca >= -55 && faza_ksiezyca <= -45)
	{
		return "Trzecia kwadra";
	}
	else if (faza_ksiezyca > -45 && faza_ksiezyca < -5)
	{
		return "Zanikający sierp";
	}
	else
	{
		return "Nie można wyznaczyć fazy księżyca";
	};
}
/*wyznaczanie fazy ksiezyca w dniu urodzin*/
//-------------------------------------------------------------------------------------
/*praca na agregatach*/
long f_LiczbaWierszy()
{
	fstream plik;
	plik.open("zodiak.txt", ios::in);
	plik.clear();
	plik.seekg (0, ios::beg);
	int rows_number = 0;
	string linefornumeration;
	while (!plik.eof())
	{
		getline(plik, linefornumeration);
		rows_number++;
	};
	plik.close();
	return rows_number;
}
void f_AgregatyZBazy(int v_dimension)
{
	fstream plik;
	plik.open("zodiak.txt", ios::in);
	plik.clear();
	plik.seekg (0, ios::beg);
	string line, v_param[(f_LiczbaWierszy()-1)*9];
	long i = 0, j = 0, k = 0;
	while (getline(plik,line))
	{
		istringstream ss(line);
		string token;

		while (getline(ss, token, ';'))
		{
			v_param[i] = token;
			i++;
		};
	};
	string parameter[(f_LiczbaWierszy() - 1)];

	//v_dimension to zmienna, która się ustawia prawidłowo w zależności od wymiaru - czyli np. jak imię to ma być zero, jak druga wartość to 1 etc.
	v_dimension = v_dimension - 1;
	//v_dimension to zmienna, która się ustawia prawidłowo w zależności od wymiaru - czyli np. jak imię to ma być zero, jak druga wartość to 1 etc.
	for (long i = v_dimension; i < (f_LiczbaWierszy() - 1) * 9; i = i + 9)
	{
		parameter[j] = v_param[i];
		j = j + 1;
	};
	sort(parameter, parameter + j);

	string wymiar[j];
	long liczebnosc[j];
	for (long i = 0; i < j; i++)
	{
		if (parameter[i] == "")
		{
			break;
		}
		if (i == 0)
		{
			wymiar[k] = parameter[i];
			liczebnosc[k] = 1;
		}
		if (i != 0)
		{
			if (wymiar[k] == parameter[i])
			{
				liczebnosc[k] = liczebnosc[k] + 1;
			}
			else
			{
				wymiar[k+1] = parameter[i];
				liczebnosc[k+1] = 1;
				k = k + 1;
			};
		}
	}

	cout << "Aggregat po wymiarze: " << endl;
	for (long i = 0; i <= k; i++)
	{
		cout << wymiar[i] << "	" << liczebnosc[i] << endl;
	};
}

void f_ObslugaAgregatow()
{
	int v_dimension;
	int v_loopstop = 0;
	do
	{
		if (f_LiczbaWierszy() > 2)
		{
			cin.clear();
			cin.sync();
			system("cls");
			cout << "Wybierz po jakiej zmiennej chciałbyś pogrupować wyniki:" << endl;
			cout << "1. Po imieniu;" << endl;
			cout << "2. Po roku urodzenia;" << endl;
			cout << "3. Po miesiącu urodzenia;" << endl;
			cout << "4. Po dniu urodzenia;" << endl;
			cout << "5. Po nazwie dnia tygodnia z daty urodzenia;" << endl;
			cout << "6. Po znaku zodiaku;" << endl;
			cout << "7. Po płci;" << endl;
			cout << "8. Po fazie księżyca." << endl;
			cout << "9. Powrót do poprzedniego menu" << endl;
			cin >> v_dimension;
			if (v_dimension == 1 || v_dimension == 2 || v_dimension == 3 || v_dimension == 4 || v_dimension == 5 || v_dimension == 6 || v_dimension == 7 || v_dimension == 8)
			{
				f_AgregatyZBazy(v_dimension);
				v_loopstop = 1;
			}
			else if (v_dimension == 9)
			{
				v_loopstop = 1;
				break;
			}
			else
			{
				cout << "Wybierz wymiar z listy." << endl;
			}
			cout << "Naciśnij dowolny przycisk."<< endl;
			getch();
		}
		else
		{
			cout << "Pusty plik z bazą. Naciśnij dowolny przycisk." << endl;
			v_loopstop = 1;
			getch();
			break;
		}
	} while (v_loopstop = 1);
}
/*praca na agregatach*/
//-------------------------------------------------------------------------------------
void f_ZapiszTabliceDoPliku ()
{	int sizeof_tFunboy = sizeof(tFunboy)/sizeof(tFunboy[0]);
	fstream plik;
	plik.open( "zodiak.txt", ios::out | ios::app );
		//cout<<"zapisuje do pliku"<<endl;
		for (int i=0; i<sizeof_tFunboy; i++)
		{	//plik<<i<<endl;
			if (tFunboy[i].imie!="" && tFunboy[i].rok_urodzenia>0 && tFunboy[i].nazwa_dnia_urodzenia!="")
			{	plik<<tFunboy[i].imie<<';';
				plik<<tFunboy[i].rok_urodzenia<<';';
				plik<<tFunboy[i].miesiac_urodzenia<<';';
				plik<<tFunboy[i].dzien_urodzenia<<';';
				plik<<tFunboy[i].nazwa_dnia_urodzenia<<';';
				plik<<tFunboy[i].znak_zodiaku<<';';
				plik<<tFunboy[i].plec<<';';
				plik<<tFunboy[i].faza_ksiezyca<<';';
				plik<<tFunboy[i].horoskop_link<<';'<<endl;
			}
		}
			plik.flush();
			plik.close();
}
//-------------------------------------------------------------------------------------
void f_PodajDane ()
{
	int v_day, v_month, v_year;
	bool v_czyPoprawneDane = false;
	string v_name, v_dzienUrodzin, v_zodiac;
	char v_gender;

	do
	{ 	cin.clear();
		cin.sync();
		system("cls");
		cout<<"Podaj rok urodzenia" <<endl;
		cin>>v_year;
		v_czyPoprawneDane = f_CzyJestYearUrodzenia( v_year );
	} while (v_czyPoprawneDane == false);

	v_czyPoprawneDane = false;
	do
	{ 	cin.clear();
		cin.sync();
		cout<<"Podaj miesiąc urodzenia" <<endl;
		cin>>v_month;
		v_czyPoprawneDane = f_CzyJestMountUrodzenia( v_month );
	} while (v_czyPoprawneDane == false);

	//cout<< "true: "<< true<<endl;
	//cout<< "false:"<< false<<endl;
	//cout << "v_czyYear:  "<<v_czyYear << endl;
	//cout << "v_czyMount: "<<v_czyMount << endl;

	v_czyPoprawneDane = false;
	do
	{	cin.clear();
		cin.sync();
		cout<<"Podaj dzień urodzenia" <<endl;
		cin>>v_day;
		v_czyPoprawneDane = f_CzyJestDayUrodzenia( v_day, v_month, v_year);
		//cout << "v_czyDay: "<<v_czyDay << endl;
	} while (v_czyPoprawneDane== false);

	v_czyPoprawneDane = true; //po zrobieniu walidacji zmien na false
	do
	{	cin.clear();
		cin.sync();
		cout<<"Podaj imię" <<endl;
		cin>>v_name;
		v_czyPoprawneDane = f_CzyPoprawneImie( v_name) ;	//wywolanie funkcji do walidacji imienia czy np. user nie wpisal 1234...
		//getch();
	} while (v_czyPoprawneDane== false);
	v_name = f_ImieInitCap(v_name);							//initcap - niezaleznie od tego co user wpisal.

	v_dzienUrodzin = f_OdgadnijDzienUrodzin(v_day, v_month, v_year);
	v_gender = f_SprawdzPlec(v_name);
	v_zodiac = f_Zodiak(v_day, v_month);

	oFunboy.imie=v_name;
	oFunboy.rok_urodzenia=v_year;
	oFunboy.miesiac_urodzenia=v_month;
	oFunboy.dzien_urodzenia=v_day;
	oFunboy.nazwa_dnia_urodzenia=v_dzienUrodzin;
	oFunboy.znak_zodiaku=v_zodiac;
	oFunboy.plec=v_gender;
	oFunboy.faza_ksiezyca=f_FazaKsiezycaSlownie(f_Fazaksiezyca(oFunboy.rok_urodzenia, oFunboy.miesiac_urodzenia, oFunboy.dzien_urodzenia));
	oFunboy.horoskop_link=f_HoroskopLink(v_zodiac);

	ptFunboy[0]=oFunboy;		//przypisanie wskaznikowi wartosci

	cin.clear();
	cin.sync();
	system("cls");
	cout << "Cześć "<< oFunboy.imie <<". "<<endl;
	cout << "Data Twoich narodzin to: " << oFunboy.dzien_urodzenia<<"/"<<oFunboy.miesiac_urodzenia<<"/"<<oFunboy.rok_urodzenia<<endl;
	cout << "Dzień Twoich urodzin to: " << oFunboy.nazwa_dnia_urodzenia <<endl;
	cout << "Twoja płeć to: "<< f_PlecSlownie(oFunboy.plec)<< endl;
	cout << "Twój znak zodiaku to: " << oFunboy.znak_zodiaku << endl;
	cout << "W dniu Twoich urodzin była następująca faza księyca: " << oFunboy.faza_ksiezyca << endl;
	cout << "Link do Twojego horoskopu: " << oFunboy.horoskop_link << endl;
	cout << "Kliknij dowolny przycisk, żeby otworzyć horoskop w przeglądarce." << endl;
	f_ZapiszTabliceDoPliku();
	getch();
	f_OtworzLinkHoroskop(v_zodiac);

//	cout << "Press any key to continue... " <<endl;
//	getch();
}
//-------------------------------------------------------------------------------------
bool f_Wytnij_Zapisz(int vl_lp, string vl_linia)
{
	string vl_birthdate, vl_day, vl_month, vl_year, vl_name, vl_dzienUrodzin, vl_zodiac;;
	char vl_separator=';', vl_separator1='-', vl_gender;
	int t_seperatory[2], vl_licznikSeparatorow =0, i, v_day, v_month, v_year, vl_blad;
	bool vl_CzyPoprawneDane;
	//pFunboy = &oFunboy;			//przypisanie wskaznikowi wartosci

	for (i=0; i<vl_linia.length()-1; i++) //powtarzaj dopoki i<dlugosci linii
	{	if (vl_linia[i]==vl_separator)
		{	t_seperatory[vl_licznikSeparatorow]=i; //zbieranie informacji o pozycji separatora
			vl_licznikSeparatorow++;} 
	}
	if (vl_licznikSeparatorow!=2)
		return false;

	vl_name = vl_linia.substr(t_seperatory[0]+1,t_seperatory[1]-t_seperatory[0]-1);
	vl_birthdate=vl_linia.substr(t_seperatory[1]+1,vl_linia.length()-1);
	//cout<< "vl_imie : "<<vl_name<<" vl_birthdate : "<<vl_birthdate<<endl;

	vl_licznikSeparatorow=0;
	for (i=0; i<vl_birthdate.length()-1; i++) //powtarzaj dopoki i<dlugosci vl_birthdate
	{	if (vl_birthdate[i]==vl_separator1)
		{	t_seperatory[vl_licznikSeparatorow]=i; //zbieranie informacji o pozycji separatora1
			vl_licznikSeparatorow++;} 
	}
	vl_year	= vl_birthdate.substr(0,t_seperatory[0]);
	vl_month= vl_birthdate.substr(t_seperatory[0]+1,t_seperatory[1]-t_seperatory[0]-1);
	vl_day	= vl_birthdate.substr(t_seperatory[1]+1,vl_birthdate.length()-1);

	//cout<< "vl_year : "<<vl_year<<" vl_month : "<<vl_month<<" vl_day : "<<vl_day<<endl;

	sscanf(vl_year.c_str(), "%d", &v_year);
	sscanf(vl_month.c_str(), "%d", &v_month);
	sscanf(vl_day.c_str(), "%d", &v_day);

	//sprawdzam poprawnosc danych
	vl_blad = 0;
	vl_CzyPoprawneDane = f_CzyJestYearUrodzenia( v_year );
	vl_blad = (vl_CzyPoprawneDane + vl_blad );
	vl_CzyPoprawneDane = f_CzyJestMountUrodzenia( v_month );
	vl_blad = (vl_CzyPoprawneDane + vl_blad );
	vl_CzyPoprawneDane = f_CzyJestDayUrodzenia( v_day, v_month, v_year);
	vl_blad = (vl_CzyPoprawneDane + vl_blad );
	vl_CzyPoprawneDane = f_CzyPoprawneImie( vl_name) ;		//wywolanie funkcji do walidacji imienia czy np. user nie wpisal 1234...
	vl_blad = (vl_CzyPoprawneDane + vl_blad );
	//koniec sprawdzania poprawnosci danych

	if (vl_blad==4)
	{	vl_name = f_ImieInitCap(vl_name);						//initcap - niezaleznie od tego co user wpisal.	
		vl_dzienUrodzin = f_OdgadnijDzienUrodzin(v_day, v_month, v_year);
		vl_gender = f_SprawdzPlec(vl_name);
		vl_zodiac = f_Zodiak(v_day, v_month);


		oFunboy.imie=vl_name;
		oFunboy.rok_urodzenia=v_year;
		oFunboy.miesiac_urodzenia=v_month;
		oFunboy.dzien_urodzenia=v_day;
		oFunboy.nazwa_dnia_urodzenia=vl_dzienUrodzin;
		oFunboy.znak_zodiaku=vl_zodiac;
		oFunboy.plec=vl_gender;
		oFunboy.faza_ksiezyca=f_FazaKsiezycaSlownie(f_Fazaksiezyca(oFunboy.rok_urodzenia, oFunboy.miesiac_urodzenia, oFunboy.dzien_urodzenia));
		oFunboy.horoskop_link=f_HoroskopLink(vl_zodiac);


		ptFunboy[vl_lp]=oFunboy;
		//cout<<ptFunboy[vl_lp].imie<<";"<<ptFunboy[vl_lp].znak_zodiaku<<endl;

		return true;
	}
	//cout<<"eof"<<endl;
	return false;

}
//-------------------------------------------------------------------------------------
bool f_Import_z_pliku ()
{	string lv_filename, vl_linia, vl_rozszezenie =".csv";
	fstream plik;
	int vl_Lp =0;
	bool vl_CzyPoprawneDane;
	pFunboy = &oFunboy;
	int vl_sizeof_tFunboy = sizeof(tFunboy)/sizeof(tFunboy[0]);
	cin.clear();
	cin.sync();
	system("cls");

	cout<< "Import danych z pliku csv do głównego pliku danych"<<endl;
	cout<< "Plik z danymi do zaimportowania musi zawierać 3 kolumny: "<<endl;
	cout<< "nr kolejny, imię i data urodzenia w formacie yyyy-mm-dd. "<<endl;
	cout<< "Kolumny muszą być oddzielone od siebie ';' "<<endl;
	cout<< "Podaj nazwę pliku .csv z danymi do zaimportowania: ";
	cin>> lv_filename;

	size_t znalezionaPozycja = lv_filename.find( vl_rozszezenie );
	if( znalezionaPozycja == std::string::npos )
	{	lv_filename=lv_filename+vl_rozszezenie;}

		//cout << lv_filename << endl;

	plik.open( lv_filename.c_str(), ios::in );
	if( plik.good() == false )
	{	cout << "Plik nie istnieje."<<endl;
		getch();
		return false;}

	while(!plik.eof())
		{
			getline(plik, vl_linia);
			if (vl_linia.length()!=0)
			{
				vl_CzyPoprawneDane = f_Wytnij_Zapisz(vl_Lp, vl_linia);
				if (vl_CzyPoprawneDane==true)
				{
					if (vl_Lp < vl_sizeof_tFunboy-1)
					{ vl_Lp++;}	
					else
					{ 	f_ZapiszTabliceDoPliku();
						vl_Lp=0;
						//zerowanie tablicy ptFunboy[vl_lp]=oFunboy;
						//zeruje atrybuty obiektu
						for (int i=0; i<vl_sizeof_tFunboy; i++)
						{	//plik<<i<<endl;
							tFunboy[i].imie="";
							tFunboy[i].rok_urodzenia=0;
							tFunboy[i].miesiac_urodzenia=0;
							tFunboy[i].dzien_urodzenia=0;
							tFunboy[i].nazwa_dnia_urodzenia="";
							tFunboy[i].znak_zodiaku="";
							tFunboy[i].faza_ksiezyca="";
							tFunboy[i].horoskop_link="";
						}
					}
				}
			}
		}
	f_ZapiszTabliceDoPliku();
//	delete tFunboy;
	plik.close();
//    getch();
return true;
}
//-------------------------------------------------------------------------------------
void f_OdczytPelnejBazy()
{
	fstream plik;
	plik.open("zodiak.txt", ios::in);
	if (plik.good()==true && f_LiczbaWierszy()>0)
	{
		plik.clear();
		plik.seekg (0, ios::beg);
		cout << "Poniżej znajduje sie wypis z pełnej bazy danych." << endl;
		cout << "W kolumnie po średnikach znajduje się: imię, rok, miesiąc i dzień urodzenia, nazwa dnia tygodnia z daty urodzenia, znak zodiaku, płec, faza księżyca oraz link do horoskopu"<<endl;
		string linia;
		while (getline(plik, linia))
			{
				cout<< linia << endl;
			};
		plik.flush();
		plik.close();
	}
	else
		{	cout <<"Plik nie istnieje" <<endl;
		}
	cout << endl << "Naciśnij dowolny przycisk, żeby wrócił do menu"<< endl;
	getch();
}
//-------------------------------------------------------------------------------------
void f_czyPlikIstnieje()
{
	fstream plik;
	plik.open ("zodiak.txt", ios::in);
	if (plik.good()==false)
		{	plik.open( "zodiak.txt", ios::out | ios::app );
		}
	plik.close();
}
//-------------------------------------------------------------------------------------
int main()
{	//srand(time ( 0 ) );
	//setlocale(LC_CTYPE, "Polish");
	system("chcp 1250");
	setlocale(LC_CTYPE, "pl_PL");
	//SetConsoleOutputCP( 28592 );
	Cechy *pFunboy; //deklaracja wskaznika do obiektu
	char v_znak;
	pFunboy = &oFunboy;
	bool v_Import_z_pliku;
	f_czyPlikIstnieje();

	do
	{
		cin.clear();
		cin.sync();
		system("cls");
		cout <<"Program Horoskop."<< endl;
		cout <<" "<< endl;
		cout <<"Program stworzony na zaliczenie ćwiczeń z Podstaw Programowania."			<< endl;
		cout <<"Jest to praca grupowa Tomasza Oksiędzkiego i Artura Grzegrzółki -"			<< endl;
		cout <<"studentów I roku WSM na kierunku Informatyka."								<< endl<< endl;
		cout <<"Funkcjonalności programu:"													<< endl;
		cout <<"1. Podanie imienia i daty urodzenia"										<< endl;
		cout <<"2. Określenie dnia tygodnia na podstawie daty urodzenia"					<< endl;
		cout <<"3. Zmiana koloru czcionki w zalezności od dnia tygodnia z daty urodzenia"	<< endl;
		cout <<"4. Stworzenie/otwarcie bazy danych"											<< endl;
		cout <<"5. Określenie płci na podstawie imienia"									<< endl;
		cout <<"6. Wyznaczenie wieku użytkownika"											<< endl;
		cout <<"7. Rozpoznanie znaku zodiaku"												<< endl;
		cout <<"8. Zwrócenie horoskopu"														<< endl;
		cout <<"9. Wyznaczenie fazy księżyca w dniu urodzin"								<< endl;
		cout <<"10.Import danych do głównej bazy danych"									<< endl;
		cout <<"11.Funkcja zwracajaca pełną zawartość bazy danych"							<< endl;
		cout <<"12.Agregaty na bazie danych"												<< endl<< endl;
		cout <<"Aby rozpocząć korzystanie z programu wciśnij 1, aby zakończyć działanie programu wciśnij W."<< endl << endl;
		cout<<"Dokonaj wyboru :";

		v_znak = getchar();
		if (v_znak=='W')
		{
			exit(0);
		}

	} while (v_znak!='1');

	do
	{
		cin.clear();
		cin.sync();
		system("cls");
		cout <<"********************* MENU *********************"	<< endl;
		cout << "1. Określenie dnia tygodnia z daty urodzenia	"	<< endl;
		cout << "   Określenie płci na podstawie imienia		"	<< endl;
		cout << "   Wyznaczenie wieku użytkownika				"	<< endl;
		cout << "   Rozpoznanie znaku zodiaku					"	<< endl;
		cout << "   Wyświetl horoskop							"	<< endl;
		cout << "   Wyznaczenie fazy księżyca w dniu urodzin	"	<< endl;
		cout << "2. Wyswietl historię							"	<< endl;
		cout << "3. Dodaj dane z pliku							"	<< endl;
		cout << "4. Pokaż agregaty								"	<< endl;
		cout << "W. Wyjście z programu							"	<< endl;
		cout<<"Wybieram : ";

		v_znak = getchar();
		switch (v_znak)
		{
			case '1':
				f_PodajDane();
//				f_Zapisz_do_pliku();

				cin.clear();
				cin.sync();
				system("cls");
				break;
			case '2':
				f_OdczytPelnejBazy();
				break;
			case '3':
				v_Import_z_pliku=f_Import_z_pliku();
				break;
			case '4':
				f_ObslugaAgregatow();
				break;
			case 'W':
				exit(0);
				break;
			default:
				cout << "Nie ma takiej opcji w menu."<< flush;
				Sleep(750);
				break;
		}
	} while (v_znak!='W');

	return 0;
}