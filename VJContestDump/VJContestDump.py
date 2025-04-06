input_text = """
	6 / 7	A	QOJ 8420	Ciphertext
2 / 7	B	QOJ 1250	Tokens
2 / 3	C	QOJ 1458	Binary Search Algorithm
0 / 1	D	QOJ 1844	Cactus
1 / 1	E	QOJ 7598	Steel Ball Run
F	QOJ 6550	Elimination Race
G	QOJ 7578	Salty Fish
	1 / 2	A	QOJ 7349	UFO Rectangles
Solved	4 / 6	B	QOJ 2204	Border
Solved	2 / 3	C	QOJ 7188	Aho-Corasick Automaton
D	QOJ 6555	Sets May Be Good
E	QOJ 1465	Not Our Problem
F	QOJ 7126	Control point
1 / 1	G	QOJ 7129	Independent set
H	QOJ 8435	Empty Vessels
I	QOJ 1167	Expected Distance
J	QOJ 2615	Surround the Cat
K	QOJ 1816	Multiple Parentheses
L	QOJ 2567	Hidden Rook
M	QOJ 866	Display of Springs
	6 / 8	A	QOJ 7504	HearthStone
4 / 6	B	QOJ 2621	First Occurrence
1 / 1	C	QOJ 1864	Might and Magic
6 / 6	D	AtCoder arc189_e	Straight Path
Solved	7 / 9	A	Gym 102361E	Escape
B	Gym 102428A	Algorithm Teaching
Solved	3 / 4	C	Gym 103861H	Check Pattern is Good
D	Gym 102896O	Optimum Server Location
2 / 2	E	Gym 102984J	Setting Maps
F	Gym 102832H	Combination Lock
G	Gym 103427D	Cross the Maze
Solved	3 / 3	H	CodeForces 1178H	Stock Exchange
Solved	5 / 5	I	AtCoder arc142_e	Pairing Wizards
3 / 3	J	CodeForces 739D	Recover a functional graph
3 / 3	K	CodeForces 1305H	Kuroni the Private Tutor
Solved	1 / 1	L	CodeForces 925F	Parametric Circulation
2 / 2	M	CodeForces 1861F	Four Suits
		A	CodeForces 1477E	Nezzar and Tournaments
2 / 2	B	洛谷 P6816	Quasi-template
10 / 10	C	QOJ 7245	Frank Sinatra
11 / 24	D	CodeForces 1313E	Concatenation with intersection
	2 / 2	A	QOJ 6119	Frustration and Bracket Sequences
2 / 2	B	QOJ 1088	Border Similarity Undertaking
12 / 13	C	QOJ 7245	Frank Sinatra
Solved	10 / 12	D	LibreOJ 3033	两个天线
2 / 2	E	LibreOJ 3038	穿越时空 Bitaro
2 / 2	F	LibreOJ 3539	猫或狗
		A	洛谷 P6849	大葱的神力
3 / 3	B	洛谷 P4298	祭祀
12 / 12	C	洛谷 P6122	Mole Tunnels
5 / 5	D	AtCoder agc031_e	Snuke the Phantom Thief
Solved	4 / 7	E	UVA 1389	Hard Life
Solved	8 / 10	F	AtCoder agc038_f	Two Permutations
G	洛谷 P8291	学术社区
4 / 4	H	CodeForces 1517G	Starry Night Camping
1 / 1	I	CodeForces 1383F	Special Edges
Solved	2 / 3	J	CodeForces 1416F	Showing Off
K	UVA 12433	Rent a Car
L	CodeForces 1427G	One Billion Shades of Grey
M	CodeForces 1718D	Permutation for Burenka
N	CodeForces 1666K	Kingdom Partition
5 / 10	O	AtCoder arc129_e	Yet Another Minimization
2 / 3	P	AtCoder arc137_e	Bakery
Q	CodeForces 1662J	Training Camp
R	洛谷 P9726	Magic
Solved	18 / 20	A	CodeForces 2048G	Kevin and Matrices
4 / 4	B	CodeForces 2048H	Kevin and Strange Operation
Solved	7 / 7	C	QOJ 4283	Power of XOR
Solved	15 / 18	D	QOJ 8428	Partition into Teams
E	QOJ 4845	DFS
F	QOJ 6545	Connect the Dots
0 / 1	G	QOJ 1845	Permute
4 / 6	H	QOJ 7302	Walk of Length 6
1 / 1	I	QOJ 1277	Permutation
1 / 1	J	QOJ 6118	Eartheart
		A	QOJ 8435	Empty Vessels
2 / 3	B	QOJ 1167	Expected Distance
C	QOJ 2615	Surround the Cat
Solved	3 / 4	D	QOJ 1816	Multiple Parentheses
Solved	2 / 2	E	QOJ 2567	Hidden Rook
F	QOJ 866	Display of Springs
G	QOJ 7561	Digit DP
H	QOJ 6352	SPPPSPSS.
Solved	2 / 2	I	POJ 3377	Ferry Lanes
Solved	3 / 3	J	POJ 3422	Kaka's Matrix Travels
K	POJ 3016	K-Monotonic
Solved	11 / 22	A	HDU 5457	Hold Your Hand
Solved	10 / 14	B	CodeChef GNUM	Game of Numbers
C	CodeForces 1427G	One Billion Shades of Grey
Solved	3 / 10	D	CodeForces 1383F	Special Edges
Solved	10 / 10	E	QOJ 4283	Power of XOR
4 / 4	F	QOJ 1277	Permutation
Solved	1 / 1	A	QOJ 7580	Milk Candy
B	QOJ 1349	Towns and Roads
C	QOJ 1343	Zombie Land
D	QOJ 7330	Territory Game
E	QOJ 7322	Random Numbers
F	QOJ 2546	High Powers

"""

# Split the input text into lines
lines = input_text.strip().split('\n')

# Process each line and create the output format

mp={}

output_lines = []
for line in lines:
    parts = line.split('\t')
    # print(parts)
    
    # Check if the line has enough parts (at least 3)
    if len(parts) >= 3:
        platform = parts[-2].split()[0]  # Get the platform (QOJ or AtCoder)
        problem_id = parts[-2].split()[1]  # Get the problem ID
        
        if (platform,problem_id) in mp:
            continue
        mp[(platform,problem_id)]=1

        # Always consider the problem as solved ('1')
        output_line = f"{platform}\t|\t{problem_id}\t|\t1\t|"
        output_lines.append(output_line)



# Join the output lines
output_text = '\n'.join(output_lines)

# Print the output text
print(output_text)