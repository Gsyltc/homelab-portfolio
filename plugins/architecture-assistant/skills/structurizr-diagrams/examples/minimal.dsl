workspace {

    model {
        !include theme/properties.dsl

        user = person "Utilisateur" "Utilisateur du système"

        !include models/system.dsl
    }

    views {
        !include views/system-context.dsl
        !include views/system-container.dsl
        !include views/system-components.dsl

        styles {
            !include theme/0000-default-styles.dsl
            !include theme/0001-project-styles.dsl
            !include theme/0002-external-tools.dsl
        }
    }

}

# models/system.dsl
system = softwareSystem "Système Exemple" "Description courte (<= 50)" {
    api = container "API" "Service API (<= 50)" {
        controller = component "Contrôleur" "Point d'entrée (<= 50)"
        service = component "Service métier" "Logique métier (<= 50)"
    }
    db = container "Base de données" "Stockage (<= 50)"
}

# Relation consolidée (un seul lien par sens)
user -> system "Utilise"
system.api.controller -> system.api.service "Orchestre"
system.api.service -> system.db "Lit et écrit" "new"

# Extension via !element (ajout de composant dans conteneur défini ailleurs)
/*
!element system.api {
    validator = component "Validateur" "Validation (<= 50)" "new"
}
!relationship system.api.controller -> system.api.validator "Valide"
*/
