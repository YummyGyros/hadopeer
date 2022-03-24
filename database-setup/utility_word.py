
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
    "très", "peu", "beaucoup", "à", "oû",
    "et", "en", "au", "aux", "ou", "or", "ni", "car", "sur", "pas", "y",
    "avec", "sans", "dont", "par", "mais", "soit", "tant", "dans", "donc", "lors", "aussi", "pendant",
    "comme", "comment",
    "parce", "puisqu", "qui", "que", "quoi", "quand", "qu", "qu'", "qu’", "lorsqu", "lorsque", "quel", "quelle", "quels", "quelles", "jusqu", "auxquels", "auxquelles",
    "se", "j", "je", "tu", "t", "il", "elle", "iel", "on", "nous", "vous", "ils", "elles", "iels", "plus", 
    "outre", "autre", "notamment", "après", "non", "mieux", "mme", "autant", "tel", "lequel", "lequelle"
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