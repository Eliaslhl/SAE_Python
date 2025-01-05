import pstats

# Charger les fichiers de profilage
avant = pstats.Stats('avant/avant.stats')
apres = pstats.Stats('après/apres.stats')

# Extraire les appels des fonctions
def extract_ncalls(stats):
    ncalls = {}
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        ncalls[func] = nc
    return ncalls

# Extraire les ncalls avant et après optimisation
avant_ncalls = extract_ncalls(avant)
apres_ncalls = extract_ncalls(apres)

# Fusionner les résultats avant et après dans un tableau limité à 50 fonctions
print("Fonction | Appels Avant | Appels Après")

# Trier les fonctions par nombre d'appels avant
sorted_avant = sorted(avant_ncalls.items(), key=lambda x: x[1], reverse=True)[:50]

# Afficher les 50 premières fonctions
for func, avant_count in sorted_avant:
    apres_count = apres_ncalls.get(func, 0)
    print(f"{func} | {avant_count} | {apres_count}")