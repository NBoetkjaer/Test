# Opgaven lyder: Placer 8 dronninger på et skakbrædt, så ingen dronning er truet af en anden dronning.
# -Så hvis en dronning optager en række, kolonne eller diagonal kan der altså ikke stå en anden dronning på 
# denne række, kolonne eller diagonal.
#
#    Rækker og kolonner         Diagonal 1 og 2
# N-1)    +                  N-1)             +  
#   :)    :                    :)          +     
#   3)    +                    3) x     +        
#   2) x  Q  x  x .. x         2)    Q           
#   1)    +                    1) +     x        
#   0)    +                    0)          x     
#      ~~~~~~~~~~~~~~~            ~~~~~~~~~~~~~~~
#      0  1  2  3 .. N-1          0  1  2  3 .. N-1
#
# En dronning som står på feltet (1,2) - dvs kolonne 1 og række 2. Vil altså optage kolonne 1 og række 2.
# samtidig vil den også optage to diagonaler den ene(x) diagonal går fra feltet (0,3) -> (3,0) og 
# den anden (+) gå fra feltet (0,1)-> (7,6) (der ligger udenfor illustrationen.)
#
# På et kvadratisk ternet brædt er der N * N felter. (et skakbrædt har 8 * 8 = 64 felter)
# Det vil sige at der er N rækker og N kolonner.
# Der (2*N - 1) diagonaler som går den ene vej og (2*N - 1) diagonaler den anden vej.
#
# Vi kan skrive et program som starter med at placere den første dronning og herefter placerer de øvrige dronninger 
# på de frie pladser. Hvis vi laver nogle lister over hvilke rækker, kolonner og diagonaler, som allerede er optaget.
# Kan vi bruge disse, til at finde en fri plads til den næste dronning.
#
# Række og kolonne listerne er simple de følger numereringen på den forrige illustration, dvs. fra 0 til (N-1). 
# For diagonalerne laver vi flg. konvention, som gør det muligt at angive diagonalerne med et nummer fra 0 til (2N-2).
# 
#    Diagonal 1:\ (x)                             Diagonal 2:/ (+)
#  N-1)  N-1   N    N+1  N+2 .. 2N-3  2N-2       N-1)  0    1    2    3  ...  N-2   N-1
#  N-2)  N-2   N-1  N    N+1 .. 2N-4  2N-3       N-2)  1    2    3    4  ...  N-1   N
#  N-3)  N-3   N-2  N-1  N+1 .. 2N-5  2N-4       N-3)  2    3    4    5  ...  N     N+1
#   : )  :    :     :    :  ...  :     :          : )  :    :    :    :  ...  :     :
#   2 )  2    3     4    5  ...  N+1   N+2        2 )  N-3  N-2  N-1  N   .. 2N-5  2N-4
#   1 )  1    2     3    4  ...  N     N+1        1 )  N-2  N-1  N    N+1 .. 2N-4  2N-3
#   0 )  0    1     2    3  ...  N-1   N          0 )  N-1  N    N+1  N+2 .. 2N-3  2N-2
#      ~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~~~~~        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#        0    1     2    3  ...  N-2   N-1             0    1    2    3  ...  N-2   N-1 
#
# Med udgangspunkt i eksemplet, hvor en dronning optager feltet (1,2) kan vi nu angive at:
#  kolonne(1) er optaget
#  række(2) er optaget
#  diagonal_1(3) er optaget
#  diagonal_2(N-2) er optaget
#
# For at finde det diagonal nummer (3), som er optaget i diagonal_1 skal man lægge række og kolonne samen, altså 1+2=3.
# For at finde det diagonal nummer (N-2), som er optaget i diagonal_2, skal man trække rækken fra kolonnen og lægge (N-1) til.
# Dvs. 1-2 + (N-1) = N-2
#

# Her definerer vi listerne over rækker, kolonner og diagonalerne.
N=8
rowIsUsed = [False]*N           # Liste med N elementer som alle er False (dvs. frie).
colIsUsed = [False]*N
diag1IsUsed = [False]*(2*N-1)   # Liste med 2*N-1 elementer som alle er False (dvs. frie).
diag2IsUsed = [False]*(2*N-1)
done = False

# Detter er en funktion til at checke om et felt (col, row) er frit.
# Hvis feltet er frit returnerer funktionen False eller returneres True.
def PositionIsUsed(col, row):
    return  (rowIsUsed[row] or              # Check rækken
            colIsUsed[col] or               # Check kolonnen
            diag1IsUsed[row + col] or       # Check diagonal_1
            diag2IsUsed[col - row + N - 1]) # Check diagonal_2

# Denne funktion bruges til at markere et felt som optaget. Hvis isUsed er True vil de rækker, kolonner 
# og diagonaler som går gennem feltet blive markeret som optaget. Er isUsed lig False vil de 
# blive markeret som frie.
def SetPosition(col, row, isUsed):
    rowIsUsed[row] = isUsed
    colIsUsed[col] = isUsed
    diag1IsUsed[row + col] = isUsed
    diag2IsUsed[col - row + N - 1] = isUsed

# Denne funktion vil prøve at placere en dronning i den angivne række (row). Hvis dette lykkes, 
# kalder funktionen sig selv (recursion) med næste række som argument og returnerer True. Hvis Functionen
# ikke kan placere en dronning vil den returnere False.
# Når alle rækker er fyldt med dronninger returnerer funktionen True.
# og  ikke er mul
def TryPlaceQueen(row):
    global done
    if(row == N):
        done = True  # vi har placeret aller dronningerne og er færdige.
        return True  # Hurra.
    # Prøv at placere en dronning lang en række. (dvs. kolonnen tælles op fra 0 til N-1)
    for col in range(N):
        if not PositionIsUsed(col, row): # Er feltet (col,row) frit (dvs. ikke i brug)?
            SetPosition(col, row, True) # Feltet er frit - marker feltet som optaget. 
            if TryPlaceQueen(row + 1): # Forsæt med at placere en dronning på næste række. (recursion)
                if done:
                    print((col, row))
                return True
            else:
                # Det var ikke muligt at placere en dronning på næste række- Det vil sige at denne position 
                # ikke kunne bruges, marker den som fri igen så vi kan prøve den næste kolonne.
                SetPosition(col, row, False)
    return False # Nu har vi prøvet alle kolonner uden held, så vi returnerer False.

TryPlaceQueen(0)


