# Spazer tool for processing web pages

from bs4 import BeautifulSoup
import pathlib
import re

# Variables to track the input, output and gained space
space_gained = 0
space_input = 0
space_output = 0

# Intervals of text that we will keep
intervals = []
interval_size = 60

keyAddress = ['\bOffice\b','\bComplex\b','\bApartment\b','\bBuilding\b',
                 '\bTower\b','\bFloor\b','\bFlat\b','\bBlock\b','\bSector\b',
                 '\bDistrict\b','\bMarket\b','\bDepartment\b','\bStation\b',
                 '\bPillar\b','\bMetro\b','\bLane\b','\bShop\b','\bCollege\b',
                 '\bEast\b','\bWest\b','\bNorth\b','\bSouth\b','\bOpposite\b',
                 '\bFax\b','\bPlaza\b','\bBranch\b','\bTel\b','\bEnclave\b',
                 '\bEnquiry\b','\bPIN\b','\bMarg\b','\bPlot\b','\bNear\b','\bContact\b',
                 '\bCircle\b','\bChungi\b','\bPark\b','\bMall\b','\bHouse\b',
                 '\bBhavan\b','\bBhawan\b','\bAddress\b','\bPhone\b','\bID\b',
                 '\bTechnology\b','\bTechnologies\b', '\bInc\.'
                 
                 '\b0-9\b','\(s\)','\bNo\.','\bNumber\b',
                 '\bRoad\b','\bRd\b','\bRd\.',
                 '\(T\)','\(F\)',

                 '\bGandhi\b','\bBose\b','\bAmbedkar\b','\bShaheed\b','M\.G\.',
                 '\bKalam\b','\bKhan\b','\bSingh\b','\bZafar\b','\bNehru\b',
                 '\bScindia\b','\bAzad\b','\bRafi\b','\bThyagaraja\b','\bTilak\b',
                 '\bVivekanand\b','\bMaharaja\b','\bAkbar\b','\bAli\b','\bJustice\b',
                 '\bTeresa\b','\bMandela\b','\bJawahar\b','\bMaharshi\b','\bShahjahan\b',
                 '\bHussain\b','\bRani\b','\bNetaji\b','\bSwami\b','\bShri\b','\bSri\b',

                 '\bLieutenant\b','\bColonel\b','\bBrigadier\b','\bMarshal\b','\bSquadron\b',
                 '\bCommodore\b','\bAdmiral\b','\bSubedar\b',

                 'Nagar\b','Garh\b','llur\b','bakkam\b','pur\b','\bSalai\b',
                 'pura\b','gaon\b','halli\b','palle\b','wadi\b','patti\b',
                 'abad\b','khurd\b','ariya\b','kalan\b','para\b','pora\b',
                 'pada\b','hara\b','har\b','khera\b','chak\b','guda\b','bari\b',
                 'pore\b','kot\b','palli\b','pud\b','puzha\b'
                 ]

