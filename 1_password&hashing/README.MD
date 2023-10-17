# Hashing and Password Breaking Competition
Compete password breaking, in the shortest time with combination of various tactics. BF, rainbow, dictionary attack using hashcat

## Bruteforce Vs Dictionary Attack
a)	Dictionary Attack.   Based on the provided Dictionary.txt, 6 out of 15 MD5 digests were found in 1.04 sec.

b)	Bruteforce Attack.   My python scripted was written such that it filtered out those hashes that were not cracked by dictionary attack to be sent for bruteforce attack., i.e. on the remaining 9 hashes, as there is no meaning to re-run those hashes that were already crack via dictionary attack. This also saves that computation time. 4 more MD5 digests  were found in 27.80 sec.

c)	Rainbow Table.   The used of Rainbow Table was explored with 6 settings, with chain length as 3800 but with the chain number varying from 80K to 1260K. This was to produce a ratio from 5 to 80 when compared with the number of combinations (365 ~= 60M, for 5-character space) that bruteforce could generate. 

d)	From the ratio of 20 and onwards, all 15 passwords (blue box)) were cracked in 12.68 sec being the fastest. Consequently, a longer time was also required to generate the respective rainbow tables based on the different settings.
