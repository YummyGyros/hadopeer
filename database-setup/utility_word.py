
#func getFrenchNoiseWords() []string {
#    return append(append(frenchNoiseWords, frenchVerbAvoir...), frenchVerbEtre...)
#}

frenchNoiseWords = [
    "le", "la", "les", "l",
    "du", "de", "des", "d",
    "un", "une",
    "n", "ne",
    "ce", "ces", "ca", "c", "cet", "cette", "celui", "via", 
    "mon", "mes", "ton", "tes", "son", "sa", "ses", "leur", "leurs", "lui",
    "très", "peu", "beaucoup", "à", "oû", "paul", "vouloir", "gosselin", "alinéa", 
    "et", "en", "au", "aux", "ou", "or", "ni", "car", "sur", "pas", "y", "dire", "patrick", "pierre"
    "avec", "sans", "dont", "par", "mais", "soit", "tant", "dans", "donc", "lors", "aussi", "pendant", "ainsi",
    "comme", "comment", "mme", "Monsieur", "monsieur", "331", "martine", "luc", "lefebvre", "jean", "christian", "brard", "bloch", "riester", "warsmann", "philippe", "luc"
    "parce", "puisqu", "qui", "que", "quoi", "quand", "qu", "qu'", "qu’", "lorsqu", "lorsque", "quel", "quelle", "quels", "quelles", "jusqu", "auxquels", "warsmann", "auxquelles",
    "se", "j", "je", "tu", "t", "il", "elle", "iel", "on", "nous", "vous", "ils", "elles", "iels", "plus", 
    "outre", "autre", "notamment", "après", "non", "mieux", "mme", "autant", "tel", "lequel", "lequelle", "faire", "entre", "aujourd", "tout", "bien", "hui", "numéro"
]

frenchVerbEtre =[
    "être",
# Indicatif
    "suis", "es", "est", "sommes", "etes", "sont",
    "etais", "etait", "etions", "etiez", "etaient",
    "fus", "fut", "fumes", "futes", "furent",
    "serai", "seras", "sera", "serons", "serez", "seront",

# Conditionnel
    "serais", "serait", "serions", "seriez", "seraient",

# Subjonctif
    "sois", "soit", "soyons", "soyez", "soient",
    "fusse", "fusses", "fussions", "fussiez", "fussent",

# Participe
    "etant", "ete",
]

frenchVerbAvoir = [
    "avoir",
    # Indicatif
    "ai", "as", "a", "avons", "avez", "ont",
    "avais", "avait", "avions", "aviez", "avaient",
    "eus", "eut", "eumes", "eutes", "eurent",
    "aurai", "auras", "aura", "aurons", "aurez", "auront",

    # Conditionnel
    "aurais", "aurait", "aurions", "auriez", "auraient",

    # Subjonctif
    "aie", "ais", "ait", "ayons", "ayez", "aient",
    "eusse", "eusses", "eut", "eussions", "eussiez", "eurent",

    # Participe
    "ayant", "eu",
]