keyStates = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                 'Chhattisgarh','\bGoa\b','Gujarat','Haryana','Himachal Pradesh',
                 'Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra',
                 'Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Orissa','Punjab',
                 'Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh',
                 'Uttarakhand','West Bengal','Uttranchal','Hariyana','Panjab','Madras',
                 
                 'Andaman and NicobarIslands','Chandigarh','Delhi','New Delhi',
                 'Jammu and Kashmir','Ladakh','Lakshadweep','Puducherry',

                 'Amravati','Visakhapatnam','Itanagar','Dispur','Guwahati',
                 'Patna','Panaji','Vasco da Gama','Gandhinagar','Ahmedabad',
                 'Chandigarh','Faridabad','Shimla','Dharamshala','Ranchi',
                 'Jamshedpur','Banagalore','Bengaluru','Thiruvananthpuram',
                 'Trivandrum','Bhopal','Indore','Mumbai','Bombay','Imphal',
                 'Shillong','Aizawl','Kohima','Dimapur','Bhubaneswar','Cuttack',
                 'Ludhiana','Jalandhar','Jaipur','Kota','Jodhpur','Gangtok',
                 'Chennai','Hyderabad','Agartala','Lucknow','Ghaziabad','Noida',
                 'Kanpur','Dehradun','Kolkata','Port Blair','Daman','Silvassa',
                 'Srinagar','Jammu','Leh','Kargil','Kavaratti','Andrott','Pondicherry',
                 '\bPune\b','Ajmer','Gwalior','Rajkot','Panaji','Surat','Nagpur',
                 'Thane','Vadodra','\bAgra\b','Nashik','Nasik','Meerut','Kalyan',
                 'Dombivali','Vasai','Virar','Varanasi','Aurangabad','Dhanbad',
                 'Amritsar','Allahabad','Prayagraj','Jabalpur','Coimbatore',
                 'Vijayawada','Madurai','Solapur','Tiruchirappalli','Trichy',
                 'Mysore','Bareily','Gurugram','Gurgaon','Aligarh','Warangal',
                 'Saharanpur','Gorakhpur','Bikaner','Kochi','Kolhapur','\bLoni\b',
                 'Poona','Calcutta']

patternAddressStr = "|".join(keyAddress)
patternAddressStr = r'{}'.format(patternAddressStr)

patternStatesStr = "|".join(keyStates)
patternStatesStr = r'{}'.format(patternStatesStr)

patternAddress = re.compile(patternAddressStr,flags=re.I)
patternStates = re.compile(patternStatesStr,flags=re.I)
patternPIN = re.compile(r"\b\d\d\d\d\d\d\b|\b\d\d\d \d\d\d\b")
patternPhone = re.compile(r"\+91|\(\+91\)|\b\d\d\d\d\d\d\d\d\d\d\b|\+91(\s)")
patternEmail = re.compile(r"@|\[at\]|\[dot\]")
patterns = [patternAddress, patternStates, patternPIN, patternEmail, patternPhone]

print("Welcome to Spazer\n")

for x in range(10):
    filename = str(x) + ".html"
    file = pathlib.Path('input/' + filename)
    if (file.exists()):

        # Read each file
        print("Reading " + filename)
        f = open('input/' + filename, 'r', errors="ignore")
        contents = f.read()   
        
        # Remove html tags
        soup = BeautifulSoup(contents, 'lxml')        
        output = soup.get_text() 
        
        # Your code begins
        for pattern in patterns:
            for match in re.finditer(pattern, output):
                span = match.span()
                intervals.append((span[0] - interval_size, span[1] + interval_size))
        result_chars = []
        skipped_prev_char = False
        for (i, ch) in enumerate(output):
            add_char = False
            for (start, end) in intervals:
                if start <= i and i <= end:
                    add_char = True
                    break
            
            if add_char:
                if skipped_prev_char:
                    # Add \n to seperate this character from earlier characters in the string.
                    result_chars.append('\n')
                result_chars.append(ch)
                skipped_prev_char = False
            else:
                skipped_prev_char = True
        output = "".join(result_chars)

        # Remove extra spaces and newlines
        output = re.sub('\n+', '\n', output)
        output = re.sub(' +', ' ', output)
        output = re.sub('\n ', '\n', output)
        output = re.sub(' \n', '\n', output)
        # Your code ends
        
        # Write the output variable contents to output/ folder.
        print ("Writing reduced " + filename)
        fw = open('output/' + filename, "w")
        fw.write(output)
        fw.close()
        f.close()
        
        # Calculate space savings
        space_input = space_input + len(contents)
        space_output = space_output + len(output)
        
space_gained = round((space_input - space_output) * 100 / space_input, 2)

print("\nTotal Space used by input files = " + str(space_input) + " characters.") 
print("Total Space used by output files = " + str(space_output) + " characters.")
print("Total Space Gained = " + str(space_gained) + "%") 
