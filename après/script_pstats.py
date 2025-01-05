import pstats

# Charger les résultats du profilage
p = pstats.Stats('profile_output.prof')

# Trier les fonctions par nombre d'appels
p.strip_dirs().sort_stats('calls')

# Afficher les 50 premières fonctions avec le plus grand nombre d'appels
p.print_stats(50)